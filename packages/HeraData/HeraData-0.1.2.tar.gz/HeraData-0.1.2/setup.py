from setuptools import setup, find_packages

setup(
    name='HeraData',
    version='0.1.2',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author='369',
    author_email='luck.yangbo@gmail.com',
    description='A data storage library',
    packages=find_packages(),
    install_requires=[
        'elasticsearch',
    ],
    python_requires='>=3.6',
)
