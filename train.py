from pathlib import Path

import tensorflow as tf


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

DATASET_DIR = Path("dataset_from_phone")
MODEL_DIR = Path("models")

IMAGE_SIZE = (160, 160)
BATCH_SIZE = 32
VALIDATION_SPLIT = 0.20
SEED = 123

EPOCHS_HEAD = 15
EPOCHS_FINE_TUNE = 10


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> None:
    print("=" * 70)
    print("Thumb Classifier Training")
    print("=" * 70)

    print(f"TensorFlow version: {tf.__version__}")

    print(
        "Available GPUs:",
        tf.config.list_physical_devices("GPU"),
    )

    if not DATASET_DIR.exists():
        raise FileNotFoundError(
            f"Dataset directory not found: {DATASET_DIR.resolve()}"
        )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # -------------------------------------------------------------------------
    # Load training data
    # -------------------------------------------------------------------------

    print("\nLoading training dataset...")

    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=VALIDATION_SPLIT,
        subset="training",
        seed=SEED,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=True,
    )

    print("\nLoading validation dataset...")

    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=VALIDATION_SPLIT,
        subset="validation",
        seed=SEED,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=True,
    )

    class_names = train_ds.class_names

    print("\nClasses:")
    for index, name in enumerate(class_names):
        print(f"  {index}: {name}")

    # -------------------------------------------------------------------------
    # Save labels
    # -------------------------------------------------------------------------

    labels_path = Path("labels.txt")

    labels_path.write_text(
        "\n".join(class_names),
        encoding="utf-8",
    )

    print(f"\nLabels saved to: {labels_path.resolve()}")

    # -------------------------------------------------------------------------
    # Optimize dataset pipeline
    # -------------------------------------------------------------------------

    autotune = tf.data.AUTOTUNE

    train_ds = train_ds.prefetch(
        buffer_size=autotune
    )

    val_ds = val_ds.prefetch(
        buffer_size=autotune
    )

    # -------------------------------------------------------------------------
    # Data augmentation
    # -------------------------------------------------------------------------

    augmentation = tf.keras.Sequential(
        [
            tf.keras.layers.RandomRotation(0.05),
            tf.keras.layers.RandomZoom(0.10),
            tf.keras.layers.RandomContrast(0.10),
            tf.keras.layers.RandomBrightness(0.10),
        ],
        name="augmentation",
    )

    # -------------------------------------------------------------------------
    # Pretrained MobileNetV3Small
    # -------------------------------------------------------------------------

    print("\nLoading MobileNetV3Small...")

    base_model = tf.keras.applications.MobileNetV3Small(
        input_shape=(
            IMAGE_SIZE[0],
            IMAGE_SIZE[1],
            3,
        ),
        include_top=False,
        weights="imagenet",
    )

    # Phase 1:
    # Freeze pretrained layers.
    base_model.trainable = False

    # -------------------------------------------------------------------------
    # Build classifier
    # -------------------------------------------------------------------------

    inputs = tf.keras.Input(
        shape=(
            IMAGE_SIZE[0],
            IMAGE_SIZE[1],
            3,
        )
    )

    x = augmentation(inputs)

    x = tf.keras.applications.mobilenet_v3.preprocess_input(x)

    x = base_model(
        x,
        training=False,
    )

    x = tf.keras.layers.GlobalAveragePooling2D()(x)

    x = tf.keras.layers.Dropout(0.2)(x)

    outputs = tf.keras.layers.Dense(
        len(class_names),
        activation="softmax",
    )(x)

    model = tf.keras.Model(
        inputs,
        outputs,
    )

    # -------------------------------------------------------------------------
    # Compile phase 1
    # -------------------------------------------------------------------------

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=1e-3,
        ),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    print("\nModel created.")

    model.summary()

    # -------------------------------------------------------------------------
    # Callbacks
    # -------------------------------------------------------------------------

    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        filepath=MODEL_DIR / "best_model.keras",
        monitor="val_accuracy",
        save_best_only=True,
        mode="max",
        verbose=1,
    )

    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=4,
        restore_best_weights=True,
        verbose=1,
    )

    # -------------------------------------------------------------------------
    # Phase 1 training
    # -------------------------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("PHASE 1: Training classifier head")
    print("=" * 70)

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS_HEAD,
        callbacks=[
            checkpoint,
            early_stopping,
        ],
    )

    # -------------------------------------------------------------------------
    # Phase 2: Fine tuning
    # -------------------------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("PHASE 2: Fine tuning")
    print("=" * 70)

    base_model.trainable = True

    # Keep most of MobileNet frozen.
    for layer in base_model.layers[:-20]:
        layer.trainable = False

    # Recompile with a much smaller learning rate.
    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=1e-5,
        ),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS_FINE_TUNE,
        callbacks=[
            checkpoint,
            early_stopping,
        ],
    )

    # -------------------------------------------------------------------------
    # Final save
    # -------------------------------------------------------------------------

    final_model_path = MODEL_DIR / "thumb_classifier.keras"

    model.save(
        final_model_path,
    )

    print("\n")
    print("=" * 70)
    print("Training complete")
    print("=" * 70)

    print(
        f"Final model: {final_model_path.resolve()}"
    )

    print(
        f"Labels: {labels_path.resolve()}"
    )


if __name__ == "__main__":
    main()