# -*- coding: utf-8 -*-

import os
from os.path import abspath, dirname
from importlib import import_module

BASE_PATH = dirname(dirname(abspath(__file__)))


CONFIG_MODE = os.environ.get('CONFIG_MODE') or 'local'

print(CONFIG_MODE)

config_path = os.path.join(BASE_PATH, 'config', CONFIG_MODE + '.py')

if not os.path.exists(config_path):
    print('[!] 配置错误，请初始化环境变量')
