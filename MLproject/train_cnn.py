"""
Simple training scaffold for a skin disease CNN using a Kaggle-style folder layout:

data/skin/
    class_a/
        img1.jpg
        ...
    class_b/
        ...

This uses TensorFlow + Keras with MobileNetV2 transfer learning.
Adjust paths, image size, epochs, and batch size as needed.
"""

import json
import pathlib
import tensorflow as tf


def main():
    data_dir = pathlib.Path("data/skin")
    if not data_dir.exists():
        raise FileNotFoundError(
            "Dataset not found. Place your dataset under data/skin/<class_name>/image.jpg"
        )

    img_size = (224, 224)
    batch_size = 32
    val_split = 0.2
    seed = 1337

    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=val_split,
        subset="training",
        seed=seed,
        image_size=img_size,
        batch_size=batch_size,
    )
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=val_split,
        subset="validation",
        seed=seed,
        image_size=img_size,
        batch_size=batch_size,
    )

    class_names = train_ds.class_names
    num_classes = len(class_names)

    # Prefetch for performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

    base = tf.keras.applications.MobileNetV2(
        input_shape=img_size + (3,),
        include_top=False,
        weights="imagenet",
    )
    base.trainable = False  # freeze backbone for a quick start

    inputs = tf.keras.Input(shape=img_size + (3,))
    x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
    x = base(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dense(128, activation="relu")(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
    model = tf.keras.Model(inputs, outputs)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    model.fit(train_ds, validation_data=val_ds, epochs=5)

    # Save model and label map
    pathlib.Path("models").mkdir(exist_ok=True)
    model.save("models/skin_cnn.h5")
    with open("models/skin_cnn_labels.json", "w") as f:
        json.dump(class_names, f)

    print("Saved model to models/skin_cnn.h5 and labels to models/skin_cnn_labels.json")


if __name__ == "__main__":
    main()

