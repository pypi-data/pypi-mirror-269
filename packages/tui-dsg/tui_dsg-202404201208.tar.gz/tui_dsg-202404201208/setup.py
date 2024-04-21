from setuptools import setup, find_packages
from datetime import datetime


version = datetime.now().strftime('%Y%m%d%H%M')

setup(
    name='tui_dsg',
    version=version,
    author='Eric Tröbs',
    author_email='eric.troebs@tu-ilmenau.de',
    description='everything you need for our jupyter notebooks',
    long_description='everything you need for our jupyter notebooks',
    long_description_content_type='text/markdown',
    url='https://dbgit.prakinf.tu-ilmenau.de/lectures/data-science-grundlagen',
    project_urls={},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.10',
    install_requires=[
        'jupyter',
        'ipywidgets',
        'checkmarkandcross',
        'pillow~=10.2.0',
        'requests~=2.31.0',
        'beautifulsoup4~=4.12.3',
        'numpy~=1.26.4',
        'pandas~=1.5.3',
        'pyyaml~=6.0.1',
        'grizzly_sql==0.1.5.post1',
        'plotly~=5.20.0',
        'kaleido~=0.2.1',
        'matplotlib~=3.8.3',
        'networkx~=2.8.8',
        'scipy~=1.12.0',
        'scikit-learn~=1.4.1',
        'fa2_modified',
        'statsmodels~=0.14.1',
        'torch~=2.2.2',
        'nltk~=3.8.1',
        'HanTa~=1.1.1',
        'Levenshtein~=0.25.0'
    ],
    package_data={},
    include_package_data=True
)
