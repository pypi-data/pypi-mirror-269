from setuptools import setup
from pathlib import Path
long_description = Path('readme.md').read_text()
print(long_description)

setup(
    name='EasyDataPy',
    version='1.4',
    description='EasyDataPy through EasyData API key of State Bank of Pakistan helps to obtain information on and download a series of interest in Python for further analysis',
    long_description=long_description,
    author='Dr. Syed Ateeb Akhter Shah',
    author_email='syed.ateeb@wmich.edu',
    packages=['EasyDataPy'],
    install_requires=[
        'plotly',
        'pandas',
        'requests',
        'readme_md',
    ],
    include_package_data=True,
    long_description_content_type='text/markdown',
    keywords=['EasyData', 'EasyDataPy'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        'Programming Language :: Python'
    ],
)
