from setuptools import setup, find_packages

setup(
    name='BookDB',
    version='0.1.0',
    description='A tool for populating book data into databases for big data processing',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/BookDB',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        # List your package dependencies here
        # 'requests', 'pandas', etc.
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)