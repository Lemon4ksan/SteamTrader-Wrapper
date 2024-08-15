import re
from setuptools import find_packages, setup

with open('steam_trader/__init__.py', encoding='UTF-8') as f:
    version = re.findall(r"__version__ = '(.+)'", f.read())[0]

with open('README.md', 'r', encoding='UTF-8') as f:
    readme = f.read()

setup(
    name='steam-trader',
    version=version,
    author='Lemon4ksan (Bananchiki)',
    author_email='senya20151718@gmail.com',
    license='BSD License',
    url='https://github.com/MarshalX/yandex-music-api/',
    keywords='python steam trader api wrapper library client питон пайтон '
    'стим трейдер апи обёртка библиотека клиент',
    description='Неофициальная Python библиотека для работы с API сервиса Steam-Trader.',
    long_description=readme,
    long_description_content_type='text/markdown',
    package_dir={'': 'steam_trader'},
    packages=find_packages(),
    install_requires=['httpx',],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: Russian',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD 3-Clause License',
        'Operating System :: OS Independent',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    python_requires='>=3.12',
)
