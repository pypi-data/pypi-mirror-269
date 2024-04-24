#!usr/bin/env python3
# -*- coding: utf-8 -*-
from .xiuxian_xiazaishuju import download_xiuxian_data
from nonebot.plugin import PluginMetadata
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent
)
from nonebot import get_driver
from pathlib import Path
from nonebot.log import logger
from nonebot import require, load_all_plugins
from .config import config as _config
from nonebot import load_all_plugins   


DRIVER = get_driver()
dir_ = Path(__file__).parent


try:
    NICKNAME: str = list(DRIVER.config.nickname)[0]
except Exception as e:
    logger.info(f"缺少超级用户配置文件，{e}!")
    NICKNAME = 'bot'

try:
    download_xiuxian_data()
except Exception as e:
    logger.info(f"下载配置文件失败，修仙插件无法加载，{e}!")
    raise ImportError


require('nonebot_plugin_apscheduler')


src = 'src.plugins.'                              # src = ''内应当是插件上级目录+插件保存地址,注意地址之接连接用. 
load_all_plugins(
        [
            f'{src}xiuxian.xiuxian_boss',
            f'{src}xiuxian.xiuxian_bank',
            f'{src}xiuxian.xiuxian_sect',
            f'{src}xiuxian.xiuxian_info',
            f'{src}xiuxian.xiuxian_buff',
            f'{src}xiuxian.xiuxian_back',
            f'{src}xiuxian.xiuxian_rift',
            f'{src}xiuxian.xiuxian_mixelixir',
            f'{src}xiuxian.xiuxian_work',
            f'{src}xiuxian.xiuxian_base',
        ],
        [],
    )



__plugin_meta__ = PluginMetadata(
    name='修仙模拟器',
    description='',
    usage=(
        "必死之境机逢仙缘，修仙之路波澜壮阔！\n"
        " 输入 < 修仙帮助 > 获取仙界信息"
    ),
    extra={
        "show": True,
        "priority": 15
    }
)




