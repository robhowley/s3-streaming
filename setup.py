import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='s3-streaming',
    version='0.0.3',
    author='Rob Howley',
    author_email='howley.robert@gmail.com',
    description='stream and (de)serialize s3 objects with no local footprint',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/robhowley/s3-streaming',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
