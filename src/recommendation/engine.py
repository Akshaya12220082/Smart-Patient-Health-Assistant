"""
Simple rules-based recommendation engine with risk stratification.
"""

from __future__ import annotations

from typing import Dict, Any, List

from src.utils import load_config


def risk_band(score_0_100: float, config_path: str | None = None) -> str:
    """Determine risk band from score with granular levels"""
    try:
        config = load_config(config_path)
        thresholds = config["risk_thresholds"]
        score = float(score_0_100)
        g0, g1 = thresholds["green"]
        y0, y1 = thresholds["yellow"]
        r0, r1 = thresholds["red"]
        if g0 <= score <= g1:
            return "green"
        if y0 <= score <= y1:
            return "yellow"
        if r0 <= score <= r1:
            return "red"
    except Exception:
        # Fallback to granular thresholds if config fails
        score = float(score_0_100)
        if score <= 25:
            return "green_low"
        elif score <= 40:
            return "green_high"
        elif score <= 55:
            return "yellow_low"
        elif score <= 70:
            return "yellow_high"
        elif score <= 85:
            return "red_low"
        else:
            return "red_high"
    return "unknown"


def _get_recommendations_by_risk(condition: str, band: str) -> Dict[str, List[str]]:
    """Get categorized recommendations based on disease and risk level"""
    condition = condition.lower()
    
    # Map granular bands to main categories for display
    main_band = band
    if band.startswith("green"):
        main_band = "green"
    elif band.startswith("yellow"):
        main_band = "yellow"
    elif band.startswith("red"):
        main_band = "red"
    
    if band in ["green_low", "green_high"]:
        # Low Risk Recommendations
        base = {
            "lifestyle": [
                "Maintain healthy sleep habits (7-9 hours per night)",
                "Practice stress management techniques like meditation or yoga",
                "Stay socially active and maintain mental wellness",
                "Avoid smoking and limit alcohol consumption"
            ],
            "diet": [
                "Eat a balanced diet rich in vegetables, fruits, and whole grains",
                "Limit processed foods and added sugars",
                "Stay well-hydrated (8 glasses of water daily)",
                "Control portion sizes and maintain healthy weight"
            ],
            "exercise": [
                "Aim for 150 minutes of moderate exercise per week",
                "Include both cardio and strength training",
                "Take regular breaks from sitting every hour",
                "Find activities you enjoy to stay consistent"
            ],
            "monitoring": [
                "Schedule annual health check-ups",
                "Track your weight and vital signs monthly",
                "Keep a health journal to note any changes"
            ],
            "medical": [
                "Continue preventive care with your doctor",
                "Stay up to date with recommended screenings"
            ]
        }
        
        # Add condition-specific recommendations
        if condition == "diabetes":
            base["diet"].extend(["Choose low-glycemic index foods", "Limit refined carbohydrates and sugary beverages"])
            base["monitoring"].append("Check fasting glucose every 6-12 months")
        elif condition == "heart":
            base["diet"].extend(["Follow a heart-healthy diet (Mediterranean or DASH)", "Limit saturated fats and sodium"])
            base["monitoring"].append("Monitor blood pressure regularly")
            base["exercise"].append("Include cardio exercises like walking, swimming, or cycling")
        elif condition == "kidney":
            base["diet"].extend(["Moderate protein intake", "Limit sodium and potassium-rich foods"])
            base["monitoring"].append("Annual kidney function tests (eGFR)")
            
    elif band in ["yellow_low", "yellow_high"]:
        # Moderate Risk Recommendations
        base = {
            "lifestyle": [
                "Make lifestyle modifications a priority",
                "Reduce stress through relaxation techniques",
                "Ensure adequate sleep and rest",
                "Quit smoking immediately if applicable",
                "Limit alcohol to moderate levels or avoid completely"
            ],
            "diet": [
                "Work with a nutritionist for personalized meal planning",
                "Significantly reduce processed foods and fast food",
                "Monitor calorie intake to achieve/maintain healthy weight",
                "Increase fiber intake through vegetables and whole grains"
            ],
            "exercise": [
                "Gradually increase physical activity with doctor's approval",
                "Start with 30 minutes of moderate activity 5 days/week",
                "Consider supervised exercise programs",
                "Avoid sudden strenuous activities"
            ],
            "monitoring": [
                "Schedule medical consultation within 2-4 weeks",
                "Track symptoms, weight, and vital signs weekly",
                "Keep a detailed health diary",
                "Set up regular follow-up appointments"
            ],
            "medical": [
                "Consult your primary care physician for comprehensive evaluation",
                "Discuss preventive medication if recommended",
                "Follow prescribed treatment plans carefully"
            ]
        }
        
        # Add condition-specific recommendations
        if condition == "diabetes":
            base["diet"].extend(["Strictly control carbohydrate portions", "Avoid sugary snacks and beverages"])
            base["monitoring"].extend(["Consider HbA1c test", "Monitor blood glucose levels regularly"])
            base["medical"].append("Consider referral to endocrinologist or dietician")
        elif condition == "heart":
            base["diet"].extend(["Follow strict low-sodium diet (<2000mg/day)", "Reduce cholesterol and saturated fat intake"])
            base["monitoring"].extend(["Check blood pressure daily", "Get lipid profile test"])
            base["medical"].extend(["Consult cardiologist for evaluation", "Consider ECG and stress test"])
        elif condition == "kidney":
            base["diet"].extend(["Limit protein intake as advised", "Restrict phosphorus and potassium"])
            base["monitoring"].extend(["Regular urine albumin/creatinine ratio tests", "Monitor kidney function closely"])
            base["medical"].append("Schedule nephrology consultation")
            
    elif band in ["red_low", "red_high"]:
        # High Risk Recommendations
        base = {
            "lifestyle": [
                "Avoid strenuous physical or mental stress",
                "Ensure someone is available to assist you",
                "Keep emergency contacts readily accessible",
                "Do not ignore any warning symptoms"
            ],
            "diet": [
                "Follow strict dietary restrictions as prescribed",
                "Avoid foods that worsen your condition",
                "Work closely with a registered dietician",
                "Stay hydrated unless fluid restriction advised"
            ],
            "exercise": [
                "Avoid strenuous exercise until medical clearance",
                "Only light activities as approved by doctor",
                "Rest adequately and avoid overexertion"
            ],
            "monitoring": [
                "Monitor vital signs daily or as directed",
                "Keep detailed log of symptoms and readings",
                "Watch for emergency warning signs",
                "Do not self-medicate - consult doctor for any medication"
            ],
            "medical": [
                "Seek immediate medical attention",
                "Schedule urgent specialist consultation",
                "Follow treatment plan strictly",
                "Consider emergency care if symptoms worsen",
                "Have all medical records and medications list ready"
            ]
        }
        
        # Add condition-specific urgent recommendations
        if condition == "diabetes":
            base["monitoring"].extend(["Check blood glucose frequently", "Watch for signs of hyper/hypoglycemia"])
            base["medical"].extend(["Urgent endocrinology review required", "Discuss insulin or medication adjustment"])
        elif condition == "heart":
            base["monitoring"].append("Seek immediate ER if chest pain, shortness of breath, or dizziness occurs")
            base["medical"].extend(["Urgent cardiology consultation required", "May need cardiac catheterization or advanced imaging"])
        elif condition == "kidney":
            base["monitoring"].append("Watch for swelling, decreased urination, or severe fatigue")
            base["medical"].extend(["Urgent nephrology evaluation needed", "May require dialysis or advanced kidney care"])
    
    else:
        # Fallback for unknown bands
        base = {
            "lifestyle": ["Maintain healthy lifestyle habits"],
            "diet": ["Eat a balanced, nutritious diet"],
            "exercise": ["Stay physically active as appropriate"],
            "monitoring": ["Monitor your health regularly"],
            "medical": ["Consult with healthcare professionals"]
        }
    
    return base


