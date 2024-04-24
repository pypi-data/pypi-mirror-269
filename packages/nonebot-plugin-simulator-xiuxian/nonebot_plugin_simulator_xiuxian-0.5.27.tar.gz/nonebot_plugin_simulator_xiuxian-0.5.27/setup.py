from setuptools import setup,find_namespace_packages,find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='nonebot_plugin_simulator_xiuxian',
    version='0.5.27',
    description='修仙',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='甘城菜月',
    author_email='2859385794@qq.com',
    license='MIT license',
    include_package_data=True,
    packages=find_namespace_packages(include=["nonebot_plugin_simulator_xiuxian"]),
    platforms='all',
    install_requires=["nonebot2",
                      "nonebot-adapter-onebot",
                      'wget',
                      "nonebot_plugin_apscheduler",
                      "Pillow==9.5.0",
                      "pydantic",
                      "wcwidth",
                      "ujson",],
    url='https://github.com/luoyefufeng/nonebot_plugin_simulator_xiuxian',
)


