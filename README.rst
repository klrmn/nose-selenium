nose-selenium
*************

A Selenium WebDriver plugin for nose.

Thank you to `Dave Hunt <http://github.com/davehut>`_ for doing
this work first for py.test in
`pytest-mozwebqa <http://github.com/davehunt/pytest-mozwebqa>`_.

Currently, this plugin deals only with input parameters, and does not
modify the results reporting in any way.

nosetests command line options
==============================

.. code-block:: bash

    $ nosetests --with-nose-selenium --help
    Usage: nosetests [options]

    Options:
      -h, --help            show this help message and exit
      -V, --version         Output nose version and exit
      -p, --plugins         Output list of available plugins and exit. Combine
                            with higher verbosity for greater detail
      -v, --verbose         Be more verbose. [NOSE_VERBOSE]
    [snip]
      --with-nose-selenium  Enable plugin NoseSelenium: None
                            [NOSE_WITH_NOSE_SELENIUM]
      --config-file         Load options from ConfigParser compliant config file.
                            Values in config file will override values sent on the
                            command line.
      --browser-location=BROWSER_LOCATION
                            Run the browser in this location (default ['local'],
                            options [local, remote, grid, sauce]). May be stored
                            in environmental variable SELENIUM_BROWSER_LOCATION.
      --browser=BROWSER     Run this type of browser (default ['FIREFOX'], options
                            for local [FIREFOX, INTERNETEXPLORER, CHROME], options
                            for remote/grid/sauce [ANDROID, CHROME, FIREFOX,
                            HTMLUNIT, HTMLUNITWITHJS, INTERNETEXPLORER, IPAD,
                            IPHONE, OPERA, PHANTOMJS, SAFARI]). May be stored in
                            environmental variable SELENIUM_BROWSER.
      --build=str           build identifier (for continuous integration). Only
                            used for sauce.
      --browser-version=BROWSER_VERSION
                            Run this version of the browser. (default:  implies
                            latest.)
      --os=OS               Run the browser on this operating system. (default:
                            none, options [windows, mac, linux], required for grid
                            or sauce)
      --grid-address=str    host that selenium grid is listening on. (default: [])
                            May be stored in environmental variable
                            SELENIUM_GRID_ADDRESS.
      --grid-port=num       port that selenium grid is listening on. (default:
                            4444)
      --remote-address=str  host that remote selenium server is listening on. May
                            be stored in environmental variable
                            REMOTE_SELENIUM_ADDRESS.
      --remote-port=num     port that remote selenium server is listening on.
                            (default: 4444)
      --timeout=num         timeout (in seconds) for page loads, etc. (default:
                            60)
      --sauce-username=str  username for sauce labs account. May be stored in
                            environmental variable SAUCE_USERNAME.
      --sauce-apikey=str    API Key for sauce labs account. May be stored in
                            environmental variable SAUCE_APIKEY.
      --saved-files-storage Full path to place to store screenshots and html dumps.
                            May be stored in environmental variable SAVED_FILES_PATH.

Example Commands
----------------

.. code-block:: bash

    $ nosetests --with-nose-selenium --browser-location=local --browser=FIREFOX
    $ nosetests --with-nose-selenium --browser-location=grid --grid-address=192.168.0.11 --os=linux --browser=CHROME
    $ nosetests --with-nose-selenium --browser-location=remote --remote-address=192.168.0.107 --browser=HTMLUNIT
    $ nosetests --with-nose-selenium --browser-location=sauce --os=windows --browser=INTERNETEXPLORER --sauce-username=<name> --sauce-apikey=<api_key>
    $ nosetests --with-nose-selenium --config-file=selenium.conf


Writing test scripts with nose-selenium
=======================================
Loading configuration from a config file
---------------------------------
If you use the --config-file flag, the rest of the command-line flags
will be ignored. The same defaults values for optional keys apply, and
validation checking will be performed when involked from nosetests.

**Example selenium.conf file**

Not all keys are required for all configurations, read the command-line
options section above for clues. Where values are provided, they are the
defaults.

.. code-block:: bash

    [SELENIUM]
    BROWSER_LOCATION: local
    BROWSER: FIREFOX
    BUILD:
    BROWSER_VERSION:
    OS:
    # remote or grid address
    REMOTE_ADDRESS:
    # remote or grid port
    REMOTE_PORT: 4444
    TIMEOUT: 60
    SAUCE_USERNAME:
    SAUCE_APIKEY:
    SAVED_FILES_PATH:


Inheriting from SeleniumTestCase
--------------------------------

SeleniumTestCase creates the webdriver and stores it in self.wd in its setUp()
and closes it in tearDown().

.. code-block:: python

    from nose_selenium import SeleniumTestCase


    class MyTestCase(SeleniumTestCase):

        def test_that_google_opens(self):
            self.wd.get("http://google.com")
            self.assertEqual(self.wd.title, "Google")

Using ScreenshotOnExceptionWebDriver
------------------------------------
ScreenshotOnExceptionWebDriver is designed to take a screenshot, fetch the
html, and log the url before reporting any WebDriverException. It excludes
exceptions encountered by WebDriverWait's until() and until_not() methods.

Using ScreenshotOnExceptionWebDriverWait
----------------------------------------
If you want screenshots and html to be captured for TimeoutException-s
raised by WebDriverWait, use ScreenshotOnExceptionWebDriverWait in its
place.

Using build_webdriver in your test scripts
------------------------------------------

If you're not using test classes, you may use build_webdriver
in the following manner. Its extra arguments are used to attach
metadata to SauceLabs jobs and ignored if the browser is not being
opened on SauceLabs.

.. code-block:: python

    from nose_selenium import build_webdriver

    def test_that_google_opens():
        wd = build_webdriver(name="google opens", tags=['sanity'], public=False)
        wd.get('http://google.com')
        assert wd.title == 'Google'
        wd.halt()

Using setup_selenium_from_config()
----------------------------------
If you'd like to use ``ScreenshotOnExceptionWebDriver`` or
``ScreenshotOnExceptionWebDriverWait`` without using the nose framework,
you can put its settings in a ConfigParser compliant file with a [SELENIUM]
section and call ``setup_selenium_from_config`` with a ConfigParser instance which
has read from this file. This will set up the variables so that
``build_webdriver`` can read them.

.. code-block:: python

    from nose_selenium import build_webdriver, setup_selenium_from_config
    from ConfigParser import ConfigParser

    CONFIG = ConfigParser()
    CONFIG.read('selenium.conf')

    setup_selenium_from_config(CONFIG)
    wd = build_webdriver()


.. note::

    If you use portions of this library without using nose, validity checking
    will not be performed.
    
Backwards Compatibility
=======================

As this code is in 'alpha' I will attempt but not promise backwards compatibility.
Please leave me a note if you're using this plugin, as I am more likely to break
backwards compatibility if I think I'm the only one using it.

Bugs and Feature Requests
=========================

I am aware that this plugin represents a minimal set of features. If there is
something in particular you would like me to add, please check the
`issues list <http://github.com/klrmn/nose-selenium/issues>`_ and create new
issues or leave comments in existing ones.