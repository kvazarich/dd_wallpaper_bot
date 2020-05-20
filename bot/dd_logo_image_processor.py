import io

from PIL import Image


class DDLogoImageProcessor:
    def __init__(self, cfg):
        self.height_factor = float(cfg.get('height_factor'))
        self.width_factor = float(cfg.get('width_factor'))
        self.filling_colour = tuple(int(num) for num in cfg.get('filling_colour').split(', '))

    def process(self, image, **kwargs):
        image = Image.open(image)
        logo = Image.open('logo.png')
        logo = logo.convert('RGBA')
        logo = logo.resize(self._get_new_logo_size(image.size, logo.size), resample=Image.NEAREST)
        overlay = Image.new('RGBA', (image.size[0], logo.size[1]), self.filling_colour)
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
            logo_size[0]/(image_size[0] * self.width_factor),
            logo_size[1]/(image_size[1] * self.height_factor)
        )
        return int(logo_size[0] // factor), int(logo_size[1] // factor)
