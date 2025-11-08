"""
Compare different ML algorithms for each disease
and select the best performing model
"""

import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import warnings

warnings.filterwarnings('ignore')

def load_and_preprocess(csv_path, target_column):
    """Load and preprocess data"""
    df = pd.read_csv(csv_path)
    
    # Handle missing values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)
    
    # Encode categorical
    for col in df.columns:
        if df[col].dtype == 'object':
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
    
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

def evaluate_models(X_train, X_test, y_train, y_test, disease_name):
    """Evaluate multiple models"""
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Define models
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
        'XGBoost': XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss'),
        'LightGBM': LGBMClassifier(n_estimators=100, random_state=42, verbose=-1),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'SVM': SVC(probability=True, random_state=42),
        'KNN': KNeighborsClassifier(n_neighbors=5),
        'Naive Bayes': GaussianNB()
    }
    
    results = []
    
    print(f"\n{'='*70}")
    print(f"Comparing Models for {disease_name.upper()}")
    print(f"{'='*70}\n")
    
    for name, model in models.items():
        print(f"Training {name}...", end=' ')
        
        try:
            # Train
            model.fit(X_train_scaled, y_train)
            
            # Predict
            y_pred = model.predict(X_test_scaled)
            y_pred_proba = model.predict_proba(X_test_scaled)[:, 1] if hasattr(model, 'predict_proba') else None
            
            # Metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
            recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
            
            try:
                roc_auc = roc_auc_score(y_test, y_pred_proba) if y_pred_proba is not None else 0
            except:
                roc_auc = 0
            
            # Cross-validation
            cv_scores = cross_val_score(
                model, X_train_scaled, y_train,
                cv=StratifiedKFold(5, shuffle=True, random_state=42),
                scoring='accuracy',
                n_jobs=-1
            )
            
            results.append({
                'Model': name,
                'Accuracy': accuracy,
                'Precision': precision,
                'Recall': recall,
                'F1-Score': f1,
                'ROC-AUC': roc_auc,
                'CV Mean': cv_scores.mean(),
                'CV Std': cv_scores.std()
            })
            
            print(f"✓ Acc: {accuracy*100:.2f}%")
            
        except Exception as e:
            print(f"✗ Error: {str(e)[:50]}")
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('Accuracy', ascending=False)
    
    print(f"\n{'='*70}")
    print("Results (sorted by accuracy):")
    print(f"{'='*70}\n")
    print(results_df.to_string(index=False))
    
    # Best model
    best_model = results_df.iloc[0]
    print(f"\n{'='*70}")
    print(f"🏆 Best Model: {best_model['Model']}")
    print(f"   Accuracy: {best_model['Accuracy']*100:.2f}%")
    print(f"   F1-Score: {best_model['F1-Score']*100:.2f}%")
    print(f"   CV Score: {best_model['CV Mean']*100:.2f}% (+/- {best_model['CV Std']*2*100:.2f}%)")
    print(f"{'='*70}\n")
    
    return results_df

if __name__ == "__main__":
    print("\n🔬 ML Model Comparison Tool")
    print("="*70)
    
    # Diabetes
    print("\n1️⃣  DIABETES DATASET")
    X_train, X_test, y_train, y_test = load_and_preprocess("data/raw/diabetes.csv", "Outcome")
    diabetes_results = evaluate_models(X_train, X_test, y_train, y_test, "Diabetes")
    
    # Heart
    print("\n2️⃣  HEART DISEASE DATASET")
    X_train, X_test, y_train, y_test = load_and_preprocess("data/raw/heart.csv", "target")
    heart_results = evaluate_models(X_train, X_test, y_train, y_test, "Heart Disease")
    
    # Kidney
    print("\n3️⃣  KIDNEY DISEASE DATASET")
    X_train, X_test, y_train, y_test = load_and_preprocess("data/raw/kidney.csv", "classification")
    kidney_results = evaluate_models(X_train, X_test, y_train, y_test, "Kidney Disease")
    
    print("\n✅ Comparison complete!")
