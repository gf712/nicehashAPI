from setuptools import setup

about = {}
with open('./nicehashAPI/__about__.py', 'r') as f:
    exec(f.read(), about)

setup(
    name='nicehashAPI',
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Programming Language :: Python :: 3 :: Only',
                 'Programming Language :: Python :: Implementation :: CPython'
                 ],
    keywords='crypto-mining nicehash cloud-mining',
    version=about['__version__'],
    package_dir={'nicehashAPI': 'nicehashAPI'},
    packages=['nicehashAPI'],
    # url='https://github.com/gf712/PyML',
    license=about['__license__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    description='Nicehash Python API',
    test_suite="tests", install_requires=['requests']
)
