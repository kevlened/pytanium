import selenium.webdriver.remote.webdriver

OldRemoteWebDriver = selenium.webdriver.remote.webdriver.WebDriver

from selenium.webdriver.remote.webelement import WebElement as OldWebElement

# Redefine the RemoteWebDriver
class RemoteWebDriver(OldRemoteWebDriver):
    def __init__(self, desired_capabilities = None, *args, **kwargs):
        
        # Allows you to inject a custom script on every page
        self.browser_js = ""
        
        # Create the default pytanium capabilities        
        capabilities = {'unexpectedAlertBehaviour' : 'ignore',
                        'suppressAlerts' : True,
                        'suppressConfirms' : True,
                        'suppressPrompts' : True,
                        'suppressPrint' : True,
                        'enableRecorder' : False,
                        'recorderHost' : 'localhost',
                        'recorderPort' : 9999
                        }        
        
        # If desired_capabilities were passed, update the defaults
        if desired_capabilities:
            if type(desired_capabilities) is dict:
                capabilities.update(desired_capabilities)
            else:
                raise Exception("desired_capabilities must be a dictionary")
        
        # Set the custom capabilities of pytanium
        self.suppress_alerts = capabilities['suppressAlerts']
        self.suppress_confirms = capabilities['suppressConfirms']
        self.suppress_prompts = capabilities['suppressPrompts']
        self.suppress_print = capabilities['suppressPrint']
        self.enable_recorder = capabilities['enableRecorder']
        self.recorder_host = capabilities['recorderHost']
        self.recorder_port = capabilities['recorderPort']
        
        # If we're using the recorder, check the proxy
        if self.enable_recorder:
            self.check_recorder_proxy()                
            extra_ie_capabilities = {"proxy": {
                                        "httpProxy":"{0}:{1}".format(self.recorder_host, str(self.recorder_port)),
                                        "ftpProxy":None,
                                        "sslProxy":None,
                                        "noProxy":None,
                                        "proxyType":"MANUAL",
                                        "class":"org.openqa.selenium.Proxy",
                                        "autodetect":False
                                        }}
            
            capabilities.update(extra_ie_capabilities)
            
        # Build accessors to help identify objects using Sahi's style
        self.accessors = []
        self.accessors_name_set = set()
#        self.load_accessors()        
        
        # Build the old remote webdriver
        #super(OldRemoteWebDriver, self).__init__(*args, **kwargs)
        OldRemoteWebDriver.__init__(self, desired_capabilities = desired_capabilities, *args, **kwargs)
        
        # Set the default window as the first open window
        self.default_window = self.current_window_handle

# Modify the base webdriver
selenium.webdriver.remote.webdriver.WebDriver = RemoteWebDriver

# Reload all the drivers that use the base webdriver
reload(selenium.webdriver.firefox.webdriver)
Firefox = selenium.webdriver.firefox.webdriver.WebDriver

reload(selenium.webdriver.chrome.webdriver)
Chrome = selenium.webdriver.chrome.webdriver.WebDriver

reload(selenium.webdriver.ie.webdriver)
Ie = selenium.webdriver.ie.webdriver.WebDriver