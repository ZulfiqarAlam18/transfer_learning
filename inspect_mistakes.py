from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image


MODEL_PATH = Path("models/best_model.keras")
TEST_DIR = Path("data_split/test")

IMAGE_SIZE = (160, 160)


def main():
    print("=" * 70)
    print("MISCLASSIFIED TEST IMAGES")
    print("=" * 70)

    model = tf.keras.models.load_model(
        MODEL_PATH
    )

    class_names = sorted(
        [
            directory.name
            for directory in TEST_DIR.iterdir()
            if directory.is_dir()
        ]
    )

    for actual_index, actual_class in enumerate(class_names):

        class_dir = TEST_DIR / actual_class

        for image_path in sorted(
            class_dir.glob("*.jpg")
        ):
            try:
                image = Image.open(
                    image_path
                ).convert("RGB")

                image = image.resize(
                    IMAGE_SIZE
                )

                image_array = np.array(
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

                confidence = float(
                    predictions[predicted_index]
                )

                predicted_class = (
                    class_names[predicted_index]
                )

                if (
                    predicted_index
                    != actual_index
                ):
                    print("\nMISCLASSIFIED")
                    print(
                        f"Image: {image_path}"
                    )
                    print(
                        f"Actual: {actual_class}"
                    )
                    print(
                        f"Predicted: "
                        f"{predicted_class}"
                    )
                    print(
                        f"Confidence: "
                        f"{confidence:.4f}"
                    )

                    print(
                        "\nAll probabilities:"
                    )

                    for index, name in enumerate(
                        class_names
                    ):
                        print(
                            f"  {name:20s} "
                            f"{predictions[index]:.4f}"
                        )

            except Exception as error:
                print(
                    f"Failed: {image_path}"
                )
                print(error)


if __name__ == "__main__":
    main()