def generate_recommendations(condition: str, risk_score_0_100: float, config_path: str | None = None) -> Dict[str, Any]:
    """Generate comprehensive categorized recommendations based on disease and risk level"""
    band = risk_band(risk_score_0_100, config_path=config_path)
    
    # Get categorized recommendations
    recommendations = _get_recommendations_by_risk(condition, band)
    
    # Add intensity/urgency markers based on granular band
    if band == "green_low":
        recommendations["lifestyle"].insert(0, "✅ Excellent health indicators - maintain current habits")
    elif band == "green_high":
        recommendations["lifestyle"].insert(0, "⚠️ Good health but some risk factors detected - focus on prevention")
    elif band == "yellow_low":
        recommendations["medical"].insert(0, "⚡ Moderate risk detected - schedule medical consultation within 3-4 weeks")
    elif band == "yellow_high":
        recommendations["medical"].insert(0, "⚡ Elevated risk - schedule medical consultation within 1-2 weeks")
    elif band == "red_low":
        recommendations["medical"].insert(0, "🚨 High risk detected - seek medical attention within 3-5 days")
    elif band == "red_high":
        recommendations["medical"].insert(0, "🚨 CRITICAL RISK - Seek immediate medical attention (within 24-48 hours)")
    
    # Determine zone name with score context
    score = float(risk_score_0_100)
    if band.startswith("green"):
        zone_name = f"Green Zone (Low Risk - {score:.1f}%)"
    elif band.startswith("yellow"):
        zone_name = f"Yellow Zone (Moderate Risk - {score:.1f}%)"
    elif band.startswith("red"):
        zone_name = f"Red Zone (High Risk - {score:.1f}%)"
    else:
        zone_name = "Unknown Zone"
    
    return {
        "disease": condition,
        "risk_score": score,
        "zone": zone_name,
        "risk_level": band,  # Include granular band for reference
        "recommendations": recommendations,
    }


