import os
from nose.plugins import Plugin
from selenium import webdriver

import logging
logger = logging.getLogger(__name__)


# storing these at module level so they can be imported into scripts
BROWSER_LOCATION = None
BROWSER = None
BUILD = None
BROWSER_VERSION = None
OS = None
BASE_URL = None
REMOTE_ADDRESS = None
REMOTE_PORT = None
TIMEOUT = None
SAUCE_USERNAME = None
SAUCE_APIKEY = None

class NoseSelenium(Plugin):

    name = 'nose-selenium'
    score = 200
    status = {}

    def help(self):
        pass

    def options(self, parser, env=os.environ):

        parser.add_option('--browser-location',
                          action='store',
                          choices=['local', 'remote', 'grid', 'sauce'],
                          default=env.get('SELENIUM_BROWSER_LOCATION', ['local']),
                          dest='browser_location',
                          help='Run the browser in this location'
                         )
        valid_browsers = [attr for attr in dir(webdriver.DesiredCapabilities) if not attr.startswith('__')]
        parser.add_option('--browser',
                          action='store',
                          choices=valid_browsers,
                          default=env.get('SELENIUM_BROWSER', ['FIREFOX']),
                          metavar='[local|grid|sauce]',
                          dest='browser',
                          help='Run this type of browser (default %default)'
        )
        parser.add_option('--build',
                         action='store',
                         dest='build',
                         default=None,
                         metavar='str',
                         help='build identifier (for continuous integration).')
        parser.add_option('--browser-version',
                          action='store',
                          type='str',
                          default="",
                          dest='browser_version',
                          help='Run this version of the browser. (required for grid or sauce)')
        valid_oses = ['windows', 'mac', 'linux']
        parser.add_option('--os',
                          action='store',
                          dest='os',
                          default=None,
                          choices=valid_oses,
                          help='Run the browser on this operating system. (default: %default, required for grid or sauce)')
        parser.add_option('--grid-address',
                         action='store',
                         dest='grid_address',
                         default=None,
                         metavar='str',
                         help='host that selenium grid is listening on.')
        parser.add_option('--grid-port',
                         action='store',
                         dest='grid_port',
                         type='int',
                         default=4444,
                         metavar='num',
                         help='port that selenium grid is listening on. (default: %default)')
        parser.add_option('--remote-address',
                          action='store',
                          dest='remote_address',
                          default=env.get('REMOTE_SELENIUM_ADDRESS', []),
                          metavar='str',
                          help='host that selenium server is listening on.')
        parser.add_option('--remote-port',
                          action='store',
                          dest='remote_port',
                          type='int',
                          default=4444,
                          metavar='num',
                          help='port that selenium server is listening on. (default: %default)')
        parser.add_option('--timeout',
                         action='store',
                         type='int',
                         default=60,
                         metavar='num',
                         help='timeout (in seconds) for page loads, etc. (default: %default)')
        parser.add_option('--sauce-username',
                         action='store',
                         default=env.get('SAUCE_USERNAME', []),
                         dest='sauce_username',
                         metavar='str',
                         help='username for sauce labs account.')
        parser.add_option('--sauce-apikey',
                         action='store',
                         default=env.get('SAUCE_APIKEY', []),
                         dest='sauce_apikey',
                         metavar='str',
                         help='API Key for sauce labs account.')
        parser.add_option('--baseurl',
                          action='store',
                          dest='base_url',
                          metavar='url',
                          help='base url for the application under test.')
        Plugin.options(self, parser, env)


    def configure(self, options, conf):
        global BROWSER_LOCATION
        global BROWSER
        global BUILD
        global BROWSER_VERSION
        global OS
        global BASE_URL
        global REMOTE_ADDRESS
        global REMOTE_PORT
        global TIMEOUT
        global SAUCE_USERNAME
        global SAUCE_APIKEY

        Plugin.configure(self, options, conf)
        if self.enabled:
            BROWSER_LOCATION = options.browser_location
            BROWSER = options.browser
            BASE_URL = options.base_url
            TIMEOUT = options.timeout
            BUILD = options.build
            # # so long as chrome is always empty for latest, we can't
            # # validate browser version
            # if options.browser_location in ['grid', 'sauce']:
            #     BROWSER_VERSION = options.browser_version
            #     if BROWSER_VERSION == None:
            #         raise Exception("'grid' and 'sauce' values for --browser-location "
            #             "require the --browser-version option.")
            if options.browser_location in ['grid', 'remote']:
                REMOTE_ADDRESS = options.grid_address or options.remote_address
                REMOTE_PORT = options.grid_port or options.remote_port
                if not REMOTE_ADDRESS:
                    raise Exception("'grid' and 'remote' values for --browser-location "
                        "require --grid-address or --remote-address, respectively.")
            if options.browser_location == 'sauce':
                SAUCE_USERNAME = options.sauce_username
                SAUCE_APIKEY = options.sauce_apikey
                if not SAUCE_USERNAME or not SAUCE_APIKEY:
                    raise Exception("'sauce' value for --browser-location "
                        "requires --sauce-username and --sauce-apikey.")
            if options.browser_location in ['grid', 'sauce']:
                OS = options.os
                if not OS:
                    raise Exception("'grid' and 'sauce' values for --browser-location " +
                        "require the --os option.")


    # def finalize(self, result):
    #     super(NoseSelenium, self).finalize(result)


