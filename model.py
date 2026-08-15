import numpy as np
import pandas as pd
import random

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import StandardScaler
import joblib

# ==================================
# DATASET DIGITAL TWIN V2
# ==================================

data = []

for i in range(300):

    suhu_udara = random.uniform(24, 36)
    kelembapan_udara = random.uniform(60, 95)
    curah_hujan = random.uniform(20, 200)
    cahaya = random.uniform(200, 1200)
    angin = random.uniform(0, 15)

    soil_moisture = random.uniform(20, 90)
    ph = random.uniform(4.5, 7.5)
    npk = random.uniform(1, 10)
    soil_temp = random.uniform(20, 35)
    water_level = random.uniform(0, 20)

    ndvi = random.uniform(0.2, 1.0)
    hst = random.uniform(1, 120)
    varietas = random.randint(1, 5)

    score = 0

    if kelembapan_udara > 85:
        score += 1

    if curah_hujan > 130:
        score += 1

    if ndvi < 0.5:
        score += 1

    if soil_moisture > 75:
        score += 1

    if ph < 5.2 or ph > 6.8:
        score += 1

    if score >= 4:
        label = 2
    elif score >= 2:
        label = 1
    else:
        label = 0

    data.append([
        suhu_udara,
        kelembapan_udara,
        curah_hujan,
        cahaya,
        angin,

        soil_moisture,
        ph,
        npk,
        soil_temp,
        water_level,

        ndvi,
        hst,
        varietas,

        label
    ])

columns = [
    "suhu_udara",
    "kelembapan_udara",
    "curah_hujan",
    "cahaya",
    "angin",

    "soil_moisture",
    "ph",
    "npk",
    "soil_temp",
    "water_level",

    "ndvi",
    "hst",
    "varietas",

    "label"
]

df = pd.DataFrame(data, columns=columns)

# ==================================
# FEATURE & LABEL
# ==================================

X = df.drop("label", axis=1)
y = df["label"]

# ==================================
# SCALER
# ==================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

joblib.dump(scaler, "scaler.pkl")

# ==================================
# MODEL AI
# ==================================

model = Sequential([
    Dense(64, activation='relu', input_shape=(13,)),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(3, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(
    X_scaled,
    y,
    epochs=300,
    verbose=1
)

# ==================================
# SAVE MODEL
# ==================================

model.save("model.h5")

print("")
print("===================================")
print("AGRITWIN AI V2 BERHASIL DILATIH")
print("Dataset :", len(df))
print("Feature :", X.shape[1])
print("===================================")