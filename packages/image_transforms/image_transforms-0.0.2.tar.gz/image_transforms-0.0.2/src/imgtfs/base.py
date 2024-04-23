from PIL import Image

__all__ = ['ImageTransform']
class ImageTransform:
    def __call__(self, image: Image.Image) -> Image.Image:
        return image