import tensorflow as tf
from tensorflow.keras.models import load_model

model = load_model("model.h5")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open("model.tflite", "wb") as f:
    f.write(tflite_model)

print("Selesai! model.tflite udah dibuat.")