## Тестовое задание

[Описание задачи](task.pdf)

#### Запуск решения:

```bash
$ git clone ...
$ docker-compose up -d
```
[Ссылка на бота по умолчанию](t.me/dd_walpaper_bot)

#### Конфигурация решения:

Решение запускается с настройками по умолчанию, чтобы переопрделить их достаточно создать файл ./wallpaper_bot/bot/config.ini вида:
```ini
[bot]
token=1150307397:AAG5l_dSXdgUq_zfTso1NeXufOuErHDurVA
private_channel_id=253473703

[photo_producer]
api_key=d7d5ad87e6400d181f7147d4a5cd7227
api_secret=4374c55a7294c650
tag=industrial

[DDLogoImageProcessor]
# Желаемые пропорции лого к изображению
# Лого будет растягиваться пропорционально,
# так, чтобы высота лого не превышала высоту
# изображения умноженную на height_factor.
# То же самое с шириной.
# (т.е лого не будет растянуто в ширину или высоту)

height_factor = 0.2
width_factor = 0.6
filling_colour = 180, 180, 180, 180
```

