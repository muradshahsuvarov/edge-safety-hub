from ml_model import predict

def analyze_data(data):
    if data.sensor_type == "gas" and data.value > 5.0:
        return "HIGH GAS LEAK RISK"
    if data.sensor_type == "motion" and data.value == 0:
        return "MAN DOWN DETECTED"
    return "SAFE"