def build_webdriver(name="", tags=[], public=False):
    """Create and return the desired WebDriver instance."""
    global BROWSER_LOCATION
    global BROWSER
    global BUILD
    global BROWSER_VERSION
    global OS
    global BASE_URL
    global REMOTE_ADDRESS
    global REMOTE_PORT
    global TIMEOUT
    global SAUCE_USERNAME
    global SAUCE_APIKEY

    wd = None

    if BROWSER_LOCATION == 'local':
        if BROWSER == 'FIREFOX':
            wd = webdriver.Firefox()
        elif BROWSER == 'CHROME':
            wd = webdriver.Chrome()
        elif BROWSER == 'INTERNETEXPLORER':
            wd = webdriver.Ie()
        else:
            raise Exception(
                'WebDriver does not have a driver for local %s' % BROWSER)

    elif BROWSER_LOCATION == 'remote':
        capabilities = getattr(webdriver.DesiredCapabilities, BROWSER.upper())
        executor = 'http://%s:%s/wd/hub' % (REMOTE_ADDRESS, REMOTE_PORT)
        wd = webdriver.Remote(command_executor=executor,
                              desired_capabilities=capabilities)

    elif BROWSER_LOCATION == 'grid':
        capabilities = getattr(webdriver.DesiredCapabilities, BROWSER.upper())
        capabilities['version'] = BROWSER_VERSION
        capabilities['platform'] = OS.upper()
        executor = 'http://%s:%s/wd/hub' % (REMOTE_ADDRESS, REMOTE_PORT)
        wd = webdriver.Remote(command_executor=executor,
                              desired_capabilities=capabilities)

    elif BROWSER_LOCATION == 'sauce':
        capabilities = {
            'build': BUILD,
            'name': name,
            'tags': tags,
            'public': public,
            'restricted-public-info': not public,
            'platform': OS,
            'browserName': BROWSER,
            'version': BROWSER_VERSION,
        }
        executor = 'http://%s:%s@ondemand.saucelabs.com:80/wd/hub' % (SAUCE_USERNAME, SAUCE_APIKEY)
        wd = webdriver.Remote(command_executor=executor,
                         desired_capabilities=capabilities)

    wd.implicitly_wait(TIMEOUT * 1000)  # translate sec to ms
    # sometimes what goes out != what goes in, so log it
    logger.info("actual capabilities: %s" % wd.capabilities)
    return wd