from pathlib import Path

from PIL import Image


# DATASET_DIR = Path("dataset")
 
DATASET_DIR = Path("dataset_from_phone")

CLASSES = [
    "thumb_fingerprint",
    "thumb_nail",
    "other_finger",
    "no_finger",
    "non_finger_object",
]


def main():
    print("=" * 60)
    print("DATASET CHECK")
    print("=" * 60)

    total = 0

    for class_name in CLASSES:
        class_dir = DATASET_DIR / class_name

        images = list(class_dir.glob("*.jpg"))

        print(f"\nClass: {class_name}")
        print(f"Images: {len(images)}")

        if not images:
            print("WARNING: No images found!")
            continue

        dimensions = {}
        corrupted = 0

        for image_path in images:
            try:
                with Image.open(image_path) as image:
                    image.verify()

                with Image.open(image_path) as image:
                    size = image.size

                dimensions[size] = dimensions.get(size, 0) + 1

            except Exception as error:
                corrupted += 1

                print(
                    f"  CORRUPTED: {image_path.name}"
                    f" | {error}"
                )

        print("Dimensions:")

        for size, count in sorted(dimensions.items()):
            print(
                f"  {size}: {count}"
            )

        if corrupted:
            print(
                f"Corrupted: {corrupted}"
            )

        total += len(images)

    print("\n" + "=" * 60)
    print(f"TOTAL IMAGES: {total}")
    print("=" * 60)


if __name__ == "__main__":
    main()