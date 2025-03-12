import pickle
import numpy as np

# Load pre-trained model
model = pickle.load(open("models/safety_model.pkl", "rb"))

def predict(data):
    X = np.array([[data.value]])  # Feature vector
    return model.predict(X)[0]
