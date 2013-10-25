from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.ui import Select
import re

class PytaniumElement(WebElement):
            
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
            
            self.from_selenium_element(selenium_element)            
        
        # Override all the WebElement actions        
        _oldexecute = WebElement._execute
        
        def _newexecute(command, *args, **kwargs):
            
            if self._parent:
                
                # Inject javascript to supplement Selenium functionality
                self._parent.inject_extensions()
                
                # Make sure it's ready to execute
                self._parent.wait_until_load_complete()
            
            # We use the tag name to check for existence
            # If we don't skip the tag name, we have a loop
            if not command == Command.GET_ELEMENT_TAG_NAME:
                if self._id:         
                    
                    # Make sure the object even exists
                    self.assert_exists()
                
                else:
                    
                    # If not, try to find it again
                    self.get_selenium_element()
                    
                    # Make sure it exists now
                    self.assert_exists()
                         
            # If we made it here, execute the original execute
            return _oldexecute(self, command, *args, **kwargs)
            
        self._execute = _newexecute
    
    # Sahi
    def exists(self):
        
        if WebElement._id:
            
            try:
                self.tag_name
                # TODO: Figure out which is best to determine if element exists
                # self.location
                # self.id
                # self.text
                
                return True
                                
            except StaleElementReferenceException:
                self.get_selenium_element()
                
                if WebElement._id:
                    return True
                else:
                    return False
        else:
            self.get_selenium_element()
            
            if WebElement._id:
                return True
            else:
                return False
    
    # Sahi
    def assert_exists(self):
        if not self.exists():
            raise Exception("{0}('{1}') was not found on the page".format(self.accessor_name, self.identifier))
        
    def get_value(self):
        return self.get_attribute('value')
        
    def set_value(self, value, add = False):        
        if not add:
            if self.accessor_name == 'select':
                try:
                    Select(self).deselect_all()
                except NotImplementedError:
                    # Don't do anything if it's not a multiselect
                    pass
            else:
                self.clear()
                
        self.send_keys(value)        
    
    # Sahi
    value = property(get_value, set_value)
    
    # Sahi
    def check(self):        
        if not self.is_selected():
            self.click()
    
    # Sahi  
    def uncheck(self):
        if self.is_selected():
            self.click()
            
    # Sahi
    def right_click(self):
        self.assert_exists()
        ActionChains(self._parent).context_click(self).perform()
    
    # Sahi
    def double_click(self):
        ActionChains(self._parent).double_click(self).perform()
        
    # Sahi
    def get_selected(self):
        selected_options = Select(self).all_selected_options
        
        # Returns a single option or a list of options
        if len(selected_options) == 1:
            return selected_options[0].text
        else:
            return [o.text for o in selected_options]
    
    # Sahi
    def set_selected(self, value, add = False):
        
        # If we're not adding
        if not add:
            try:
                Select(self).deselect_all()
            except NotImplementedError:
                # Don't do anything if it's not a multiselect
                pass
        
        # Can be passed a list of options to set
        if type(value) is list:
            for val in value:
                Select(self).select_by_visible_text(val)
        else:
            Select(self).select_by_visible_text(value)       
    
    # Sahi
    selected = property(get_selected, set_selected)
    
    def from_selenium_element(self, webelement):
        WebElement._id = webelement._id
        WebElement._parent = webelement._parent
    
    # Identify the selenium element id and parent
    def get_selenium_element(self):
        
        # If the original constructor was a selenium element, we're done
        if self.uses_selenium_identifier:
            return
        
        # TODO: Try to remove wait until ready for better performance
        self._parent.wait_until_load_complete() 
        
        # Build the identifier regex
        id_regex = None
        
        # Don't change the original identifier
        ident = self.identifier
        
        # Is the original identifier a regex
        is_regex = False # Assume it's not
        
        # Is the original identifier a simple index
        is_only_index = False # Assume it's not
        
        # Is the original identifier a dictionary
        is_dictionary = False # Assume it's not
        
        if type(ident) is str:
            
            # Build regex to find [#] and get an index
            bracket_digit_re = re.compile(r'.*\[(\d+)\]$')
            regex_result = bracket_digit_re.findall(ident)
            
            # If a [#] exists
            if len(regex_result) > 0:
                
                # Store the index from [#] (there should only be one)
                self.index = int(regex_result[0])
                
                # Remove the last [#] tag
                split = ident.rsplit('[' + str(self.index) + ']' , 1)
                ident = split[0]
                        
            # See if it's a regex
            if ident[0] == '/' and ident[len(ident) - 1] == '/':
                is_regex = True
                
                # Remove the '/'s
                ident = ident[1 : len(ident) - 1]
            
            if is_regex:
                id_regex = re.compile(ident)
                
        elif type(ident) is int:
            is_only_index = True
            self.index = ident
        
        elif type(ident) is dict:
            is_dictionary = True
            
        # Identify the possible accessors
        poss_accessors = [a for a in self._parent.accessors if a['name'] == self.accessor_name]
        
        # Loop through all the possible accessors
        for poss_accessor in poss_accessors:
            
            tag = poss_accessor['tag'].lower()
            atype = poss_accessor['type']
            
            # Get all the nodes from the tags name
            nodes = self._parent.find_elements_by_tag_name(tag)
            
            if is_dictionary:
                # Get the total number of matches
                matches = []
                
                # Loop through the all the nodes
                for node in nodes:
                    
                    valid_node = True
                    
                    if atype and node.get_attribute('type') != atype:
                        continue
                    
                    # Loop through the dictionary
                    for att, val in ident.iteritems():                        
                        
                        # If the attribute doesn't have the right value
                        if node.get_attribute(att) != val:
                            valid_node = False
                            break
                    
                    if valid_node:
                        matches.append(node)
                
                if len(matches) > self.index:
                    el = matches[self.index]
                    
                    self.from_selenium_element(el)
                    
                    return
