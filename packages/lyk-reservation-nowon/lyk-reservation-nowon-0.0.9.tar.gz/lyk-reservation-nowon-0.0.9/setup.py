from setuptools import setup

setup(
    name='lyk-reservation-nowon',
    version='0.0.9',
    keywords=['reservation', 'lyk', 'pypi'],
    install_requires=['pyperclip', 'selenium', 'webdriver_manager'],
    packages=['lyk_reservation'],
    package_dir={'lyk_reservation': 'dist'}
)
