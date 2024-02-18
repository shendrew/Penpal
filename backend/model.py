import tensorflow as tf
import numpy as np

model = tf.keras.Sequential([
    # Reshape input images to (28, 28, 1)
    tf.keras.layers.Reshape((28, 28, 1), input_shape=(28, 28)),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu',
                           input_shape=(28, 28, 1)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    # 62 classes for multiclass classification
    tf.keras.layers.Dense(62, activation='softmax')
])

model.load_weights("../emnist_model.h5")

print(model.predict(np.random.rand(1, 28, 28)))