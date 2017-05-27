from setuptools import setup, find_packages

with open('README.rst') as fin:
    readme = fin.read()

setup(
    name='django-nap',
    version='0.30.5',
    description='A light REST tool for Django',
    long_description=readme,
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    url='http://github.com/funkybob/django-nap',
    keywords=['django', 'json', 'rest'],
    packages = find_packages(exclude=('tests*',)),
    zip_safe=False,
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: Implementation :: PyPy',
    ],
    requires = [
        'Django (>=1.8)',
    ],
    install_requires = [
        'Django>=1.8',
    ],
)
