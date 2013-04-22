import sys
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from setuptools import setup

setup(
    name='nose-selenium',
    version='0.01',
    author='Leah Klearman',
    author_email = 'lklrmn@gmail.com',
    description = 'Control the WebDriver instance in your scripts with command-line options',
    py_modules = ['nose_selenium'],
    entry_points = {
        'nose.plugins.0.10': [
            'nose-selenium = nose_selenium:NoseSelenium'
        ]
    },
    url='http://github.com/klrmn/nose-selenium',
    license='Mozilla Public License 2.0 (MPL 2.0)',
    keywords='nose selenium webdriver',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'],
    install_requires=['selenium', 'nose', 'requests', 'unittest2'],
)
