import os
from test_configuration import NoseSeleniumBase, ConfigurationErrorBase
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
class TestDefaults(FunctionalityBase):
    pass


@skipUnless('CHROME_IS_INSTALLED' in os.environ,
            "set CHROME_IS_INSTALLED environment variable to run this test")
class TestLocalFirefox(FunctionalityBase):
    """This test will only run if FIREFOX_IS_INSTALLED is set in the
    testrunner's env."""
    args = [
        '--browser-location=local',
        '--browser=CHROME',
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


########### server not responding test cases #6 ###############
# class TestSauceInvalidCreds(ConfigurationErrorBase):
#     args = [
#         '--browser-location=sauce',
#         '--browser=chrome',
#         '--browser-version=',
#         '--os=Linux',
#         '--sauce-username=foo',
#         '--sauce-apikey=bar',
#     ]
#
#     @property
#     def expected_error(self):
#         return "Error authenticating to Sauce Labs."
#
# class TestRemoteNotResponding(ConfigurationErrorBase):
#     args = [
#         '--browser-location=remote',
#         '--browser=FIREFOX',
#         '--remote-address=192.167.0.106',
#     ]
#
#     @property
#     def expected_error(self):
#         return "Error connecting to remote selenium server."
#
#
# class TestGridNotResponding(ConfigurationErrorBase):
#     args = [
#         '--browser-location=grid',
#         '--browser=FIREFOX',
#         '--grid-address=192.167.0.106',
#         '--os=windows',
#     ]
#
#     @property
#     def expected_error(self):
#         return "Error connecting to selenium grid server."


@skipUnless('REMOTE_SELENIUM_ADDRESS' in os.environ,
            "set REMOTE_SELENIUM_ADDRESS environment variable to run this test")
class SeleniumErrorCatching(NoseSeleniumBase):
    args = [
        '--browser-location=remote',
        '--saved-files-storage=/tmp/selenium_files'
    ]
    env = os.environ

    def makeSuite(self):
        class TC(SeleniumTestCase):

            def runTest(self):
                self.wd.get("http://google.com")
                self.wd.find_element_by_css_selector("#this-does-not-exist").click()
                self.assertEqual(self.wd.title, "Google")

        return TestSuite([TC()])

    def test_browser_works(self):
        for line in self.output:
            line = line.rstrip()

        # 3 kudos for whomever can tell me how to test the logging output
        # for "Screenshot saved to /tmp/selenium_files/1367965901247792.png"
        # and "HTML saved to /tmp/selenium_files/1367965901247792.html"
        self.assertTrue('NoSuchElementException' in self.output)
        self.assertTrue('Ran 1 test' in self.output)
