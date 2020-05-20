import os
import configparser

import wall_paper_bot
import flicker_photo_producer
import dd_logo_image_processor


def get_default_cfg():
    config = configparser.ConfigParser()
    config['bot'] = {
        "token": "1150307397:AAG5l_dSXdgUq_zfTso1NeXufOuErHDurVA"
    }
    config['photo_producer'] = {
        'api_key': 'd7d5ad87e6400d181f7147d4a5cd7227',
        'api_secret': '4374c55a7294c650',
        'tag': 'industrial'
    }
    config['DDLogoImageProcessor'] = {
        'height_factor': 0.2,
        'width_factor': 0.6,
        'filling_colour': '180, 180, 180, 180'
    }
    return config


def get_config(path):
    """
    Returns the config object
    """
    if not os.path.exists(path):
        return get_default_cfg()

    _config = configparser.ConfigParser()
    _config.read(path)
    return _config


if __name__ == '__main__':
    config = get_config('config.ini')
    photo_producer = flicker_photo_producer.FlickrPhotoProducer(dict(config.items('photo_producer')))
    photo_processors = [dd_logo_image_processor.DDLogoImageProcessor(dict(config.items('DDLogoImageProcessor')))]
    bot = wall_paper_bot.WallPaperBot(
        dict(config.items('bot')),
        photo_producer=photo_producer,
        photo_processors=photo_processors
    )
    bot.run_bot()