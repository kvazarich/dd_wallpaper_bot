import io
import logging

from PIL import Image


class DDLogoImageProcessor:
    # соотношение высоты лого к высоте изображения
    HEIGHT_FACTOR = 0.2
    WIDTH_FACTOR = 0.6
    FILL_COLOUR = (180, 180, 180, 180)

    def process(self, image, **kwargs):
        image = Image.open(image)
        logo = Image.open('logo.png')
        logo = logo.convert('RGBA')
        logo = logo.resize(self._get_new_logo_size(image.size, logo.size), resample=Image.NEAREST)
        overlay = Image.new('RGBA', (image.size[0], logo.size[1]), self.FILL_COLOUR)
        image.paste(
            overlay,
            (
                0,
                image.size[1] - overlay.size[1]
            ),
            overlay
        )
        image.paste(
            logo,
            (
                (image.size[0] - logo.size[0]) // 2,
                image.size[1] - logo.size[1]
            ),
            logo
        )
        result = io.BytesIO()
        image.save(result, format=image.format)
        result.seek(0)
        return result

    def _get_new_logo_size(self, image_size, logo_size):
        factor = max(
            logo_size[0]/(image_size[0] * self.WIDTH_FACTOR),
            logo_size[1]/(image_size[1] * self.HEIGHT_FACTOR)
        )
        return int(logo_size[0] // factor), int(logo_size[1] // factor)
