from setuptools import setup, find_packages

setup(
    name='lyk-reservation-nowon',
    version='0.0.10',
    keywords=['reservation', 'lyk', 'pypi'],
    install_requires=['pyperclip', 'selenium', 'webdriver_manager'],
    packages=find_packages(where='src'),
    package_dir={'': 'src'}
)
