import os
from PIL import Image

DATASET = "datasets/train"

print("=" * 50)
print("VERIFYING DATASET")
print("=" * 50)

for folder in os.listdir(DATASET):

    folder_path = os.path.join(DATASET, folder)

    if os.path.isdir(folder_path):

        images = os.listdir(folder_path)

        print(f"\nClass : {folder}")
        print(f"Images : {len(images)}")

        count = 0

        for image in images[:5]:

            path = os.path.join(folder_path, image)

            try:

                img = Image.open(path)

                print(image)
                print("Size :", img.size)
                print("Mode :", img.mode)

            except:

                print("Corrupted :", image)

            count += 1

print("\nVerification Complete.")