import albumentations as A


augmentation = A.Compose([

    A.HorizontalFlip(p=0.5),

    A.Rotate(
        limit=10,
        p=0.5
    ),

    A.RandomBrightnessContrast(
        brightness_limit=0.2,
        contrast_limit=0.2,
        p=0.5
    ),

    A.GaussianBlur(
        blur_limit=(3, 5),
        p=0.15
    ),

    A.GaussNoise(
        std_range=(0.01, 0.05),
        p=0.15
    )
])