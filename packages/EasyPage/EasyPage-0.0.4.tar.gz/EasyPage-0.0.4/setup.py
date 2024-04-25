from setuptools import setup, find_packages

setup(
    name='EasyPage',
    version='0.0.4',
    author='leviathangk',
    author_email='1015295213@qq.com',
    description='基于 CDP 协议，简洁快速的浏览器控制 API',
    keywords=['EasyPage', 'page', 'browser'],
    packages=find_packages(),
    install_requires=[
        "lxml",
        "parsel",
        "requests",
        "loguru",
        "beautifulsoup4",
        "websockets",
        "pyee",
        "websocket-client",
    ],
)

"""
    python setup.py sdist
    python -m twine upload dist/*
"""
