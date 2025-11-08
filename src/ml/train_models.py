import pandas as pd
import numpy as np
import joblib
import os
import warnings
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, confusion_matrix, 
                             classification_report)
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import json

warnings.filterwarnings('ignore')

def clean_data(df, target_column, model_name):
    """Clean and preprocess data"""
    print(f"   � Original shape: {df.shape}")
    
    # Handle missing values
    if df.isnull().sum().sum() > 0:
        print(f"   🔧 Handling {df.isnull().sum().sum()} missing values...")
        # For numeric columns, fill with median
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].median(), inplace=True)
        
        # For categorical columns, fill with mode
        cat_cols = df.select_dtypes(include=['object']).columns
        for col in cat_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].mode()[0], inplace=True)
    
    # Clean target column (fix the kidney dataset issue)
    if model_name == 'kidney':
        df[target_column] = df[target_column].str.strip()  # Remove whitespace/tabs
        print(f"   ✓ Cleaned target column")
    
    # Encode categorical columns
    label_encoders = {}
    for col in df.columns:
        if df[col].dtype == 'object':
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            label_encoders[col] = le
    
    print(f"   ✓ Cleaned shape: {df.shape}")
    return df, label_encoders

def remove_outliers(X, y, contamination=0.05):
    """Remove outliers using Isolation Forest"""
    from sklearn.ensemble import IsolationForest
    iso = IsolationForest(contamination=contamination, random_state=42)
    outliers = iso.fit_predict(X)
    
    # Keep only inliers (outliers == 1, inliers == -1)
    mask = outliers == 1
    return X[mask], y[mask]

def create_ensemble_model(X_train, y_train):
    """Create ensemble model with multiple algorithms"""
    
    # Individual models with optimized parameters
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    xgb = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric='logloss'
    )
    
    lgbm = LGBMClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        num_leaves=31,
        random_state=42,
        verbose=-1
    )
    
    gb = GradientBoostingClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    )
    
    # Voting classifier (soft voting for probabilities)
    ensemble = VotingClassifier(
        estimators=[
            ('rf', rf),
            ('xgb', xgb),
            ('lgbm', lgbm),
            ('gb', gb)
        ],
        voting='soft',
        n_jobs=-1
    )
    
    return ensemble

def evaluate_model(model, X_test, y_test, model_name):
    """Comprehensive model evaluation"""
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
        'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
        'f1_score': f1_score(y_test, y_pred, average='weighted', zero_division=0)
    }
    
    if y_pred_proba is not None:
        try:
            metrics['roc_auc'] = roc_auc_score(y_test, y_pred_proba)
        except:
            metrics['roc_auc'] = 0.0
    
    print(f"\n   📊 Model Evaluation:")
    print(f"      Accuracy:  {metrics['accuracy']*100:.2f}%")
    print(f"      Precision: {metrics['precision']*100:.2f}%")
    print(f"      Recall:    {metrics['recall']*100:.2f}%")
    print(f"      F1-Score:  {metrics['f1_score']*100:.2f}%")
    if 'roc_auc' in metrics and metrics['roc_auc'] > 0:
        print(f"      ROC-AUC:   {metrics['roc_auc']*100:.2f}%")
    
    return metrics

def train_and_save_model(csv_path, target_column, model_name, use_ensemble=True, remove_outliers_flag=False):
    """
    Enhanced model training with multiple improvements:
    - Data cleaning and preprocessing
    - Outlier removal (optional)
    - Feature scaling
    - Ensemble modeling (RF, XGBoost, LightGBM, GradientBoosting)
    - Cross-validation
    - Comprehensive evaluation metrics
    """
    print(f"\n{'='*60}")
    print(f"🔹 Training {model_name.upper()} Model")
    print(f"{'='*60}")
    
    # Load data
    df = pd.read_csv(csv_path)
    
    # Clean data
    df, label_encoders = clean_data(df, target_column, model_name)
    
    # Prepare features and target
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    print(f"   📈 Class distribution:")
    print(f"      {y.value_counts().to_dict()}")
    
    # Split data with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   ✓ Train: {len(X_train)}, Test: {len(X_test)}")
    
    # Remove outliers (optional)
    if remove_outliers_flag:
        print(f"   🔍 Removing outliers...")
        X_train, y_train = remove_outliers(X_train.values, y_train.values)
        print(f"   ✓ After outlier removal: {len(X_train)} samples")
    
    # Feature scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    print(f"   🤖 Training {'ensemble' if use_ensemble else 'single'} model...")
    
    if use_ensemble:
        model = create_ensemble_model(X_train_scaled, y_train)
    else:
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
    
    model.fit(X_train_scaled, y_train)
    print(f"   ✅ Training complete!")
    
    # Cross-validation
    print(f"\n   🔄 Cross-validation (5-fold)...")
    cv_scores = cross_val_score(
        model, X_train_scaled, y_train, 
        cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
        scoring='accuracy',
        n_jobs=-1
    )
    print(f"      CV Accuracy: {cv_scores.mean()*100:.2f}% (+/- {cv_scores.std()*2*100:.2f}%)")
    
    # Evaluate on test set
    metrics = evaluate_model(model, X_test_scaled, y_test, model_name)
    
    # Save models and metadata
    os.makedirs("models/saved_models", exist_ok=True)
    model_path = f"models/saved_models/{model_name}_model.joblib"
    scaler_path = f"models/saved_models/{model_name}_scaler.joblib"
    metadata_path = f"models/saved_models/{model_name}_metadata.json"
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    
    # Save metadata
    metadata = {
        'model_name': model_name,
        'model_type': 'Ensemble (RF+XGB+LGBM+GB)' if use_ensemble else 'RandomForest',
        'features': list(X.columns),
        'n_features': len(X.columns),
        'n_samples_train': len(X_train),
        'n_samples_test': len(X_test),
        'metrics': metrics,
        'cv_scores': {
            'mean': float(cv_scores.mean()),
            'std': float(cv_scores.std())
        }
    }
    
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n   💾 Saved:")
    print(f"      Model:    {os.path.basename(model_path)}")
    print(f"      Scaler:   {os.path.basename(scaler_path)}")
    print(f"      Metadata: {os.path.basename(metadata_path)}")
    
    return model, scaler, metrics

if __name__ == "__main__":
    print("\n🏥 Smart Patient Health Assistant - Model Training")
    print("=" * 60)
    print("Training improved ML models with:")
    print("  ✓ Data cleaning and preprocessing")
    print("  ✓ Ensemble learning (RF + XGBoost + LightGBM + GB)")
    print("  ✓ Cross-validation")
    print("  ✓ Comprehensive evaluation")
    print("=" * 60)
    
    # Train all models with ensemble approach
    try:
        train_and_save_model(
            "data/raw/diabetes.csv", 
            "Outcome", 
            "diabetes",
            use_ensemble=True,
            remove_outliers_flag=False
        )
    except Exception as e:
        print(f"❌ Error training diabetes model: {e}")
    
    try:
        train_and_save_model(
            "data/raw/heart.csv", 
            "target", 
            "heart",
            use_ensemble=True,
            remove_outliers_flag=False
        )
    except Exception as e:
        print(f"❌ Error training heart model: {e}")
    
    try:
        train_and_save_model(
            "data/raw/kidney.csv", 
            "classification", 
            "kidney",
            use_ensemble=True,
            remove_outliers_flag=False
        )
    except Exception as e:
        print(f"❌ Error training kidney model: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Model training complete!")
    print("=" * 60)
