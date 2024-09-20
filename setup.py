from setuptools import find_packages, setup

with open('README.md', 'r', encoding='UTF-8') as f:
    readme = f.read()

setup(
    name='steam-trader',
    version='0.3.1',
    author='Lemon4ksan (Bananchiki)',
    author_email='senya20151718@gmail.com',
    license='BSD License',
    url='https://github.com/Lemon4ksan/SteamTrader-Wrapper',
    keywords='python steam trader api wrapper library client питон пайтон '
    'стим трейдер апи обёртка библиотека клиент',
    description='Неофициальная Python библиотека для работы с API сервиса Steam-Trader.',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['httpx'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: Russian',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    python_requires='>=3.12',
    project_urls={
        'Документация': 'https://lemon4ksan.github.io/steam-trader/',
    }
)
