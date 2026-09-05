
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def train_price_forecaster():
    """
    Trains a lightweight Random Forest model to predict market price spread multipliers
    based on synthetic feature inputs (renewable penetration, grid demand, and volatility).
    """
    np.random.seed(42)
    # Synthetic training data: [renewable_penetration, demand_index, volatility_index]
    X_train = np.random.rand(200, 3)
    y_train = 1.0 + 0.3 * X_train[:, 0] - 0.2 * X_train[:, 1] + 0.4 * X_train[:, 2] + np.random.normal(0, 0.05, 200)
    
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    return model

def predict_market_multiplier(renewable_factor=0.5, demand_factor=0.5, volatility_factor=0.5):
    model = train_price_forecaster()
    features = np.array([[renewable_factor, demand_factor, volatility_factor]])
    predicted_multiplier = float(model.predict(features)[0])
    return round(max(0.5, min(2.0, predicted_multiplier)), 2)
