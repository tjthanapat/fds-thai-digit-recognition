from tensorflow import keras
from keras import layers
import numpy as np


base_model = keras.applications.EfficientNetV2B1(weights='imagenet', include_top=False, input_shape=(224, 224,3))

x = base_model.output
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(128, activation='relu')(x)
predictions = layers.Dense(10, activation='softmax')(x)

model = keras.models.Model(inputs=base_model.input, outputs=predictions)
model.load_weights('EfficientNetV2B1_weights.h5')

thai_digit = '๐๑๒๓๔๕๖๗๘๙'


def predict_digit(img):
    res = model.predict(np.array([img]))[0]
    digit = thai_digit[np.argmax(res)]
    return digit
