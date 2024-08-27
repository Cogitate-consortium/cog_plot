from setuptools import setup, find_packages

setup(
    name='cog_plot',
    version='0.1.0',
    description='A brief description of your project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Cogitate-consortium/cog_plot',
    author='Alex Lepauvre',
    author_email='alex.lepauvre@ae.mpg.de',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
