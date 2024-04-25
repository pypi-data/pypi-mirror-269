__title__ = 'foyou-cli'
__author__ = 'foyoux'
__version__ = '0.0.19'
__url__ = 'https://github.com/foyoux/foyou-cli'
__ide__ = 'PyCharm - https://www.jetbrains.com/pycharm/'

import fire

from .aliyundrive import download_by_idm, upload_file, list_file_download_url
from .ebook import add_nav_for_epub
from .geoip import geoip
from .wikihow import wikihow


def version():
    """显示版本信息"""
    return f'{__title__}({__version__}) by {__author__}({__url__})'


def main():
    fire.Fire({
        'epub': add_nav_for_epub,
        'geoip': geoip,
        'alilist': list_file_download_url,
        'alidown': download_by_idm,
        'aliupload': upload_file,
        'wikihow': wikihow,
        'version': version,
    })
