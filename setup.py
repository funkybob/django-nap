from setuptools import setup, find_packages

setup(
    name='django-nap',
    version='0.13.4',
    description='A light REST tool for Django',
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    url='http://github.com/funkybob/django-nap',
    keywords=['django', 'json', 'rest'],
    packages = find_packages(exclude=['tests.*']),
    zip_safe=False,
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    requires = [
        'Django (>=1.4)',
        'six (>=1.3)',
    ],
    install_requires = [
        'Django>=1.4',
        'six>=1.3',
    ],
    extras_require = {
        'python2.6':  ["ordereddict", ],
    }
)
