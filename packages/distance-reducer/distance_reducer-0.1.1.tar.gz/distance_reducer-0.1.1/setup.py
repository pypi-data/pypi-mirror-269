from distutils.core import setup

setup(
    name='distance_reducer',
    packages=['distance_reducer'],
    version='0.1.1',
    license='MIT',
    description='Group dataframe elements by minimizing the distance between them using linear minimization',
    author='Kevin Bourdon',
    author_email='kevin.bourdon@kedgebs.com',
    url='https://github.com/KevinBrd',
    download_url='https://github.com/KevinBrd/distance_reducer/archive/refs/tags/v_0.1.1.tar.gz',
    keywords=['GROUP', 'DISTANCE', 'MINIMIZING', 'LINEAR', 'OPTIMIZATION'],
    install_requires=[
        'numpy',
        'pandas',
        'plotly',
        'docplex',
        'geopy',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Office/Business',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: System :: Clustering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
