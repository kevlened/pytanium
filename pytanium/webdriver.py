import httplib
import selenium.webdriver.remote.webdriver
from pytanium_element import PytaniumElement

OldRemoteWebDriver = selenium.webdriver.remote.webdriver.WebDriver

# Redefine the RemoteWebDriver
class RemoteWebDriver(OldRemoteWebDriver):
    def __init__(self, desired_capabilities = None, *args, **kwargs):
        
        # Modify the existing WebElement identification functions
        oldfindelement = OldRemoteWebDriver.find_element
        
        def find_element(*args, **kwargs):
            webelement = oldfindelement(*args, **kwargs)
            return PytaniumElement(selenium_element = webelement)
        
        OldRemoteWebDriver.find_element = find_element
        
        # TODO: Override the ability to identify multiple elements
        
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
        self.load_accessors()        
        
        # Build the old remote webdriver
        OldRemoteWebDriver.__init__(self, desired_capabilities = desired_capabilities, *args, **kwargs)
        
        # Set the default window as the first open window
        self.default_window = self.current_window_handle
    
    def check_recorder_proxy(self):
        try:
            testconn = httplib.HTTPConnection(self.recorder_host, self.recorder_port)
            testconn.connect()
            testconn.request("GET", "/_s_/spr/blank.htm")
            testconn.getresponse();
            testconn.close()
            
        except Exception:
            raise Exception("The recorder proxy is not available. Please start Sahi on {0}:{1}.".format(self.recorder_host, self.recorder_port))
     
         
    def addAD(self, accessor):
        self.accessors.append(accessor)
        self.accessors_name_set.add(accessor['name'])  
    
    # Taken *almost* directly from concat.js in Sahi
    def load_accessors(self):
#        self.addAD({'tag': "INPUT", 'type': "text", 'event':"change", 'name': "textbox", 'attributes': ["name", "id", "index", "className"], 'action': "_setValue", 'value': "value"})
        self.addAD({'tag': "A", 'type': None, 'event':"click", 'name': "link", 'attributes': ["sahiText", "title|alt", "id", "index", "href", "className"], 'action': "click", 'value': "sahiText"})
