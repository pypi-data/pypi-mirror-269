from PIL import Image
from pathlib import Path
import imgtfs


def test(transform: imgtfs.GrayTransform, img_path: str = "images/lena.jpg"):
    image = Image.open(img_path)
    image = transform(image)
    image.show()


if __name__ == "__main__":
    transform = imgtfs.GrayGammaAutoTransform()
    test(
        transform,
    )
