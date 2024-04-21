from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='FlutterFinder',
    version='1.0',
    description='A command-line interface (CLI) tool to find Flutter apps in a directory.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Sai Chandan Kadarla',
    author_email='chandankadarla2722002@gmail.com',
    url='https://github.com/chan27-2/flutter-finder',
    packages=['flutter_finder'],
    entry_points={
        'console_scripts': ['flutter_finder=flutter_finder:main']
    },
    data_files=[('share/man/man1', ['flutter_finder.1'])],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities'
    ],
    python_requires='>=3.7',
)
