import random
from urllib3 import request, exceptions
from time import sleep
from webbrowser import open
import re


class YandexMusicRnd:

    def __init__(self,
                 max_index: int = 10000000,
                 open_url: bool = True,
                 max_iterations: int = 60,
                 find_clear: str = 'no',
                 find_have_albom: str = 'all',
                 find_have_similar: str = 'all',
                 find_have_clips: str = 'all',
                 show_progress: bool = True,
                 quiet: bool = False
                 ):
        """
        Init class
        :param max_index:
        :param open_url:
        :param max_iterations:
        :param find_clear:
        :param find_have_albom:
        :param find_have_similar:
        :param find_have_clips:
        :param show_progress:
        :param quiet:
        """

        self.max_index = max_index
        self.open_url = open_url
        self.max_iterations = max_iterations
        self.cur_iteration = 0
        self.find_clear = find_clear
        self.find_have_albom = find_have_albom
        self.find_have_similar = find_have_similar
        self.find_have_clips = find_have_clips
        self.show_progress = show_progress
        self.quiet = quiet

    def get_artist(self, open_url: bool = None) -> str:
        """

        :param open_url:
        :return: Site url
        """

        if open_url is None:
            open_url = self.open_url

        found = False
        while not found:
            if self.cur_iteration >= self.max_iterations:
                break

            self.cur_iteration += 1

            index = random.randint(1, self.max_index)

            site = f'https://music.yandex.ru/artist/{index}'

            if not self.quiet and self.show_progress:
                self.print_progress(site)

            header = {
                'useragent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br, zstd', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cache-Control': 'no-cache',
                'Cookie': '_ym_uid=1622682016147407419; top100_id=t1.-1.395082145.1655703021280; adtech_uid=1c96e7f3-45ff-4585-9b88-a16144779124%3A; tmr_lvid=997ea03b7523aaf9e0fd16976517d34a; tmr_lvidTS=1622682017469; _ga_2L9VT8HJQE=GS1.1.1683682860.18.1.1683682861.0.0.0; _ga=GA1.2.137072697.1622682018; _ga_0BR10WFP5Z=GS1.2.1687415179.2.0.1687415179.0.0.0; _ym_d=1702424816; t3_sid_4425061=s1.994923944.1712897308203.1712897386591.336.1; last_visit=1712861386592%3A%3A1712897386592; _ga_TZS1E41JJM=GS1.2.1712897309.312.1.1712897386.0.0.0; PHPSESSID=ahun8gohjv99s7kds26jcmgd29; _csrf=aaf6b526379541551f526a37be005efcccc9d4f8063390272258cf965c359ba5a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%222ERUErtaUMh1s_Gupg-D6JhLlVhd3H5K%22%3B%7D; _ym_isad=2; _ym_visorc=w'
            }

            try:
                response = request('GET', site, headers=header)
            except exceptions.HTTPError as e:
                pass
            else:
                html = response.data.decode(response.headers.get('Content-charset', 'utf-8'))
                found = self.check_filter(html)

            sleep(1)

        if found:
            if open_url:
                open(site)
        else:
            if not self.quiet:
                print(f'За максимальное количество итераций ({self.max_iterations}) результат не найден.')
            site = ''

        return site

    def check_filter(self, html) -> bool:
        """
        Check filter parameters
        :param html:
        :return: Bool
        """

        clear = False
        albom = False
        similar = False
        clips = False

        if len(re.findall('>Главное</span>', html)) == 0:
            clear = True
        else:
            if len(re.findall('>Альбомы</a>', html)) >= 1:
                albom = True
            if len(re.findall('>Похожие</a>', html)) >= 1:
                similar = True
            if len(re.findall('>Клипы</a>', html)) >= 1:
                clips = True

        if self.find_clear == 'yes':
            if clear:
                return True
            else:
                return False

        if clear and self.find_clear == 'no':
            return False

        if self.find_have_albom == 'yes' and not albom:
            return False

        if self.find_have_albom == 'no' and albom:
            return False

        if self.find_have_similar == 'yes' and not similar:
            return False

        if self.find_have_similar == 'no' and similar:
            return False

        if self.find_have_clips == 'yes' and not clips:
            return False

        if self.find_have_clips == 'no' and clips:
            return False

        return True

    def print_progress(self, site: str) -> None:
        """
        Print progress
        :param site: Current site url
        :return: None
        """
        print(f'{site} [{self.cur_iteration}/{self.max_iterations}]')

    @property
    def max_index(self) -> int:
        return self.__max_index

    @max_index.setter
    def max_index(self, max_index: int):
        self.__max_index = max_index

    @property
    def open_url(self) -> bool:
        return self.__open_url

    @open_url.setter
    def open_url(self, open_url: bool):
        self.__open_url = open_url

    @property
    def max_iterations(self) -> int:
        return self.__max_iterations

    @max_iterations.setter
    def max_iterations(self, max_iterations: int):
        self.__max_iterations = max_iterations

    @property
    def quiet(self) -> bool:
        return self.__quiet

    @quiet.setter
    def quiet(self, quiet: bool):
        self.__quiet = quiet

    @property
    def show_progress(self) -> bool:
        return self.__show_progress

    @show_progress.setter
    def show_progress(self, show_progress: bool):
        self.__show_progress = show_progress

    @property
    def find_have_albom(self) -> str:
        return self.__find_have_albom

    @find_have_albom.setter
    def find_have_albom(self, find_have_albom: str):
        self.__find_have_albom = find_have_albom

    @property
    def find_have_similar(self) -> str:
        return self.__find_have_similar

    @find_have_similar.setter
    def find_have_similar(self, find_have_similar: str):
        self.__find_have_similar = find_have_similar

    @property
    def find_have_clips(self) -> str:
        return self.__find_have_clips

    @find_have_clips.setter
    def find_have_clips(self, find_have_clips: str):
        self.__find_have_clips = find_have_clips

    @property
    def find_clear(self) -> str:
        return self.__find_clear

    @find_clear.setter
    def find_clear(self, find_clear: str):
        self.__find_clear = find_clear
