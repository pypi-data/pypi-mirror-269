import cv2
import numpy as np
from PIL import Image
from .base import ImageTransform

__all__ = [
    "GrayTransform",
    "GrayLogTransform",
    "GrayGammaTransform",
    "GrayGammaAutoTransform",
    "GrayHETransform",
    "GrayCLAHETransform",
    "GrayMeanStdTransform",
]

epsilon = 1e-8

class GrayTransform(ImageTransform):
    def __init__(self) -> None:
        super().__init__()

    def image_to_numpy(self, image: Image.Image):
        image = image.convert("L")
        image = np.array(image, dtype=np.uint8)
        image = cv2.normalize(image, None, 0.0, 1.0, cv2.NORM_MINMAX, dtype=cv2.CV_32FC1)
        image = np.clip(image, 0.0, 1.0)
        return image

    def numpy_to_image(self, image: np.ndarray) -> Image.Image:
        image = cv2.normalize(
            image * 255, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8UC1
        )
        return Image.fromarray(image)

    def __call__(self, image: Image.Image) -> Image.Image:
        image = self.image_to_numpy(image)
        image = self.core(image)
        return self.numpy_to_image(image)

    def core(self, image: np.ndarray) -> np.ndarray:
        return image


class GrayLogTransform(GrayTransform):
    def __init__(self, value: float = 1.0):
        super().__init__()
        self.value = value

    def core(self, image: np.ndarray) -> np.ndarray:
        return np.log(1.0 + self.value * image) / np.log(1.0 + self.value)


class GrayGammaTransform(GrayTransform):
    def __init__(self, gamma: float = 1.0):
        super().__init__()
        self.gamma = gamma

    def core(self, image: np.ndarray) -> np.ndarray:
        return np.power(image, self.gamma)


class GrayGammaAutoTransform(GrayTransform):
    def __init__(self) -> None:
        super().__init__()

    def core(self, image: np.ndarray) -> np.ndarray:
        mean = np.mean(image)
        gamma = np.log(0.5) / np.log(mean+epsilon)
        return np.power(image, gamma)


class GrayHETransform(GrayTransform):
    def __init__(self) -> None:
        super().__init__()

    def core(self, image: np.ndarray) -> np.ndarray:
        return cv2.equalizeHist(image)


class GrayCLAHETransform(GrayTransform):
    def __init__(
        self, clipLimit: float = 4.0, tileGridSize: tuple[int, int] = (12, 12)
    ):
        super().__init__()
        self.clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)

    def image_to_numpy(self, image: Image.Image):
        image = image.convert("L")
        image = np.array(image, dtype=np.uint8)
        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        return image

    def numpy_to_image(self, image: np.ndarray) -> Image.Image:
        return Image.fromarray(image)

    def core(self, image: np.ndarray) -> np.ndarray:
        return self.clahe.apply(image)


class GrayMeanStdTransform(GrayTransform):
    def __init__(self, mean: float = 127, std: float = 32) -> None:
        super().__init__()
        self.mean = mean
        self.std = std

    def numpy_to_image(self, image: np.ndarray) -> Image.Image:
        image = image.clip(0.0, 255.0)
        image = image.astype(np.uint8)
        return Image.fromarray(image)

    def core(self, image: np.ndarray) -> np.ndarray:
        mean = np.mean(image)
        std = np.std(image)
        if std==0.0:
            std = epsilon
        image = (image - mean) / std
        image = image * self.std + self.mean
        return image
