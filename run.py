import os
import configparser

import wall_paper_bot
import flicker_photo_producer


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
    bot = wall_paper_bot.WallPaperBot(dict(config.items('bot')), photo_producer=photo_producer)
    bot.run_bot()