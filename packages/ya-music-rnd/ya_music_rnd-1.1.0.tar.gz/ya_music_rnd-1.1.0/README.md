# yandex_rnd

![PyPI](https://img.shields.io/pypi/v/ya_music_rnd)
![PyPI - License](https://img.shields.io/pypi/l/ya_music_rnd)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ya_music_rnd)

Поиск случайного исполнителя на сайте яндекс музыки (https://music.yandex.ru) и открытие его страницы в браузере. 

***

## Установка пакета

### Установка пакета с PyPi

```bash
$ pip install ya-music-rnd
```

### Установка пакета из исходного кода

Исходный код размещается на [GitHub](https://github.com/Genzo4/yandex_rnd).  
Скачайте его и установите пакет:

```bash
$ git clone https://github.com/Genzo4/yandex_rnd
$ cd yandex_rnd
$ pip install .
```

***

## Использование пакета

- ### Подключаем:
```python
from ya_music_rnd import YandexMusicRnd
```

- ### Создаём экземпляр
Создаём экземпляр YandexMusicRnd.
Можно указать дополнительные параметры:
- max_index - максимальный индекс для поиска. 
  Значение по умолчанию: 10000000
- open_url - открывать в браузере найденного исполнителя или нет.
  Значение по умолчанию: True
- max_iterations - количество максимальных итераций поиска.
  Значение по умолчанию: 60
- find_clear - искать "пустых" исполнителей (у них на странице нет ничего).
  Принимаемые значения: 'yes' - искать только пустые, 'no' - не искать пустые, 'all' - искать и те, и другие.
  Значение по умолчанию: 'no'
- find_have_albom - фильтр исполнителей по наличию альбомов.
  Принимаемые значения: 'yes', 'no', 'all'.
  Значение по умолчанию: 'all'
- find_have_similar - фильтр исполнителей по наличию похожих исполнителей.
  Принимаемые значения: 'yes', 'no', 'all'.
  Значение по умолчанию: 'all'
- find_have_clips - фильтр исполнителей по наличию клипов.
  Принимаемые значения: 'yes', 'no', 'all'.
  Значение по умолчанию: 'all'
- show_progress - показывать прогресс поиска.
  Значение по умолчанию: True 
- quiet - не выводить никаких сообщений на экран.
  Значение по умолчанию: False

```python
ya_rnd = YandexMusicRnd()
```

- ### Находим исполнителя

```python
site = ya_rnd.get_artist()  # возвращает URL найденного артиста
```

Пример использования модуля см. в файле main.py

***

# Yandex Music Rnd

На основе пакета ya_music_rnd сделана программа Yandex Music Rnd.
Готовые билды программы можно взять в релизах на сайте Github (https://github.com/Genzo4/yandex_rnd/releases)

- ### Билд под Windows
```cmd
pip install -r requirements_build.txt
pyinstaller -F -n ya_music_rnd -i favicon32.png main.py --version-file version.txt
```

Готовый исполняемый файл появляется в папке dist. 

Помощь по параметрам командной строки можно узнать выполнив:
```cmd
ya_music_rnd.exe -h
```

***

[Changelog](https://github.com/Genzo4/yandex_rnd/blob/main/CHANGELOG.md)