#        self.addAD({'tag': "IMG", 'type': None, 'event':"click", 'name': "image", 'attributes': ["title|alt", "id", this.getFileFromURL, "index", "className"], 'action': "click"})
        self.addAD({'tag': "IMG", 'type': None, 'event':"click", 'name': "image", 'attributes': ["title|alt", "id", "fileFromURL", "index", "className"], 'action': "click"})
        
        self.addAD({'tag': "LABEL", 'type': None, 'event':"click", 'name': "label", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "LI", 'type': None, 'event':"click", 'name': "listItem", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "UL", 'type': None, 'event':"click", 'name': "list", 'attributes': ["id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "OL", 'type': None, 'event':"click", 'name': "list", 'attributes': ["id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "DIV", 'type': None, 'event':"click", 'name': "div", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "SPAN", 'type': None, 'event':"click", 'name': "span", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "TABLE", 'type': None, 'event':"click", 'name': "table", 'attributes': ["id", "className", "index"], 'action': None, 'value': "sahiText"})
        self.addAD({'tag': "TR", 'type': None, 'event':"click", 'name': "row", 'attributes': ["id", "className", "sahiText", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "TD", 'type': None, 'event':"click", 'name': "cell", 'attributes': ["sahiText", "id", "className", "index", "encaps_TR", "encaps_TABLE"], 'action': "click", 'idOnly': False, 'value': "sahiText"})
        self.addAD({'tag': "TH", 'type': None, 'event':"click", 'name': "tableHeader", 'attributes': ["sahiText", "id", "className", "encaps_TABLE"], 'action': "click", 'value': "sahiText"})
    
        self.addAD({'tag': "INPUT", 'type': "button", 'event':"click", 'name': "button", 'attributes': ["value", "name", "id", "index", "className"], 'action': "click", 'value': "value"})
        self.addAD({'tag': "BUTTON", 'type': "button", 'event':"click", 'name': "button", 'attributes': ["sahiText", "name", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        
#        self.addAD({'tag': "INPUT", 'type': "checkbox", 'event':"click", 'name': "checkbox", 'attributes': ["name", "id", "value", "className", "index"], 'action': "click", 'value': "checked", 'assertions': function(value){return [("true" == ("" + value)) ? _sahi.language.ASSERT_CHECKED : _sahi.language.ASSERT_NOT_CHECKED];}})
        self.addAD({'tag': "INPUT", 'type': "checkbox", 'event':"click", 'name': "checkbox", 'attributes': ["name", "id", "value", "className", "index"], 'action': "click", 'value': "checked"})

        
        self.addAD({'tag': "INPUT", 'type': "password", 'event':"change", 'name': "password", 'attributes': ["name", "id", "index", "className"], 'action': "setValue", 'value': "value"})
#        self.addAD({'tag': "INPUT", 'type': "radio", 'event':"click", 'name': "radio", 'attributes': ["id", "name", "value", "className", "index"], 'action': "click", 'value': "checked", assertions: function(value){return [("true" == ("" + value)) ? _sahi.language.ASSERT_CHECKED : _sahi.language.ASSERT_NOT_CHECKED];}})    
        self.addAD({'tag': "INPUT", 'type': "radio", 'event':"click", 'name': "radio", 'attributes': ["id", "name", "value", "className", "index"], 'action': "click", 'value': "checked"})    
        
        self.addAD({'tag': "INPUT", 'type': "submit", 'event':"click", 'name': "submit", 'attributes': ["value", "name", "id", "className", "index"], 'action': "click", 'value': "value"})    
        self.addAD({'tag': "BUTTON", 'type': "submit", 'event':"click", 'name': "submit", 'attributes': ["sahiText", "name", "id", "className", "index"], 'action': "click", 'value': "sahiText"})    
    
        self.addAD({'tag': "INPUT", 'type': "text", 'event':"change", 'name': "textbox", 'attributes': ["name", "id", "index", "className"], 'action': "setValue", 'value': "value"})
        
        self.addAD({'tag': "INPUT", 'type': "reset", 'event':"click", 'name': "reset", 'attributes': ["value", "name", "id", "className", "index"], 'action': "click", 'value': "value"})    
        self.addAD({'tag': "BUTTON", 'type': "reset", 'event':"click", 'name': "reset", 'attributes': ["sahiText", "name", "id", "className", "index"], 'action': "click", 'value': "sahiText"})    
    
        self.addAD({'tag': "INPUT", 'type': "hidden", 'event':"", 'name': "hidden", 'attributes': ["name", "id", "className", "index"], 'action': "setValue", 'value': "value"})    
        
        self.addAD({'tag': "INPUT", 'type': "file", 'event':"click", 'name': "file", 'attributes': ["name", "id", "index", "className"], 'action': "setFile", 'value': "value"})    
#        self.addAD({'tag': "INPUT", 'type': "image", 'event':"click", 'name': "imageSubmitButton", 'attributes': ["title|alt", "name", "id", this.getFileFromURL, "index", "className"], 'action': "click"})    
        self.addAD({'tag': "INPUT", 'type': "image", 'event':"click", 'name': "imageSubmitButton", 'attributes': ["title|alt", "name", "id", "fileFromURL", "index", "className"], 'action': "click"}) 
        self.addAD({'tag': "INPUT", 'type': "date", 'event':"change", 'name': "datebox", 'attributes': ["name", "id", "index", "className"], 'action': "setValue", 'value': "value"})
        self.addAD({'tag': "INPUT", 'type': "datetime", 'event':"change", 'name': "datetimebox", 'attributes': ["name", "id", "index", "className"], 'action': "setValue", 'value': "value"})
        self.addAD({'tag': "INPUT", 'type': "datetime-local", 'event':"change", 'name': "datetimelocalbox", 'attributes': ["name", "id", "index", "className"], 'action': "setValue", 'value': "value"})
        self.addAD({'tag': "INPUT", 'type': "email", 'event':"change", 'name': "emailbox", 'attributes': ["name", "id", "index", "className"], 'action': "setValue", 'value': "value"})
        self.addAD({'tag': "INPUT", 'type': "month", 'event':"change", 'name': "monthbox", 'attributes': ["name", "id", "index", "className"], 'action': "setValue", 'value': "value"})
        self.addAD({'tag': "INPUT", 'type': "number", 'event':"change", 'name': "numberbox", 'attributes': ["name", "id", "index", "className"], 'action': "setValue", 'value': "value"})
        self.addAD({'tag': "INPUT", 'type': "range", 'event':"change", 'name': "rangebox", 'attributes': ["name", "id", "index", "className"], 'action': "setValue", 'value': "value"})
        self.addAD({'tag': "INPUT", 'type': "search", 'event':"change", 'name': "searchbox", 'attributes': ["name", "id", "index", "className"], 'action': "setValue", 'value': "value"})
        self.addAD({'tag': "INPUT", 'type': "tel", 'event':"change", 'name': "telephonebox", 'attributes': ["name", "id", "index", "className"], 'action': "setValue", 'value': "value"})
        self.addAD({'tag': "INPUT", 'type': "time", 'event':"change", 'name': "timebox", 'attributes': ["name", "id", "index", "className"], 'action': "setValue", 'value': "value"})
        self.addAD({'tag': "INPUT", 'type': "url", 'event':"change", 'name': "urlbox", 'attributes': ["name", "id", "index", "className"], 'action': "setValue", 'value': "value"})
        self.addAD({'tag': "INPUT", 'type': "week", 'event':"change", 'name': "weekbox", 'attributes': ["name", "id", "index", "className"], 'action': "setValue", 'value': "value"})
    
        
        
#        self.addAD({'tag': "SELECT", 'type': None, 'event':"change", 'name': "select", 'attributes': ["name", "id", "index", "className"], 'action': "setSelected", 'value': function(el){return _sahi._getSelectedText(el) || _sahi.getOptionId(el, el.value) || el.value;},assertions: function(value){return [_sahi.language.ASSERT_SELECTION];}})    
        self.addAD({'tag': "SELECT", 'type': None, 'event':"change", 'name': "select", 'attributes': ["name", "id", "index", "className"], 'action': "setSelected"})    

        self.addAD({'tag': "OPTION", 'type': None, 'event':"none", 'name': "option", 'attributes': ["encaps_SELECT", "sahiText", "value", "id", "index"], 'action': "", 'value': "sahiText"})    
        self.addAD({'tag': "TEXTAREA", 'type': None, 'event':"change", 'name': "textarea", 'attributes': ["name", "id", "index", "className"], 'action': "setValue", 'value': "value"})
        self.addAD({'tag': "H1", 'type': None, 'event':"click", 'name': "heading1", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "H2", 'type': None, 'event':"click", 'name': "heading2", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "H3", 'type': None, 'event':"click", 'name': "heading3", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "H4", 'type': None, 'event':"click", 'name': "heading4", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "H5", 'type': None, 'event':"click", 'name': "heading5", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "H6", 'type': None, 'event':"click", 'name': "heading6", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        
        self.addAD({'tag': "AREA", 'type': None, 'event':"click", 'name': "area", 'attributes': ["id", "title|alt", "href", "shape", "className", "index"], 'action': "click"})
        self.addAD({'tag': "MAP", 'type': None, 'event':"click", 'name': "map", 'attributes': ["name", "id", "title", "className", "index"], 'action': "click"})
    
        self.addAD({'tag': "P", 'type': None, 'event':"click", 'name': "paragraph", 'attributes': ["encaps_A", "id", "className", "sahiText", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "I", 'type': None, 'event':"click", 'name': "italic", 'attributes': ["encaps_A", "sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "EM", 'type': None, 'event':"click", 'name': "emphasis", 'attributes': ["encaps_A", "sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "B", 'type': None, 'event':"click", 'name': "bold", 'attributes': ["encaps_A", "sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "STRONG", 'type': None, 'event':"click", 'name': "strong", 'attributes': ["encaps_A", "sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "PRE", 'type': None, 'event':"click", 'name': "preformatted", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "CODE", 'type': None, 'event':"click", 'name': "code", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "BLOCKQUOTE", 'type': None, 'event':"click", 'name': "blockquote", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "CANVAS", 'type': None, 'event':"click", 'name': "canvas", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "ABBR", 'type': None, 'event':"click", 'name': "abbr", 'attributes': ["encaps_A", "sahiText", "title", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "HR", 'type': None, 'event':"click", 'name': "hr", 'attributes': ["id", "className", "index"], 'action': "click", 'value': ""})
        
#        var o_fn1 = function(o){try{return o._sahi_getFlexId()}catch(e){}};
#        var o_fn2 = function(o){try{return o._sahi_getUID()}catch(e){}};
#        self.addAD({'tag': "OBJECT", 'type': None, 'event':"click", 'name': "object", 'attributes': ["id", "name", "data", o_fn1, o_fn2], 'action': "click", 'value': ""})
#        self.addAD({'tag': "EMBED", 'type': None, 'event':"click", 'name': "embed", 'attributes': ["name", "id", o_fn1, o_fn2], 'action': "click", 'value': ""})
        self.addAD({'tag': "OBJECT", 'type': None, 'event':"click", 'name': "object", 'attributes': ["id", "name", "data"], 'action': "click", 'value': ""})
        self.addAD({'tag': "EMBED", 'type': None, 'event':"click", 'name': "embed", 'attributes': ["name", "id"], 'action': "click", 'value': ""})

        self.addAD({'tag': "DL", 'type': None, 'event':"click", 'name': "dList", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "DT", 'type': None, 'event':"click", 'name': "dTerm", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "DD", 'type': None, 'event':"click", 'name': "dDesc", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
    
        self.addAD({'tag': "RECT", 'type': None, 'event':"click", 'name': "svg_rect", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "TSPAN", 'type': None, 'event':"click", 'name': "svg_tspan", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        
        self.addAD({'tag': "CIRCLE", 'type': None, 'event':"click", 'name': "svg_circle", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "ELLIPSE", 'type': None, 'event':"click", 'name': "svg_ellipse", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "LINE", 'type': None, 'event':"click", 'name': "svg_line", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "POLYGONE", 'type': None, 'event':"click", 'name': "svg_polygon", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        
        self.addAD({'tag': "POLYLINE", 'type': None, 'event':"click", 'name': "svg_polyline", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "PATH", 'type': None, 'event':"click", 'name': "svg_path", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        self.addAD({'tag': "TEXT", 'type': None, 'event':"click", 'name': "svg_text", 'attributes': ["sahiText", "id", "className", "index"], 'action': "click", 'value': "sahiText"})
        
       
    def link(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "link", identifier = identifier, *args, **kwargs)
    
    def image(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "image", identifier = identifier, *args, **kwargs)
    
    def label(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "label", identifier = identifier, *args, **kwargs)
    
    def listItem(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "listItem", identifier = identifier, *args, **kwargs)
    
    def list(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "list", identifier = identifier, *args, **kwargs)
    
    def div(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "div", identifier = identifier, *args, **kwargs)
    
    def span(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "span", identifier = identifier, *args, **kwargs)
    
    def table(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "table", identifier = identifier, *args, **kwargs)
    
    def row(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "row", identifier = identifier, *args, **kwargs)
    
    def cell(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "cell", identifier = identifier, *args, **kwargs)
    
    def tableHeader(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "tableHeader", identifier = identifier, *args, **kwargs)
    
    def button(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "button", identifier = identifier, *args, **kwargs)
    
    def checkbox(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "checkbox", identifier = identifier, *args, **kwargs)
    
    def password(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "password", identifier = identifier, *args, **kwargs)
    
    def radio(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "radio", identifier = identifier, *args, **kwargs)
    
    def submit(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "submit", identifier = identifier, *args, **kwargs)
    
    def textbox(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "textbox", identifier = identifier, *args, **kwargs)
    
    def reset(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "reset", identifier = identifier, *args, **kwargs)
    
    def hidden(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "hidden", identifier = identifier, *args, **kwargs)
    
    def file(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "file", identifier = identifier, *args, **kwargs)
    
    def imageSubmitButton(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "imageSubmitButton", identifier = identifier, *args, **kwargs)
    
    def datebox(self, identifier, *args, **kwargs):
        return PytaniumElement(pytanium_parent = self, accessor_name = "datebox", identifier = identifier, *args, **kwargs)    

# Modify the base webdriver
selenium.webdriver.remote.webdriver.WebDriver = RemoteWebDriver

# Reload all the drivers that use the base webdriver
reload(selenium.webdriver.firefox.webdriver)
Firefox = selenium.webdriver.firefox.webdriver.WebDriver

reload(selenium.webdriver.chrome.webdriver)
Chrome = selenium.webdriver.chrome.webdriver.WebDriver

reload(selenium.webdriver.ie.webdriver)
Ie = selenium.webdriver.ie.webdriver.WebDriver