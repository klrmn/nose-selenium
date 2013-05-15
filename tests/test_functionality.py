import os
from test_configuration import NoseSeleniumBase, ConfigurationErrorBase
from unittest2 import TestCase, TestSuite, skipUnless
from nose_selenium import SeleniumTestCase
from selenium.webdriver.support.ui import WebDriverWait
from webserver import SimpleWebServer

import logging
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

sel_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
sel_logger.setLevel(level=logging.ERROR)

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


LOCALHOST = 'localhost'

class LiveWebServerSeleniumTestCase(SeleniumTestCase):

    def setUp(self):
        super(LiveWebServerSeleniumTestCase, self).setUp()
        self.webserver = SimpleWebServer()
        self.webserver.start()

    def tearDown(self):
        self.webserver.stop()
        super(LiveWebServerSeleniumTestCase, self).tearDown()


@skipUnless('REMOTE_SELENIUM_ADDRESS' in os.environ,
            "set REMOTE_SELENIUM_ADDRESS environment variable to run this test")
class SeleniumErrorCatchingBase(NoseSeleniumBase):
    args = [
        # '--browser-location=remote',
        '--saved-files-storage=/tmp/selenium_files',
        # i want this to expose the logging in the nose-selenium file, but
        '--nologcapture'  # it actually controls line 159, which doesn't make sense to me
    ]
    env = os.environ

    @property
    def expected_exception(self):
        return ''

    def test_browser_works(self):
        if self.__class__.__name__ == 'SeleniumErrorCatchingBase':
            return  # abstract test

        for line in self.output:
            line = line.rstrip()
            logger.debug("OUTPUT: " + line)

        # 3 kudos for whomever can tell me how to test the logging output
        # for "Screenshot saved to /tmp/selenium_files/1367965901247792.png"
        # and "HTML saved to /tmp/selenium_files/1367965901247792.html"
        self.assertTrue(self.expected_exception in self.output)
        self.assertTrue('Ran 1 test' in self.output)
        self.assertTrue(False)


class CatchRegularError(SeleniumErrorCatchingBase):
    @property
    def expected_exception(self):
        return 'NoSuchElementException'

    def makeSuite(self):
        class TC(LiveWebServerSeleniumTestCase):

            def runTest(self):
                self.wd.get('http://%s:%s' % (LOCALHOST, self.webserver.port))
                self.wd.find_element_by_css_selector("#this-does-not-exist").click()

        return TestSuite([TC()])


class CatchWaitForError(SeleniumErrorCatchingBase):
    @property
    def expected_exception(self):
        return 'TimeoutException'

    def makeSuite(self):
        class TC(LiveWebServerSeleniumTestCase):

            def runTest(self):
                self.wd.get('http://%s:%s' % (LOCALHOST, self.webserver.port))
                self.wd.implicitly_wait(0)
                WebDriverWait(self.wd, 5).until(
                    lambda s: self.wd.find_element_by_css_selector(
                        "#this-does-not-exist"))

        return TestSuite([TC()])


class CatchAssertionError(SeleniumErrorCatchingBase):
    @property
    def expected_exception(self):
        return 'AssertionError'

    def makeSuite(self):
        class TC(LiveWebServerSeleniumTestCase):

            def runTest(self):
                self.wd.get('http://%s:%s' % (LOCALHOST, self.webserver.port))
                self.assertTrue(False)

        return TestSuite([TC()])

