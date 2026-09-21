from pathlib import Path
import random
import shutil


# SOURCE_DIR = Path("dataset")

SOURCE_DIR = Path("dataset_from_phone")

OUTPUT_DIR = Path("data_split")

CLASSES = [
    "thumb_fingerprint",
    "thumb_nail",
    "other_finger",
    "no_finger",
    "non_finger_object",
]

TRAIN_RATIO = 0.70
VALIDATION_RATIO = 0.15
TEST_RATIO = 0.15

SEED = 42


def main():
    random.seed(SEED)

    if abs(
        TRAIN_RATIO +
        VALIDATION_RATIO +
        TEST_RATIO -
        1.0
    ) > 0.001:
        raise ValueError(
            "Dataset ratios must total 1.0"
        )

    print("=" * 60)
    print("PREPARING DATASET")
    print("=" * 60)

    for class_name in CLASSES:
        source_class_dir = (
            SOURCE_DIR / class_name
        )

        images = list(
            source_class_dir.glob("*.jpg")
        )

        if not images:
            raise RuntimeError(
                f"No images found for {class_name}"
            )

        random.shuffle(images)

        total = len(images)

        train_count = int(
            total * TRAIN_RATIO
        )

        validation_count = int(
            total * VALIDATION_RATIO
        )

        train_images = images[
            :train_count
        ]

        validation_images = images[
            train_count:
            train_count + validation_count
        ]

        test_images = images[
            train_count + validation_count:
        ]

        split_data = {
            "train": train_images,
            "validation": validation_images,
            "test": test_images,
        }

        for split_name, split_images in split_data.items():

            destination_dir = (
                OUTPUT_DIR /
                split_name /
                class_name
            )

            destination_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            for image_path in split_images:

                destination_path = (
                    destination_dir /
                    image_path.name
                )

                shutil.copy2(
                    image_path,
                    destination_path,
                )

        print(
            f"{class_name}: "
            f"train={len(train_images)}, "
            f"validation={len(validation_images)}, "
            f"test={len(test_images)}"
        )

    print("\nDataset prepared.")
    print(
        f"Output: {OUTPUT_DIR.resolve()}"
    )


if __name__ == "__main__":
    main()