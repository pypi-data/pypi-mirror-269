from setuptools import setup
from setuptools import find_packages
from humai_tools import __version__

setup(
    name='humai_tools',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'mercadopago',
        'requests',
        'unidecode',
        'pydantic',
        'python-dotenv',
        'pydantic-settings',
        'pytz'
    ],
    author='Humai Dev Team',
    author_email='admin@humai.com.ar',
    description='Internal tools for private usage.',
    long_description_content_type="text/markdown",
    long_description="Internal tools for private usage.",
    url='https://github.com/institutohumai/humai_internal_tools',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
