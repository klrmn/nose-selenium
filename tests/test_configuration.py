from nose.plugins import PluginTester
from unittest2 import TestCase, TestSuite
from nose_selenium import NoseSelenium
from exceptions import TypeError

import logging
logger = logging.getLogger(__name__)


class NoseSeleniumBase(PluginTester, TestCase):
    activate = '--with-nose-selenium' # enables the plugin
    plugins = [NoseSelenium()]

    def makeSuite(self):
        class TC(TestCase):
            def runTest(self):
                raise ValueError("We should never get here")

        return TestSuite([TC()])


class ConfigurationErrorBase(NoseSeleniumBase):

    def setUp(self):
        self.error = None
        try:
            super(ConfigurationErrorBase, self).setUp()
        except TypeError as e:
            self.error = e

    @property
    def expected_error(self):
        """Implement this in the child test classes."""
        raise NotImplementedError

    def test_error_raised(self):
        if self.__class__.__name__ == 'ConfigurationErrorBase':
            return  # abstract
        self.assertIn(self.expected_error, self.error.message)


############################# local ##############################


class TestLocalInvalidBrowser(ConfigurationErrorBase):
    args = [
        '--browser-location=local',
        '--browser=HTMLUNIT',
        ]

    @property
    def expected_error(self):
        return "HTMLUNIT not in available options for --browser:"


################################ grid ############################

# cannot usefully test for browser version


class TestGridRequiresOS(ConfigurationErrorBase):
    args = [
        '--browser-location=grid',
        '--browser=FIREFOX',
        '--browser-version=10',
        '--grid-address=localhost',
    ]

    @property
    def expected_error(self):
        return ("'grid' value for --browser-location requires the --os option.")


class TestGridRequiresGridAddress(ConfigurationErrorBase):
    args = [
        '--browser-location=grid',
        '--browser=FIREFOX',
        '--os=windows',
        '--browser-version=10',
        ]

    @property
    def expected_error(self):
        return ("'grid' value for --browser-location requires --grid-address.")


class TestGridInvalidBrowser(ConfigurationErrorBase):
    args = [
        '--browser-location=grid',
        '--browser=iceweasel',
        '--grid-address=192.168.0.107',
        '--os=windows',
        ]

    @property
    def expected_error(self):
        return "iceweasel not in available options for --browser:"


#################### remote #####################################

class TestRemoteRequiresRemoteAddress(ConfigurationErrorBase):
    args = [
        '--browser-location=remote',
        '--browser=SAFARI',
        '--os=windows',
        '--browser-version=10',
        ]

    @property
    def expected_error(self):
        return ("'remote' value for --browser-location requires --remote-address.")


class TestRemoteInvalidBrowser(ConfigurationErrorBase):
    args = [
        '--browser-location=remote',
        '--browser=iceweasel',
        '--remote-address=192.168.0.107',
    ]

    @property
    def expected_error(self):
        return "iceweasel not in available options for --browser:"


##################### sauce #####################################

# cannot usefully test for browser version


class TestSauceInvalidBrowser(ConfigurationErrorBase):
    args = [
        '--browser-location=sauce',
        '--browser=iceweasel',
        '--browser-version=3.4',
        '--os=Linux',
        '--sauce-username=foo',
        '--sauce-apikey=bar',
    ]

    @property
    def expected_error(self):
        return "iceweasel not in available options for --browser:"


class TestSauceRequiresOS(ConfigurationErrorBase):
    args = [
        '--browser-location=sauce',
        '--browser=firefox',
        '--browser-version=10',
        '--sauce-username=foo',
        '--sauce-apikey=bar',
        ]

    @property
    def expected_error(self):
        return ("'sauce' value for --browser-location requires the --os option.")


class TestSauceRequiresUsername(ConfigurationErrorBase):
    args = [
        '--browser-location=sauce',
        '--browser-version=10',
        '--os=windows',
        '--sauce-apikey=bar',
    ]

    @property
    def expected_error(self):
        return ("'sauce' value for --browser-location " +
                "requires --sauce-username and --sauce-apikey.")


class TestSauceRequiresApikey(ConfigurationErrorBase):
    args = [
        '--browser-location=sauce',
        '--browser-version=10',
        '--os=windows',
        '--sauce-username=foo',
    ]

    @property
    def expected_error(self):
        return ("'sauce' value for --browser-location " +
                "requires --sauce-username and --sauce-apikey.")


#################### General ##########################


# class TestBrowserHelp(NoseSeleniumBase):
#     """ this test just doesn't want to work. when the SystemExit message
#     is thrown, it means that self.output doesn't get populated,
#     and SystemExit has a code as a parameter, not a message.
#     """
#     args = [
#         '--browser-help',
#         ]
#
#     def setUp(self):
#         try:
#             super(TestBrowserHelp, self).setUp()
#         except SystemExit as e:
#             self.error = e
#
#     def test_browser_help_message(self):
#         self.assertIn(
#             "Sauce Labs OS - Browser - Browser Version combinations:",
#             self.output)