#                    return PytaniumElement(poss_accessor, 
#                                           webelement = matches[index], 
#                                           identifier = "{0}('{1}')".format(name, identifier), 
#                                           pytanium_parent = self)
            
            else:
                
                # Look through using a prioritized attribute list        
                attributes = poss_accessor['attributes']
                
                # Loop through the attributes
                for attribute in attributes:
                    
                    # Get the total number of matches for this attribute
                    matches = []
                    
                    # Loop through all the nodes, checking for each attribute
                    for node in nodes:
                        
                        try:
                            if atype and node.get_attribute('type') != atype:
                                continue
                            
                            if attribute == 'sahiText':
                                
                                # If it's a regex, we only want to look at the text of the item
                                if is_regex:
                                    
                                    validated_text = ""
                                    unvalidated_text = node.text
                                    
                                    node_children = node.find_elements_by_xpath('.//*')
                                    
                                    # Loop through all the children
                                    for node_child in node_children:
                                        child_text = str(node_child.text)
                                        child_start = unvalidated_text.find(child_text)
                                        
                                        # If the child is present in the unvalidated text
                                        if child_start >= 0:
                                            
                                            # Validate everything before the child
                                            validated_text += unvalidated_text[:child_start]
                                            
                                            # Everything after the child is still unvalidated
                                            unvalidated_text = unvalidated_text[child_start + len(child_text):]
                                        
                                        # If there's no more text to validate, break
                                        if len(unvalidated_text) == 0:
                                            break
                                    
                                    # All remaining text is considered validated
                                    validated_text += unvalidated_text
                                    
                                    if id_regex.search(validated_text):
                                        matches.append(node)
                                
                                # If it's not a regex, we can just use the text
                                else:
                                    # TODO: Figure out how we should replace characters with spaces
                                    # I think it should just be \n with spaces and trim the ends
                                    if ident == str(node.text):
                                        matches.append(node)
                                
                                continue
                            
                            if attribute == 'className':                            
                                # TODO: make sure this is all className does
                                attribute = 'class'
                                
                            if attribute == "fileFromURL":
                                
                                # Get the src
                                source = str(node.get_attribute("src"))
                                
                                # Filter out everything except the last back slash
                                file_name = source[source.rfind('/') + 1:]
                                
                                # If the identifier matches the last item
                                if ident == file_name:
                                    # Add it to the matches
                                    matches.append(node)                                
                                continue
                            
                            if is_regex:                            
                                if id_regex.search(str(node.get_attribute(attribute))):
                                    matches.append(node)
                                    continue
                            elif is_only_index:
                                matches.append(node)
                                continue
                            else:
                                if ident == str(node.get_attribute(attribute)):
                                    matches.append(node)
                                    continue
                            
                            if attribute.find('|') >= 0:
                                attribute_split = attribute.split('|')
                                
                                for att in attribute_split:
                                    #if node.get_attribute(att) == ident:
                                    
                                    if is_regex:
                                        if id_regex.search(node.get_attribute(att)):
                                            matches.append(node)
                                            
                                            # Break so we don't add it twice
                                            break  
                                    
                                    # If the ident is an index
                                    elif is_only_index:
                                        matches.append(node)
                                        
                                        # Break so we don't add it twice
                                        break
                                    
                                    else:
                                        if ident == node.get_attribute(att):
                                            matches.append(node)
                                            
                                            # Break so we don't add it twice
                                            break                       
                                continue
                                
                        except StaleElementReferenceException:
                            continue
                
                    if len(matches) > self.index:
                        el = matches[self.index]
                    
                        # Needed for drag_and_drop
                        self.from_selenium_element(el)
                        
                        return
                    
        WebElement._id = None        
        return 