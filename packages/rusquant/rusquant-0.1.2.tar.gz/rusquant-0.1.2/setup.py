from setuptools import setup, find_packages
 
setup(
    name='rusquant',
    version='0.1.2',
    packages=find_packages(),
    include_package_data=True,
    description='Quantitative Trading Framework',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/arbuzovv/rusquant',
    author='V.Arbuzov',
    author_email='arbuzov1989@gmail.com',
    license='MIT',
    install_requires=[
        'requests',
    ],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)