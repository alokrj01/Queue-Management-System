import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib
import random

# ==========================================
# STEP 1: GENERATE FAKE TRAINING DATA
# ==========================================
# Imagine we tracked the queue for the last 30 days.
# Logic: More people ahead = Longer wait time.
print("Generating fake historical data...")

data = []
for _ in range(1000): # Generate 1000 records
    people_ahead = random.randint(0, 20) # 0 to 20 people waiting
    
    # Let's say 1 person takes roughly 5 minutes (approx 300 seconds)
    # But we add some random noise because real life is unpredictable
    base_time = people_ahead * 5 
    random_noise = random.randint(-5, 10) # +/- variation
    
    actual_wait_time = base_time + random_noise
    if actual_wait_time < 0: actual_wait_time = 0

    data.append([people_ahead, actual_wait_time])

# Convert to a DataFrame (Table)
df = pd.DataFrame(data, columns=['people_ahead', 'wait_time_minutes'])

# ==========================================
# STEP 2: TRAIN THE MODEL
# ==========================================
print("Training the AI Model...")

# X = Input (Features), y = Output (Prediction)
X = df[['people_ahead']]
y = df['wait_time_minutes']

# Create the Model (Linear Regression)
model = LinearRegression()
model.fit(X, y)

# ==========================================
# STEP 3: SAVE THE BRAIN
# ==========================================
# We save the model to a file so the API can use it later
joblib.dump(model, "wait_time_model.pkl")

print("✅ Model Trained Successfully!")
print(f"Test Prediction: If 5 people are waiting, wait time is approx: {model.predict([[5]])[0]:.1f} mins")