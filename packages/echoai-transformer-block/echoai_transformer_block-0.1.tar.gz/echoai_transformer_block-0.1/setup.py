from setuptools import setup, find_packages

setup(
    name='echoai_transformer_block',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'torch',
    ],
    author='Echoai (pratyaksh agarwal)',
    author_email='pratyakshagarwal93@gmail.com',
    description='A package for Transformer blocks',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pratyakshagarwal/Echoai',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)