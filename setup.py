from setuptools import setup, find_packages

NAME = 'src'
PACKAGES = find_packages(NAME)
setup(
    name='meg-image',
    version='1.0',
    packages=PACKAGES,
    package_dir={'': 'src'},
    package_data={
        'fonts': '*.ttf'
        },
    setup_requires=[],
    install_requires=[
        'pillow',
        'urllib3',
        'requests',
        ],
    author='liuwei02',
    author_email='liuwei02@megvii.com',
    description='megvii image',
    keywords='image',
    url='http://www.baidu.com'
)