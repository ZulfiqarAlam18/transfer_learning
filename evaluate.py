from pathlib import Path

import numpy as np
import tensorflow as tf
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
)
import matplotlib.pyplot as plt


MODEL_PATH = Path(
    "models/best_model.keras"
)

TEST_DIR = Path(
    "data_split/test"
)

IMAGE_SIZE = (
    160,
    160,
)

BATCH_SIZE = 16


def main():

    print("=" * 70)
    print("MODEL EVALUATION")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # Load model
    # -------------------------------------------------------------------------

    print(
        f"\nLoading model:\n{MODEL_PATH}"
    )

    model = tf.keras.models.load_model(
        MODEL_PATH
    )

    # -------------------------------------------------------------------------
    # Load test dataset
    # -------------------------------------------------------------------------

    test_ds = (
        tf.keras.utils.image_dataset_from_directory(
            TEST_DIR,
            image_size=IMAGE_SIZE,
            batch_size=BATCH_SIZE,
            shuffle=False,
        )
    )

    class_names = test_ds.class_names

    print("\nClasses:")

    for index, name in enumerate(
        class_names
    ):
        print(
            f"  {index}: {name}"
        )

    # -------------------------------------------------------------------------
    # Predictions
    # -------------------------------------------------------------------------

    y_true = []
    y_pred = []

    for images, labels in test_ds:

        predictions = model.predict(
            images,
            verbose=0,
        )

        predicted_classes = np.argmax(
            predictions,
            axis=1,
        )

        y_true.extend(
            labels.numpy()
        )

        y_pred.extend(
            predicted_classes
        )

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    # -------------------------------------------------------------------------
    # Accuracy
    # -------------------------------------------------------------------------

    accuracy = (
        np.mean(
            y_true == y_pred
        )
    )

    print("\n")
    print("=" * 70)
    print(
        f"TEST ACCURACY: {accuracy:.4f}"
    )
    print(
        f"CORRECT: "
        f"{np.sum(y_true == y_pred)} / "
        f"{len(y_true)}"
    )
    print("=" * 70)

    # -------------------------------------------------------------------------
    # Classification report
    # -------------------------------------------------------------------------

    print("\nCLASSIFICATION REPORT\n")

    print(
        classification_report(
            y_true,
            y_pred,
            target_names=class_names,
            zero_division=0,
        )
    )

    # -------------------------------------------------------------------------
    # Confusion matrix
    # -------------------------------------------------------------------------

    cm = confusion_matrix(
        y_true,
        y_pred,
    )

    print("\nCONFUSION MATRIX\n")

    print(cm)

    # -------------------------------------------------------------------------
    # Plot confusion matrix
    # -------------------------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(8, 8)
    )

    image = ax.imshow(cm)

    ax.set_title(
        "Thumb Classifier Confusion Matrix"
    )

    ax.set_xlabel(
        "Predicted"
    )

    ax.set_ylabel(
        "Actual"
    )

    ax.set_xticks(
        range(len(class_names))
    )

    ax.set_yticks(
        range(len(class_names))
    )

    ax.set_xticklabels(
        class_names,
        rotation=45,
        ha="right",
    )

    ax.set_yticklabels(
        class_names
    )

    for i in range(
        len(class_names)
    ):
        for j in range(
            len(class_names)
        ):
            ax.text(
                j,
                i,
                cm[i, j],
                ha="center",
                va="center",
            )

    fig.colorbar(image)

    plt.tight_layout()

    output_path = Path(
        "models/confusion_matrix.png"
    )

    plt.savefig(
        output_path,
        dpi=150,
    )

    plt.show()

    print(
        f"\nConfusion matrix saved to:"
        f"\n{output_path.resolve()}"
    )


if __name__ == "__main__":
    main()