import os
import configparser

import wall_paper_bot
import flicker_photo_producer
import dd_logo_image_processor


def get_config(path):
    """
    Returns the config object
    """
    if not os.path.exists(path):
        raise FileNotFoundError('Не найден файл конфигурации {}'.format(path))

    _config = configparser.ConfigParser()
    _config.read(path)
    return _config


if __name__ == '__main__':
    config = get_config('config.ini')
    photo_producer = flicker_photo_producer.FlickrPhotoProducer(dict(config.items('photo_producer')))
    photo_processors = [dd_logo_image_processor.DDLogoImageProcessor()]
    bot = wall_paper_bot.WallPaperBot(dict(config.items('bot')), photo_producer=photo_producer, photo_processors=photo_processors)
    bot.run_bot()