import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.14'
PACKAGE_NAME = 'Andreani_QA_Scanner'  # Debe coincidir con el nombre de la carpeta
AUTHOR = 'AndreaniTesting'
AUTHOR_EMAIL = 'user_appglatest@andreani.com'
URL = ''
LICENSE = 'MIT'  # Tipo de licencia
DESCRIPTION = 'SeleniumFramework para ejecución de casos automatizados'  # Descripción corta
LONG_DESCRIPTION = ""
LONG_DESC_TYPE = "text/markdown"

# Paquetes necesarios para que funcione la librería.
INSTALL_REQUIRES = [
    "attrs==23.1.0", "blinker==1.7.0", "bottle==0.12.25", "certifi==2023.7.22", "cffi==1.15.1",
    "charset-normalizer==3.3.1", "click==8.1.7", "clr-loader==0.2.6", "colorama==0.4.6", "exceptiongroup==1.1.3",
    "Flask==3.0.0", "h11==0.14.0", "idna==3.4", "importlib-metadata==6.8.0", "itsdangerous==2.1.2", "Jinja2==3.1.2",
    "libretranslatepy==2.1.1", "lxml==4.9.3", "MarkupSafe==2.1.3", "mtranslate==1.8", "outcome==1.2.0",
    "proxy-tools==0.1.0", "pycparser==2.21", "pyperclip==1.8.2", "PySocks==1.7.1", "pythonnet==3.0.1",
    "pywebview==4.3.3", "requests==2.31.0", "screeninfo==0.8.1", "selenium==4.11.2", "sniffio==1.3.0",
    "sortedcontainers==2.4.0", "trio==0.22.2", "trio-websocket==0.10.3", "typing_extensions==4.7.1", "urllib3==2.0.4",
    "Werkzeug==3.0.1", "wsproto==1.2.0", "zipp==3.17.0", "pynput==1.7.6", "flask-cors==4.0.0", "openpyxl==3.1.2",
    "tldextract==5.1.1", "pillow==10.2.0","python-docx"]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    package_data={
        'Andreani_QA_Scanner': ['app/*.js', 'app/extension/*.css', 'app/extension/*.png', 'app/extension/*.js',
                                'app/extension/*.html', 'app/extension/*.svg', 'app/extension/*.json',
                                'app/src/*.json', 'src/*.js', 'src/js/*.json', 'src/js/*.js', 'src/style/*.css',
                                'src/templates/*.html']},
    include_package_data=True
)
