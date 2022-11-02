# Part 1 - Building the CNN

# Importing the Keras libraries and packages
import os
import pickle
import time
from datetime import datetime

import mlfoundry
from keras.callbacks import Callback
from keras.layers import Conv2D, Dense, Flatten, MaxPooling2D
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator

client = mlfoundry.get_client(
    tracking_uri="https://app.develop.truefoundry.tech/",
    api_key="djE6dHJ1ZWZvdW5kcnk6Y2hhbmFreWF2a2Fwb29yOjdkMDg0MA==",
)
run = client.create_run(
    project_name="cat-and-dog-classifier-1",
    run_name=f"train-{datetime.now().strftime('%m-%d-%Y')}",
)


class MetricsLogCallback(Callback):
    def on_epoch_end(self, epoch, logs=None):
        run.log_metrics(logs, epoch)


# Initialising the CNN
classifier = Sequential()

# Step 1 - Convolution
classifier.add(Conv2D(32, (3, 3), input_shape=(200, 200, 3), activation="relu"))

# Step 2 - Pooling
classifier.add(MaxPooling2D(pool_size=(2, 2)))

# Adding a second convolutional layer
classifier.add(Conv2D(32, (3, 3), activation="relu"))
classifier.add(MaxPooling2D(pool_size=(2, 2)))

# Step 3 - Flattening
classifier.add(Flatten())

# Step 4 - Full connection
classifier.add(Dense(units=128, activation="relu"))
classifier.add(Dense(units=1, activation="sigmoid"))

batch_size = 32
epochs = 10

run.log_params({"batch_size": batch_size, "epochs": epochs})

# Compiling the CNN
classifier.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# Part 2 - Fitting the CNN to the images

train_datagen = ImageDataGenerator(
    rescale=1.0 / 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale=1.0 / 255)

training_set = train_datagen.flow_from_directory(
    "training_set", target_size=(200, 200), batch_size=batch_size, class_mode="binary"
)

test_set = test_datagen.flow_from_directory(
    "test_set", target_size=(200, 200), batch_size=batch_size, class_mode="binary"
)

classifier.fit_generator(
    training_set,
    steps_per_epoch=len(training_set),
    epochs=epochs,
    validation_data=test_set,
    validation_steps=len(test_set),
    callbacks=[MetricsLogCallback()],
)

_, acc = classifier.evaluate_generator(test_set, steps=len(test_set), verbose=0)


model_version = run.log_model(
    name="dog-cat-classifier",
    model=classifier,
    framework="keras",
    description="Model used for cat and dog classification",
)

print(run.run_id)

print(f"Logged model: {model_version.fqn}")
