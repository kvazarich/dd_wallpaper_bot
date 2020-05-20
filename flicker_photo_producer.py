import random
import requests

import flickrapi


class FlickrPhotoProducer:
    def __init__(self, config):
        self.config = config
        self.flickr = flickrapi.FlickrAPI(
            self.config.get('api_key'),
            self.config.get('api_secret'),
            format='parsed-json'
        )
        self._photo_sizes = (
            'm', 'n', 'z', 'c', 'l', 'o'
        )

    def _count_photos_by_tag(self, tag):
        resp = self.flickr.photos.search(tags=tag, per_page=1)
        return resp['photos']['pages']

    def _get_nearest_size_url(self, width, height, photo_num, tag):
        """Возвращает url фото c наиболее подходящим размером.

        Ширина и длина должны быть не меньше поданных на вход,
        чтобы картинку не пришлось растягивать(если такой нет - берем самую большую картинку).
        При этом разница должна быть минимальной"""
        extras = ','.join('url_{}'.format(size) for size in self._photo_sizes)
        '''flickr не отдает странички с номером больше 100000. Сейчас по тегу industrial примерно 1000000 фото. 
        По этому когда хотим получить фото, а не просто колличество фотографий приходится указывать per_page > 10'''
        per_page = 100
        page = photo_num // per_page
        photo_num = photo_num % per_page
        resp = self.flickr.photos.search(tags=tag, per_page=per_page, extras=extras, page=page)
        photo = resp['photos']['photo'][photo_num]
        result_url = None
        min_diference = max(width, height)
        max_size = None
        max_size_value = 0
        for size in self._photo_sizes:
            if 'url_' + size not in photo:
                continue
            size_height = photo['height_' + size]
            size_width = photo['width_' + size]
            if max_size_value < size_height * size_width:
                max_size_value = size_height * size_width
                max_size = size
            if size_height >= height and size_width >= width:
                difference = max(size_width-width, size_height-height)
                if difference < min_diference:
                    min_diference = difference
                    result_url = photo['url_' + size]
        if result_url is None:
            result_url = photo['url_' + max_size]
        return result_url

    def get_next_photo(self):
        tag = self.config.get('tag')
        photo_count = self._count_photos_by_tag(tag)
        photo_num = random.randint(1, photo_count)
        photo_url = self._get_nearest_size_url(photo_num=photo_num, width=1024, height=768, tag=tag)
        return requests.get(photo_url, stream=True).content