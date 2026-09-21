from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image


# =============================================================================
# CONFIGURATION
# =============================================================================

MODEL_PATH = Path(
    "models/best_model.keras"
)

TEST_DIR = Path(
    "test_images"
)

IMAGE_SIZE = (
    160,
    160,
)

# Supported test image formats.
SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


# ---------------------------------------------------------------------------
# OPTIONAL:
#
# Put the expected class for each image here.
#
# Leave the value as None if you only want the model's prediction.
#
# The key must match the filename without its extension.
# Example:
# i1.jpg   -> "i1"
# i2.webp  -> "i2"
# ---------------------------------------------------------------------------

EXPECTED_LABELS = {
    "i1": None,
    "i2": None,
    "i3": None,
   
}


# =============================================================================
# LOAD LABELS
# =============================================================================

def load_labels():
    labels_path = Path("labels.txt")

    if not labels_path.exists():
        raise FileNotFoundError(
            "labels.txt was not found."
        )

    labels = [
        line.strip()
        for line in labels_path.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    if not labels:
        raise RuntimeError(
            "labels.txt is empty."
        )

    return labels


# =============================================================================
# FIND TEST IMAGES
# =============================================================================

def find_test_images():
    if not TEST_DIR.exists():
        raise FileNotFoundError(
            f"Test directory not found: "
            f"{TEST_DIR.resolve()}"
        )

    image_paths = []

    for path in TEST_DIR.iterdir():

        if not path.is_file():
            continue

        # Convert extension to lowercase so that
        # .JPG, .PNG, .WEBP etc. are also supported.
        extension = path.suffix.lower()

        if extension in SUPPORTED_EXTENSIONS:
            image_paths.append(path)

    # Sort naturally by filename.
    image_paths.sort(
        key=lambda path: path.name.lower()
    )

    return image_paths


# =============================================================================
# PREDICT ONE IMAGE
# =============================================================================

def predict_image(
    model,
    image_path,
    labels,
):
    # PIL supports JPEG, PNG and WEBP when the
    # corresponding decoder is available.
    image = Image.open(
        image_path
    ).convert("RGB")

    # Same basic resizing used by training.
    image = image.resize(
        IMAGE_SIZE
    )

    image_array = np.asarray(
        image,
        dtype=np.float32,
    )

    image_array = np.expand_dims(
        image_array,
        axis=0,
    )

    predictions = model.predict(
        image_array,
        verbose=0,
    )[0]

    predicted_index = int(
        np.argmax(predictions)
    )

    predicted_label = labels[
        predicted_index
    ]

    confidence = float(
        predictions[predicted_index]
    )

    return (
        predicted_label,
        confidence,
        predictions,
    )


# =============================================================================
# MAIN
# =============================================================================

def main():

    print("=" * 70)
    print("MANUAL EXTERNAL IMAGE TEST")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # Load model
    # -------------------------------------------------------------------------

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )

    print(
        f"\nLoading model:"
        f"\n{MODEL_PATH}"
    )

    model = tf.keras.models.load_model(
        MODEL_PATH
    )

    # -------------------------------------------------------------------------
    # Load labels
    # -------------------------------------------------------------------------

    labels = load_labels()

    print("\nModel classes:")

    for index, label in enumerate(
        labels
    ):
        print(
            f"  {index}: {label}"
        )

    # -------------------------------------------------------------------------
    # Find test images
    # -------------------------------------------------------------------------

    image_paths = find_test_images()

    if not image_paths:
        raise RuntimeError(
            f"No supported images found in "
            f"{TEST_DIR}\n"
            f"Supported formats: "
            f"{', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    print(
        f"\nFound {len(image_paths)} "
        f"test images."
    )

    print(
        "Supported formats:"
        " JPG, JPEG, PNG, WEBP"
    )

    # -------------------------------------------------------------------------
    # Statistics
    # -------------------------------------------------------------------------

    total_with_expected = 0
    correct = 0

    # -------------------------------------------------------------------------
    # Test each image
    # -------------------------------------------------------------------------

    for image_path in image_paths:

        image_name = (
            image_path.stem
        )

        expected = EXPECTED_LABELS.get(
            image_name
        )

        try:
            (
                predicted_label,
                confidence,
                probabilities,
            ) = predict_image(
                model,
                image_path,
                labels,
            )

        except Exception as error:
            print("\n")
            print("-" * 70)
            print(
                f"ERROR: {image_path.name}"
            )
            print(
                f"Reason: {error}"
            )
            continue

        print("\n")
        print("-" * 70)

        print(
            f"IMAGE: {image_path.name}"
        )

        print(
            f"Format: "
            f"{image_path.suffix.lower()}"
        )

        print(
            f"Predicted: "
            f"{predicted_label}"
        )

        print(
            f"Confidence: "
            f"{confidence * 100:.2f}%"
        )

        # ---------------------------------------------------------------------
        # Expected label
        # ---------------------------------------------------------------------

        if expected is not None:

            total_with_expected += 1

            is_correct = (
                predicted_label ==
                expected
            )

            if is_correct:
                correct += 1

            print(
                f"Expected:  "
                f"{expected}"
            )

            print(
                f"Result:    "
                f"{'CORRECT' if is_correct else 'WRONG'}"
            )

        # ---------------------------------------------------------------------
        # Show all probabilities
        # ---------------------------------------------------------------------

        print("\nProbabilities:")

        ranked_indices = np.argsort(
            probabilities
        )[::-1]

        for index in ranked_indices:

            print(
                f"  {labels[index]:20s}"
                f" {probabilities[index] * 100:6.2f}%"
            )

    # -------------------------------------------------------------------------
    # Accuracy
    # -------------------------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    if total_with_expected > 0:

        accuracy = (
            correct /
            total_with_expected
        )

        print(
            f"Correct: "
            f"{correct}/{total_with_expected}"
        )

        print(
            f"Manual test accuracy: "
            f"{accuracy * 100:.2f}%"
        )

    else:

        print(
            "No expected labels were provided."
        )

        print(
            "Predictions were displayed, "
            "but accuracy was not calculated."
        )

    print("=" * 70)


if __name__ == "__main__":
    main()