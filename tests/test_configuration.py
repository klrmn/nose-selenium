from nose.plugins import PluginTester
from unittest2 import TestCase, TestSuite
from nose_selenium import NoseSelenium

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
        except Exception as e:
            self.error = e

    @property
    def expected_error(self):
        """Implement this in the child test classes."""
        raise NotImplementedError

    def test_error_raised(self):
        if self.__class__.__name__ == 'ConfigurationErrorBase':
            return  # abstract
        self.assertIn(self.expected_error, self.error.message)


################################ grid ############################

# class TestGridRequiresBrowserVersion(ConfigurationErrorBase):
#     args = [
#         '--browser-location=grid',
#         '--os=windows',
#         '--grid-address=localhost',
#     ]
#
#     @property
#     def expected_error(self):
#         return ("'grid' and 'sauce' values for --browser-location " +
#                 "require the --browser-version option.")


class TestGridRequiresOS(ConfigurationErrorBase):
    args = [
        '--browser-location=grid',
        '--browser-version=10',
        '--grid-address=localhost',
    ]

    @property
    def expected_error(self):
        return ("'grid' and 'sauce' values for --browser-location " +
                "require the --os option.")


class TestGridRequiresGridAddress(ConfigurationErrorBase):
    args = [
        '--browser-location=grid',
        '--os=windows',
        '--browser-version=10',
        ]

    @property
    def expected_error(self):
        return ("'grid' and 'remote' values for --browser-location " +
                "require --grid-address or --remote-address, respectively.")


#################### remote #####################################

class TestRemoteRequiresRemoteAddress(ConfigurationErrorBase):
    args = [
        '--browser-location=remote',
        '--os=windows',
        '--browser-version=10',
        ]

    @property
    def expected_error(self):
        return ("'grid' and 'remote' values for --browser-location " +
                "require --grid-address or --remote-address, respectively.")


##################### sauce #####################################

# class TestSauceRequiresBrowserVersion(ConfigurationErrorBase):
#     args = [
#         '--browser-location=sauce',
#         '--os=windows',
#         '--sauce-username=foo',
#         '--sauce-apikey=bar',
#     ]
#
#     @property
#     def expected_error(self):
#         return ("'grid' and 'sauce' values for --browser-location " +
#                 "require the --browser-version option.")


class TestSauceRequiresOS(ConfigurationErrorBase):
    args = [
        '--browser-location=sauce',
        '--browser-version=10',
        '--sauce-username=foo',
        '--sauce-apikey=bar',
        ]

    @property
    def expected_error(self):
        return ("'grid' and 'sauce' values for --browser-location " +
                "require the --os option.")


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

class TestInvalidOption(NoseSeleniumBase):

    @property
    def expected_error(self):
        """Implement this in the child test classes."""
        raise NotImplementedError

    def test_error_in_output(self):
        if self.__class__.__name__ == 'TestInvalidOption':
            return  # abstract
        logger.debug(dir(self.output))
        logger.debug(dir(self.output.stream))
        logger.debug(dir(self.output.stream.buffer))
        self.assertIn(self.expected_error, self.output.stream)

class TestInvalidBrowserOption(TestInvalidOption):
    args = [ '--browser=iceweasel', ]  # debian version of firefox

    @property
    def expected_error(self):
        return ("error: option --browser: invalid choice: 'iceweasel'")


class TestInvalidOSOption(TestInvalidOption):
    args = [ '--os=palm', ]  # chances of future support: nil

    @property
    def expected_error(self):
        return ("error: option --os: invalid choice: 'palm'")