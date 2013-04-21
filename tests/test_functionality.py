import os
from test_configuration import NoseSeleniumBase
from unittest2 import TestCase, TestSuite, skipUnless
from nose_selenium import SeleniumTestCase

import logging
logger = logging.getLogger(__name__)

class FunctionalityBase(NoseSeleniumBase):

    def makeSuite(self):
        class TC(SeleniumTestCase):

            def runTest(self):
                self.wd.get("http://google.com")
                self.assertEqual(self.wd.title, "Google")

        return TestSuite([TC()])

    def test_browser_works(self):
        if self.__class__.__name__ == 'FunctionalityBase':
            return  # abstract test

        for line in self.output:
            line = line.rstrip()

        self.assertTrue('Ran 1 test' in self.output)
        self.assertTrue('OK' in self.output)

#### All these skips are because I don't want to put real credentials
#### into a public repository and/or not all environments have a
#### GUI to run browsers in.

@skipUnless('FIREFOX_IS_INSTALLED' in os.environ,
            "set FIREFOX_IS_INSTALLED environment variable to run this test")
class TestLocalFirefox(FunctionalityBase):
    """This test will only run if FIREFOX_IS_INSTALLED is set in the
    testrunner's env."""
    args = [
        '--browser-location=local',
        '--browser=FIREFOX',
    ]

@skipUnless('REMOTE_SELENIUM_ADDRESS' in os.environ,
            "set REMOTE_SELENIUM_ADDRESS environment variable to run this test")
class TestRemoteWindowsFirefox(FunctionalityBase):
    """This test will only run if REMOTE_SELENIUM_ADDRESS is set in the
    testrunner's env."""
    args = [
        '--browser-location=remote',
        '--browser=FIREFOX',
    ]
    env = os.environ

@skipUnless(
    'SAUCE_USERNAME' in os.environ and 'SAUCE_APIKEY' in os.environ,
    "set SAUCE_USERNAME and SAUCE_APIKEY environment variables to run this test")
class TestSauceLinuxOpera(FunctionalityBase):
    """This test will only run if SAUCE_USERNAME and SAUCE_APIKEY
    are set in the testrunner's env."""
    args = [
        '--browser-location=sauce',
        '--browser=chrome',
        '--browser-version=',  # chrome always runs latest
        '--os=Linux',
    ]
    env = os.environ
