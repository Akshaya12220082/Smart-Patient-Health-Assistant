import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def train_and_save_model(csv_path, target_column, model_name):
    print(f"\n🔹 Training {model_name} model from {os.path.abspath(csv_path)}")
    
    df = pd.read_csv(csv_path)
    
    # Encode non-numeric columns
    for col in df.columns:
        if df[col].dtype == 'object':
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))

    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train_scaled, y_train)

    # Evaluate
    accuracy = accuracy_score(y_test, model.predict(X_test_scaled))
    print(f"✅ {model_name} Model Accuracy: {accuracy * 100:.2f}%")

    # Save
    os.makedirs("models/saved_models", exist_ok=True)
    model_path = f"models/saved_models/{model_name}_model.joblib"
    scaler_path = f"models/saved_models/{model_name}_scaler.joblib"

    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    
    print(f"💾 Saved model -> {os.path.abspath(model_path)}")

if __name__ == "__main__":
    train_and_save_model("data/raw/diabetes.csv", "Outcome", "diabetes")
    train_and_save_model("data/raw/heart.csv", "target", "heart")
    train_and_save_model("data/raw/kidney.csv", "classification", "kidney")
