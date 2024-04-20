from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.2.7'
DESCRIPTION = 'Illuminat: Revolutionizing Education through Personalization'

# Setting up
setup(
    name="illuminatapp",
    version=VERSION,
    author="Amey Aggarwal",
    author_email="<ameyaggarwal.sms@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={
        'illuminatapp': ['*.png', '*.ttf', '*.kv', '*.mp3', '*.mp4', '*.dll', '*.txt', '*.jpg', '*.wav', '*.cfg',
                         '*.json']},
    install_requires=['asyncgui==0.6.1', 'asyncio==3.4.3', 'asynckivy==0.6.2', 'azure-cognitiveservices-speech==1.36.0',
                      'build==1.0.3', 'buildozer==1.5.0', 'CacheControl==0.13.1', 'cachetools==5.3.2',
                      'certifi==2024.2.2', 'cffi==1.16.0', 'click==8.1.7', 'decorator==4.4.2', 'distlib==0.3.8',
                      'distro==1.9.0', 'docutils==0.20.1', 'Eel==0.16.0', 'et-xmlfile==1.1.0', 'filelock==3.13.1',
                      'firebase-admin==6.4.0', 'Flask==3.0.3', 'google-api-core==2.15.0',
                      'google-api-python-client==2.113.0', 'google-auth==2.29.0', 'google-auth-httplib2==0.2.0',
                      'google-cloud-core==2.4.1', 'google-cloud-firestore==2.14.0', 'google-cloud-storage==2.14.0',
                      'google-crc32c==1.5.0', 'google-resumable-media==2.7.0', 'googleapis-common-protos==1.62.0',
                      'greenlet==3.0.3', 'grpcio==1.60.0', 'grpcio-status==1.60.0', 'gTTS==2.5.1', 'httpcore==1.0.4',
                      'httplib2==0.22.0', 'httpx==0.27.0', 'jaraco.classes==3.4.0', 'jaraco.context==5.3.0',
                      'jaraco.functools==4.0.0', 'joblib==1.3.2', 'keyring==25.1.0', 'kivy', 'kivy-deps.angle==0.4.0',
                      'kivy-deps.glew==0.3.1', 'kivy-deps.sdl2==0.7.0', 'Kivy-Garden==0.1.5', 'kivymd==1.2.0',
                      'lazy_loader==0.3', 'libretranslatepy==2.1.1', 'librosa==0.10.1', 'llvmlite==0.42.0',
                      'lxml==5.1.0', 'markdown-it-py==3.0.0', 'MarkupSafe==2.1.5', 'materialyoucolor==2.0.7',
                      'mdurl==0.1.2', 'more-itertools==10.2.0', 'moviepy==1.0.3', 'mpmath==1.3.0', 'msal==1.28.0',
                      'msal-extensions==1.1.0', 'msgpack==1.0.7', 'msrest==0.7.1', 'msrestazure==0.6.4',
                      'mtranslate==1.8', 'multidict==6.0.5', 'networkx==3.2.1', 'nh3==0.2.17', 'numba==0.59.0',
                      'oauthlib==3.2.2', 'openai==1.17.1', 'openpyxl==3.1.2', 'packaging==23.2', 'pandas==2.2.1',
                      'pandas-stubs==2.2.1.240316', 'pefile==2023.2.7', 'pexpect==4.9.0', 'pillow==10.3.0',
                      'pip-tools==7.4.0', 'pkginfo==1.10.0', 'platformdirs==4.2.0', 'pooch==1.8.1',
                      'portalocker==2.8.2', 'proglog==0.1.10', 'proto-plus==1.23.0', 'protobuf==4.25.2',
                      'ptyprocess==0.7.0', 'pyasn1==0.5.1', 'pyasn1-modules==0.3.0', 'pycparser==2.21',
                      'pydantic==2.6.4', 'pydantic_core==2.16.3', 'pydub==0.25.1', 'Pygments==2.17.2',
                      'pyinstaller==6.5.0', 'pyinstaller-hooks-contrib==2024.3', 'PyJWT==2.8.0', 'pyparsing==3.1.1',
                      'pypiwin32==223', 'pyinstaller-hooks-contrib==2024.3', 'pywin32==306', 'pywin32-ctypes==0.2.2',
                      'PyYAML==6.0.1', 'readme_renderer==43.0', 'regex==2023.12.25', 'requests==2.31.0',
                      'requests-oauthlib==2.0.0', 'requests-toolbelt==1.0.0', 'rfc3986==1.5.0', 'rsa==4.9',
                      'safetensors==0.4.2', 'scikit-learn==1.4.1.post1', 'sh==2.0.6', 'six==1.16.0', 'sniffio==1.3.0',
                      'soundfile==0.12.1', 'soxr==0.3.7', 'supyr-struct==1.5.4', 'sympy==1.12', 'threadpoolctl==3.3.0',
                      'tokenizers==0.15.2', 'toml==0.10.2', 'tqdm==4.66.1', 'transformers==4.39.2', 'twine==5.0.0',
                      'types-pytz==2024.1.0.20240203', 'typing_extensions==4.9.0', 'tzdata==2024.1',
                      'uritemplate==4.1.1', 'urllib3==2.2.1', 'uuid==1.30', 'virtualenv==20.25.1', 'watch==0.2.7',
                      'Werkzeug==3.0.1', 'whichcraft==0.6.1', 'wave==0.0.2', 'yarl==1.9.4'],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
