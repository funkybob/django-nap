from setuptools import setup, find_packages

with open('README.rst') as fin:
    readme = fin.read()

setup(
    name='django-nap',
    version='0.40.0',
    description='A light REST tool for Django',
    long_description=readme,
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    url='http://github.com/funkybob/django-nap',
    keywords=['django', 'json', 'rest', 'api'],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    zip_safe=False,
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        # 'Programming Language :: Python :: Implementation :: PyPy',
    ],
    requires = [
        'Django (>=2.0)',
    ],
    extras_require={
        'rps': ['requets'],
    },
    install_requires = [
        'Django>=2.0',
    ],
)
