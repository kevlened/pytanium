from selenium.webdriver.remote.webelement import WebElement

class PytaniumElement(WebElement):
#    def __init__(self, *args, **kwargs):
#        WebElement.__init__(self, *args, **kwargs)
        
    def __init__(self, pytanium_parent = None, accessor_name = None, identifier = None, selenium_element = None, index = 0):
        
        self.accessor_name = accessor_name
        self.identifier = identifier
        self.index = index
        
        if selenium_element is None:
            self.uses_selenium_identifier = False
            WebElement._parent = pytanium_parent
            
            # If one wasn't passed, try to get the element
            self.get_selenium_element()
        else:
            self.uses_selenium_identifier = True
            
            WebElement._parent = selenium_element._parent
            WebElement._id = selenium_element._id