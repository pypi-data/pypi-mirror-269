import pytest
from urllib3 import request
from fake_useragent import UserAgent
from time import sleep
import re

from ya_music_rnd import YandexMusicRnd


def get_html(site: str) -> str:
    user_agent = UserAgent().getRandom

    header = {
        'useragent': user_agent['useragent'],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Cookie': '_ym_uid=1622682016147407419; top100_id=t1.-1.395082145.1655703021280; adtech_uid=1c96e7f3-45ff-4585-9b88-a16144779124%3A; tmr_lvid=997ea03b7523aaf9e0fd16976517d34a; tmr_lvidTS=1622682017469; _ga_2L9VT8HJQE=GS1.1.1683682860.18.1.1683682861.0.0.0; _ga=GA1.2.137072697.1622682018; _ga_0BR10WFP5Z=GS1.2.1687415179.2.0.1687415179.0.0.0; _ym_d=1702424816; t3_sid_4425061=s1.994923944.1712897308203.1712897386591.336.1; last_visit=1712861386592%3A%3A1712897386592; _ga_TZS1E41JJM=GS1.2.1712897309.312.1.1712897386.0.0.0; PHPSESSID=ahun8gohjv99s7kds26jcmgd29; _csrf=aaf6b526379541551f526a37be005efcccc9d4f8063390272258cf965c359ba5a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%222ERUErtaUMh1s_Gupg-D6JhLlVhd3H5K%22%3B%7D; _ym_isad=2; _ym_visorc=w'}
    response = request('GET', site, headers=header)
    html = response.data.decode(response.headers.get('Content-charset', 'utf-8'))

    return html


def test_defaults():
    ymr = YandexMusicRnd()

    assert ymr.open_url is True
    assert ymr.max_index == 10000000
    assert ymr.max_iterations == 60
    assert ymr.find_clear == 'no'
    assert ymr.find_have_albom == 'all'
    assert ymr.find_have_similar == 'all'
    assert ymr.find_have_clips == 'all'
    assert ymr.show_progress is True
    assert ymr.quiet is False


def test_init_params():
    ymr = YandexMusicRnd(
        max_index = 123,
        open_url = False,
        max_iterations = 2,
        find_clear = 'all',
        find_have_albom = 'no',
        find_have_similar = 'yes',
        find_have_clips = 'no',
        show_progress = False,
        quiet = True
        )

    assert ymr.max_index == 123
    assert ymr.open_url is False
    assert ymr.max_iterations == 2
    assert ymr.find_clear == 'all'
    assert ymr.find_have_albom == 'no'
    assert ymr.find_have_similar == 'yes'
    assert ymr.find_have_clips == 'no'
    assert ymr.show_progress is False
    assert ymr.quiet is True


def test_check_filter_1():
    ymr = YandexMusicRnd()

    site = 'https://music.yandex.ru/artist/3255295'
    html = get_html(site)

    # ymr.find_clear = 'no'
    # ymr.find_have_albom = 'all'
    # ymr.find_have_similar = 'all'
    # ymr.find_have_clips = 'all'
    assert ymr.check_filter(html) is True

    test_table = [
        ['yes', 'all', 'all', 'all', False],
        ['no', 'yes', 'all', 'all', True],
        ['no', 'no', 'all', 'all', False],
        ['no', 'all', 'yes', 'all', False],
        ['no', 'all', 'no', 'all', True],
        ['no', 'yes', 'yes', 'all', False],
        ['no', 'yes', 'no', 'all', True],
        ['no', 'no', 'yes', 'all', False],
        ['no', 'no', 'no', 'all', False],
        ['no', 'all', 'all', 'yes', False],
        ['no', 'all', 'all', 'no', True],
        ['no', 'yes', 'all', 'yes', False],
        ['no', 'yes', 'all', 'no', True],
        ['no', 'no', 'all', 'yes', False],
        ['no', 'no', 'all', 'no', False],
        ['no', 'yes', 'yes', 'yes', False],
        ['no', 'yes', 'yes', 'no', False],
        ['no', 'no', 'no', 'yes', False],
        ['no', 'no', 'no', 'no', False],
        ['no', 'all', 'yes', 'yes', False],
        ['no', 'all', 'yes', 'no', False],
        ['no', 'all', 'no', 'yes', False],
        ['no', 'all', 'no', 'no', True],
        ['no', 'yes', 'no', 'yes', False],
        ['no', 'yes', 'no', 'no', True],
        ['no', 'no', 'yes', 'yes', False],
        ['no', 'no', 'yes', 'no', False],
    ]

    for t in test_table:

        ymr.find_clear = t[0]
        ymr.find_have_albom = t[1]
        ymr.find_have_similar = t[2]
        ymr.find_have_clips = t[3]

        assert ymr.check_filter(html) == t[4]

    sleep(1)

def test_check_filter_2():
    ymr = YandexMusicRnd()

    site = 'https://music.yandex.ru/artist/4255295'
    html = get_html(site)

    assert ymr.check_filter(html) is False

    ymr.find_clear = 'yes'
    ymr.find_have_albom = 'yes'
    ymr.find_have_similar = 'yes'
    ymr.find_have_clips = 'yes'
    assert ymr.check_filter(html) is True

    sleep(1)


def test_check_filter_3():
    ymr = YandexMusicRnd()

    site = 'https://music.yandex.ru/artist/2825481'
    html = get_html(site)

    # ymr.find_clear = 'no'
    # ymr.find_have_albom = 'all'
    # ymr.find_have_similar = 'all'
    # ymr.find_have_clips = 'all'
    assert ymr.check_filter(html) is True

    test_table = [
        ['yes', 'all', 'all', 'all', False],
        ['no', 'yes', 'all', 'all', True],
        ['no', 'no', 'all', 'all', False],
        ['no', 'all', 'yes', 'all', True],
        ['no', 'all', 'no', 'all', False],
        ['no', 'yes', 'yes', 'all', True],
        ['no', 'yes', 'no', 'all', False],
        ['no', 'no', 'yes', 'all', False],
        ['no', 'no', 'no', 'all', False],
        ['no', 'all', 'all', 'yes', False],
        ['no', 'all', 'all', 'no', True],
        ['no', 'yes', 'all', 'yes', False],
        ['no', 'yes', 'all', 'no', True],
        ['no', 'no', 'all', 'yes', False],
        ['no', 'no', 'all', 'no', False],
        ['no', 'yes', 'yes', 'yes', False],
        ['no', 'yes', 'yes', 'no', True],
        ['no', 'no', 'no', 'yes', False],
        ['no', 'no', 'no', 'no', False],
        ['no', 'all', 'yes', 'yes', False],
        ['no', 'all', 'yes', 'no', True],
        ['no', 'all', 'no', 'yes', False],
        ['no', 'all', 'no', 'no', False],
        ['no', 'yes', 'no', 'yes', False],
        ['no', 'yes', 'no', 'no', False],
        ['no', 'no', 'yes', 'yes', False],
        ['no', 'no', 'yes', 'no', False],
    ]

    for t in test_table:

        ymr.find_clear = t[0]
        ymr.find_have_albom = t[1]
        ymr.find_have_similar = t[2]
        ymr.find_have_clips = t[3]

        assert ymr.check_filter(html) == t[4]

    sleep(1)


def test_check_filter_4():
    ymr = YandexMusicRnd()

    site = 'https://music.yandex.ru/artist/4705290'
    html = get_html(site)

    # ymr.find_clear = 'no'
    # ymr.find_have_albom = 'all'
    # ymr.find_have_similar = 'all'
    # ymr.find_have_clips = 'all'
    assert ymr.check_filter(html) is True

    test_table = [
        ['yes', 'all', 'all', 'all', False],
        ['no', 'yes', 'all', 'all', False],
        ['no', 'no', 'all', 'all', True],
        ['no', 'all', 'yes', 'all', False],
        ['no', 'all', 'no', 'all', True],
        ['no', 'yes', 'yes', 'all', False],
        ['no', 'yes', 'no', 'all', False],
        ['no', 'no', 'yes', 'all', False],
        ['no', 'no', 'no', 'all', True],
        ['no', 'all', 'all', 'yes', True],
        ['no', 'all', 'all', 'no', False],
        ['no', 'yes', 'all', 'yes', False],
        ['no', 'yes', 'all', 'no', False],
        ['no', 'no', 'all', 'yes', True],
        ['no', 'no', 'all', 'no', False],
        ['no', 'yes', 'yes', 'yes', False],
        ['no', 'yes', 'yes', 'no', False],
        ['no', 'no', 'no', 'yes', True],
        ['no', 'no', 'no', 'no', False],
        ['no', 'all', 'yes', 'yes', False],
        ['no', 'all', 'yes', 'no', False],
        ['no', 'all', 'no', 'yes', True],
        ['no', 'all', 'no', 'no', False],
        ['no', 'yes', 'no', 'yes', False],
        ['no', 'yes', 'no', 'no', False],
        ['no', 'no', 'yes', 'yes', False],
        ['no', 'no', 'yes', 'no', False],
    ]

    for t in test_table:

        ymr.find_clear = t[0]
        ymr.find_have_albom = t[1]
        ymr.find_have_similar = t[2]
        ymr.find_have_clips = t[3]

        assert ymr.check_filter(html) == t[4]

    sleep(1)


def test_get_artist():
    ymr = YandexMusicRnd()

    site_1 = ymr.get_artist(False)

    assert len(re.findall('https://music.yandex.ru/artist/', site_1)) == 1

    site_2 = ymr.get_artist(False)

    assert site_1 != site_2
