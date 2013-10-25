import unittest, time
from pytanium import webdriver
from selenium.webdriver.common.keys import Keys

class TestPytanium(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(capabilities = {'enableRecorder' : False})
        
        self.base_url = "http://sahi.co.in"
        print "finished setUp"

    def tearDown(self):
        self.browser.quit()
        
    def test_classic_selenium_demo(self):
        self.browser.get("http://www.python.org")
        assert "Python" in self.browser.title
        oldelem = self.browser.find_element_by_name("q")
        elem = self.browser.textbox("q")
        assert(oldelem == elem)
        elem.send_keys("selenium")
        elem.send_keys(Keys.RETURN)
        assert "Google" in self.browser.title
        
    def test_reidentify_elements(self):
        link = self.browser.link("Link Test")
        self.browser.get(self.base_url  + "/demo/index.htm")
        link.click()

    def test_multi_select(self):
        self.browser.get(self.base_url + "/demo/selectTest.htm")
        self.browser.select("s4Id").set_selected("o1")
        self.assertEquals("o1", self.browser.select("s4Id").selected)
        self.browser.select("s4Id").set_selected("o2", add = True)
        self.assertEquals(["o1","o2"], self.browser.select("s4Id").selected)
        self.browser.select("s4Id").set_selected(["o2", "o3"])
        self.assertEquals(["o2","o3"], self.browser.select("s4Id").selected)
        self.browser.select("s4Id").set_selected(["o1", "o2"], add = True)
        self.assertEquals(["o1","o2","o3"], self.browser.select("s4Id").selected)

    def test_print_called_and_clear_print_called(self):
        self.browser.quit()
        
        self.browser = webdriver.Firefox(capabilities = {'suppressPrints' : True})
        
        self.browser.get(self.base_url + "/demo/print.htm")
        self.assertFalse(self.browser.print_called())
        self.browser.button("Print").click()
        self.assertTrue(self.browser.print_called())
        self.browser.clear_print_called()
        self.assertFalse(self.browser.print_called())
        self.browser.button("Print").click()
        self.assertTrue(self.browser.print_called())
    
#    def test_style(self):
#        self.browser.get(self.base_url + "/demo/mouseover.htm");
#        if self.browser.is_chrome() or self.browser.is_firefox():
#            self.assertEquals("16px", self.browser.span("Hi Kamlesh").style("font-size"))
#            self.assertEquals("rgba(0, 0, 238, 1)", self.browser.span("Hi Kamlesh").style("color"))
#        else:
#            self.assertEquals("16px", self.browser.span("Hi Kamlesh").style("font-size"))
#            self.assertEquals("#0066cc", self.browser.span("Hi Kamlesh").style("color"))
#            
    def test_set_file(self):
        print "Starting test_set_file"
        self.browser.get(self.base_url  + "/demo/php/fileUpload.htm")
        
        # TODO: Make this a relative path
        self.browser.file("file").send_keys("C:\SahiPro\userdata\scripts\demo\uploadme.txt")
        self.browser.submit("Submit Single").click()
        assert(self.browser.span("size").exists())
        self.assertTrue(self.browser.span("size").text.find("0.3046875 Kb") >= 0)
        self.assertTrue(self.browser.span("type").text.find("Single") >= 0)
        self.browser.link("Back to form").click()
    
    def test_multi_file_upload(self):
        print "Starting test_multi_file_upload"
        self.browser.get(self.base_url  + "/demo/php/fileUpload.htm")
        
        # TODO: Make these relatives paths
        self.browser.file("file[]").send_keys("C:\SahiPro\userdata\scripts\demo\uploadme.txt")
        self.browser.file("file[][1]").send_keys("C:\SahiPro\userdata\scripts\demo\uploadme2.txt")
        self.browser.submit("Submit Array").click()
        self.assertTrue(self.browser.span("type").text.find("Array") >= 0)
        self.assertTrue(self.browser.span("file").text.find("uploadme.txt") >= 0)
        self.assertTrue(self.browser.span("size").text.find("0.3046875 Kb") >= 0)
    
        self.assertTrue(self.browser.span("file[1]").text.find("uploadme2.txt") >= 0)
        self.assertTrue(self.browser.span("size[1]").text.find("0.32421875 Kb") >= 0)
    
#    def test_visible(self):
#        print "Starting test_visible"
#        self.browser.get(self.base_url  + "/demo/index.htm")
#        self.browser.link("Visible Test").click()
#        assert(self.browser.div("using display").is_displayed())
#    
#        self.browser.button("Display none").click()
#        assert(not self.browser.div("using display").is_displayed())
#        self.browser.button("Display block").click()
#        assert(self.browser.div("using display").is_displayed())
#    
#        self.browser.button("Display none").click()
#        assert(not self.browser.div("using display").is_displayed())
#        self.browser.button("Display inline").click()
#        assert(self.browser.div("using display").is_displayed())
#    
#        assert(self.browser.div("using visibility").is_displayed())
#        self.browser.button("Visibility hidden").click()
#        assert(not self.browser.div("using visibility").is_displayed())
#        self.browser.button("Visibility visible").click()
#        assert(self.browser.div("using visibility").is_displayed())

    def test_1(self):
        print "Starting test_1"
        self.browser.get(self.base_url + "/demo/formTest.htm")
        self.browser.alert.accept()
    #        self.browser.textbox("t1").value = "aaa"
        self.browser.textbox("t1").send_keys("aaa")
        self.browser.link("Back").click()
        self.browser.link("Table Test").click()
        self.assertEqual("Cell with id", self.browser.cell("CellWithId").text)
    
    def test_regexp(self):
        self.browser.get(self.base_url + "/demo/regexp.htm")
        self.assertEquals("Inner", self.browser.div("Inner").text)
        self.assertEquals("Inner", self.browser.div("/Inner/[1]").text)
        self.assertFalse(self.browser.div("/Inner/[3]").exists())
        
        self.assertTrue(self.browser.link("/Vi/[0]").get_attribute("href").find("0.htm")!=-1)
        self.assertTrue(self.browser.link("View[1]").get_attribute("href").find("1.htm")!=-1)
        self.assertTrue(self.browser.link("/Vi/[2]").get_attribute("href").find("2.htm")!=-1)
        self.assertTrue(self.browser.link("View[3]").get_attribute("href").find("3.htm")!=-1)

    def test_accessors(self):
        print "Starting test_accessors"
        self.browser.get(self.base_url  + "/demo/formTest.htm")
        self.browser.alert.accept()
        self.assertEqual("", self.browser.textbox("t1").value)
        assert(self.browser.textbox(1).exists())
        assert(self.browser.textbox("$a_dollar").exists())
        self.browser.textbox("$a_dollar").value = "adas"
        
        self.assertEqual("adas", self.browser.textbox({"name" : "$a_dollar"}).value)
        self.assertFalse(self.browser.textbox({"name" : "$a_dollar", "unknownattribute" : "random"}).exists())
        
        self.assertEqual("", self.browser.textbox(1).value)
        assert(self.browser.textarea("ta1").exists())
        self.assertEqual("", self.browser.textarea("ta1").value)
        assert(self.browser.textarea(1).exists())
        self.assertEqual("", self.browser.textarea(1).value)
        assert(self.browser.checkbox("c1").exists())
        self.assertEqual("cv1", self.browser.checkbox("c1").value)
        assert(self.browser.checkbox(1).exists())
        self.assertEqual("cv2", self.browser.checkbox(1).value)
        assert(self.browser.checkbox("c1[1]").exists())
        self.assertEqual("cv3", self.browser.checkbox("c1[1]").value)
        assert(self.browser.checkbox(3).exists())
        self.assertEqual("", self.browser.checkbox(3).value)
        assert(self.browser.radio("r1").exists())
        self.assertEqual("rv1", self.browser.radio("r1").value)
        assert(self.browser.password("p1").exists())
        self.assertEqual("", self.browser.password("p1").value)
        assert(self.browser.password(1).exists())
        self.assertEqual("", self.browser.password(1).value)
        assert(self.browser.select("s1").exists())
        self.assertEqual("o1", self.browser.select("s1").selected)
        assert(self.browser.select("s1Id[1]").exists())
        self.assertEqual("o1", self.browser.select("s1Id[1]").selected)
        assert(self.browser.select(2).exists())
        self.assertEqual("o1", self.browser.select(2).selected)
        assert(self.browser.button("button value").exists())
        assert(self.browser.button("btnName[1]").exists())
        assert(self.browser.button("btnId[2]").exists())
        assert(self.browser.button(3).exists())
        assert(self.browser.submit("Add").exists())
        assert(self.browser.submit("submitBtnName[1]").exists())
        assert(self.browser.submit("submitBtnId[2]").exists())
        assert(self.browser.submit(3).exists())
        assert(self.browser.image("imageAlt1").exists())
        assert(self.browser.image("imageId1[1]").exists())
        assert(self.browser.image(2).exists())
        assert(not self.browser.link("Back22").exists())
        assert(self.browser.link("Back").exists())
            
            
    
    
    def test_select(self):
        print "Starting test_select"
        self.browser.get(self.base_url  + "/demo/formTest.htm")
        self.browser.alert.accept()
        self.assertEqual("o1", self.browser.select("s1Id[1]").value)
        self.browser.select("s1Id[1]").value = "o2"
        self.assertEqual("o2", self.browser.select("s1Id[1]").value)
        self.browser.select("s1Id[1]").selected = "o3"
        self.assertEqual("o3", self.browser.select("s1Id[1]").selected)
    
    
    
    def test_clicks(self):
        print "Starting test_clicks"
        self.browser.get(self.base_url  + "/demo/formTest.htm")
        self.browser.alert.accept()
        self.assertIsNotNone(self.browser.checkbox("c1"))
        self.browser.checkbox("c1").click()
        self.assertEqual(True, self.browser.checkbox("c1").is_selected())
        self.browser.checkbox("c1").click()
        self.assertEqual(False, self.browser.checkbox("c1").is_selected())
    
        self.assertIsNotNone(self.browser.radio("r1"))
        self.browser.radio("r1").click()
        self.assertEqual(True, self.browser.radio("r1").is_selected())
        assert(self.browser.radio("r1").is_selected())
        assert(not self.browser.radio("r1[1]").is_selected())
        self.browser.radio("r1[1]").click()
        self.assertEqual(False, self.browser.radio("r1").is_selected())
        assert(self.browser.radio("r1[1]").is_selected())
        assert(not self.browser.radio("r1").is_selected())
    

    def test_links(self):
        print "Starting test_links"
        self.browser.get(self.base_url  + "/demo/index.htm")
        self.browser.link("Link Test").click()
        self.browser.link("linkByContent").click()
        self.browser.link("Back").click()
        self.browser.link("link with return true").click()
        self.browser.alert.accept()
        assert(self.browser.textarea("ta1"))
        self.assertEqual("", self.browser.textarea("ta1").value)
        self.browser.link("Back").click()
        self.browser.link("Link Test").click()
        self.browser.link("link with return false").click()
        assert(self.browser.textbox("t1"))
        self.assertEqual("formTest link with return false", self.browser.textbox("t1").value)
        assert(self.browser.link("linkByContent"))
    
        # TODO: Figure out why these aren't working
#        self.browser.link("link with returnValue=false").click()
#        self.browser.alert.accept()
#        assert(self.browser.textbox("t1"))        
#        self.assertEqual("formTest link with returnValue=false", self.browser.textbox("t1").value)
#        self.browser.link("added handler using js").click()
#        assert(self.browser.textbox("t1"))
#        self.assertEqual("myFn called", self.browser.textbox("t1").value)
#        self.browser.textbox("t1").value = ""
        self.browser.image("imgWithLink").click()
        self.browser.link("Link Test").click()
        self.browser.image("imgWithLinkNoClick").click()
        assert(self.browser.textbox("t1"))
        self.assertEqual("myFn called", self.browser.textbox("t1").value)
        self.browser.link("Back").click()
    
    
    
    def test_exists(self):
        print "Starting test_exists"
        self.browser.get(self.base_url  + "/demo/index.htm")
        assert(self.browser.link("Link Test").exists())
        assert(not self.browser.link("Link Test NonExistent").exists())
    
    
    def alert1(self, message):
        self.browser.get(self.base_url  + "/demo/alertTest.htm")
        self.browser.textbox("t1").value = ("Message " + message)
        self.browser.button("Click For Alert").click()
        
        # TODO: This is a limitation of the javascript version.
        # Changing pages deletes your last alert
        # Maybe I can set a cookie to store selenium variables
    #        self.browser.get(self.base_url  + "/demo/alertTest.htm")
        time.sleep(1)
        
        self.assertEqual("Message " + message, self.browser.last_alert())
        self.browser.clear_last_alert()
        self.assertIsNone(self.browser.last_alert())
    

    def test_alert(self):
        print "Starting test_alert"
        self.browser.quit()
        self.browser = webdriver.Firefox(capabilities = {'suppressAlerts' : True})
        
        self.alert1("One")
        self.alert1("Two")
        self.alert1("Three")
        self.browser.button("Click For Multiline Alert").click()
        self.assertEqual("You must correct the following Errors:\nYou must select a messaging price plan.\nYou must select an international messaging price plan.\nYou must enter a value for the Network Lookup Charge", self.browser.last_alert())

    def test_confirm(self):
        print "Starting test_confirm"
        self.browser.quit()
        self.browser = webdriver.Firefox(capabilities = {'suppressConfirms' : True})
        
        self.browser.get(self.base_url  + "/demo/confirmTest.htm")
    #        self.browser.expect_confirm("Some question?", True)
        self.browser.button("Click For Confirm").click()
        self.assertEqual("oked", self.browser.textbox("t1").value)
        
        # TODO: same limitation as alert
    #        self.browser.get(self.base_url  + "/demo/confirmTest.htm")
        time.sleep(1)
        self.assertEqual("Some question?", self.browser.last_confirm())
        self.browser.clear_last_confirm()
        self.assertIsNone(self.browser.last_confirm())
        
        self.browser.confirm_action = False
    #        self.browser.expect_confirm("Some question?", False)
        self.browser.button("Click For Confirm").click()
        self.assertEqual("canceled", self.browser.textbox("t1").value)
        self.assertEqual("Some question?", self.browser.last_confirm())
        self.browser.clear_last_confirm()
        self.assertIsNone(self.browser.last_confirm())
        
        self.browser.confirm_action = True
    #        self.browser.expect_confirm("Some question?", True)
        self.browser.button("Click For Confirm").click()
        self.assertEqual("oked", self.browser.textbox("t1").value)
        self.assertEqual("Some question?", self.browser.last_confirm())
        self.browser.clear_last_confirm()
        self.assertIsNone(self.browser.last_confirm())
    
    
    def test_prompt(self):
        print "Starting test_prompt"
        
        self.browser.quit()
        self.browser = webdriver.Firefox(capabilities = {'suppressPrompts' : True})
        
        self.browser.get(self.base_url  + "/demo/promptTest.htm")
    #        self.browser.expect_prompt("Some prompt?", "abc")
        self.browser.prompt_text = "abc"
        self.browser.button("Click For Prompt").click()
        self.assertIsNotNone(self.browser.textbox("t1"))
        self.assertEqual("abc", self.browser.textbox("t1").value)
        # TODO: limitation
    #        self.browser.get("/demo/promptTest.htm")
    #        self.browser.waitFor(2)
        self.assertEqual("Some prompt?", self.browser.last_prompt())
        self.browser.clear_last_prompt()
        self.assertIsNone(self.browser.last_prompt())
    
#    def test_different_domains(self):
#        print "Starting test_different_domains"
#        self.browser.get("{0}/demo/".format(self.base_url))
#        self.browser.link("Different Domains External").click()
##        domain_tyto = self.browser.domain("www.tytosoftware.com")
##        domain_bing = self.browser.domain("www.bing.com")
#        
#        # Get the domains instaed of the urls
#        tyto_domain = "http://www.tytosoftware.com/demo/"
#        bing_domain = "http://www.bing.com/"
#        
#        self.browser.select_domain(tyto_domain)
#        self.browser.link("Link Test").click()
#        
#        self.browser.select_domain(bing_domain)
#        #self.browser.searchbox("q").value = "fdsfsd"
#        self.browser.textbox("q").value = "fdsfsd"
#    
#        self.browser.select_domain(tyto_domain)
#        self.browser.link("Back").click()
#        
#        self.browser.select_domain(bing_domain)
#        self.browser.submit("go").click()
#    
#        self.browser.get("{0}/demo/".format(self.base_url))
    
    
    def test_check(self):
        print "Starting test_check"
        self.browser.get(self.base_url  + "/demo/")
        self.browser.link("Form Test").click()
        self.browser.alert.accept()
        assert(not self.browser.checkbox("c1").is_selected())
        self.browser.checkbox("c1").check()
        assert(self.browser.checkbox("c1").is_selected())
        self.browser.checkbox("c1").check()
        assert(self.browser.checkbox("c1").is_selected())
        self.browser.checkbox("c1").uncheck()
        assert(not self.browser.checkbox("c1").is_selected())
        self.browser.checkbox("c1").uncheck()
        assert(not self.browser.checkbox("c1").is_selected())
        self.browser.checkbox("c1").click()
        assert(self.browser.checkbox("c1").is_selected())
        
#    def test_slow_loading(self):
#        self.browser.get("http://run.plnkr.co/TLyvY48ndLJDsfKz/")
#        self.assertTrue(not self.browser.image("10000ms.gif").is_displayed())
#        self.browser.submit("Click Me").click()
#        self.assertTrue(self.browser.image("10000ms.gif").is_displayed())
    
#    def test_title(self):
#        print "Starting test_title"
#        self.browser.get(self.base_url  + "/demo/index.htm")
#        self.assertEqual("Sahi Tests", self.browser.title)
#        self.browser.link("Form Test").click()        
#        self.browser.alert.accept()
#        self.assertEqual("Form Test", self.browser.title)
#        self.browser.link("Back").click()
#        self.browser.link("Window Open Test With Title").click()
#        self.browser.select_window("With Title")
#        self.assertEqual("With Title", self.browser.title)
#        self.browser.select_window("")
#        self.assertEqual("Sahi Tests", self.browser.title)
    
    

#    def test_dragdrop(self):
#        print "Starting test_dragdrop"
#        self.browser.get("http://www.snook.ca/technical/mootoolsdragdrop/")
#        self.browser.div("Drag me").drag_and_drop(self.browser.div("Item 2"))
#        assert(self.browser.div("dropped").exists())
#        assert(self.browser.div("Item 1").exists())
#        assert(self.browser.div("Item 3").exists())
#        assert(self.browser.div("Item 4").exists())
    
    
    
    def test_google(self):
        print "Starting test_google"
        self.browser.get("http://www.google.com")
        self.browser.textbox("q").value = "sahi forums"
    #        self.browser.submit("Google Search").click()
        self.browser.submit("btnG").click()
    #        self.browser.submit("gbqfb").click()
        self.browser.link("All Discussions - Sahi Forums").click()
        self.browser.link("Sign In").click()
    #        assert(self.browser.textbox("Form/Email").is_displayed())
    
    def test_dblclick(self):
        print "Starting test_dblclick"
        self.browser.get("{0}/demo/clicks.htm".format(self.base_url))
        self.browser.div("dbl click me").double_click()
        self.assertEqual("[DOUBLE_CLICK]", self.browser.textarea("t2").value)
        self.browser.button("Clear").click()
    
    
    def test_right_click(self):
        print "Starting test_right_click"
        self.browser.get("{0}/demo/clicks.htm".format(self.base_url))
        self.browser.div("right click me").right_click()
        self.assertEqual("[RIGHT_CLICK]", self.browser.textarea("t2").value)
        self.browser.button("Clear").click()

if __name__ == '__main__':
    unittest.main()
#    fast = unittest.TestSuite()
#    fast.addTests(TestPytanium('browser_js'))
#    unittest.TextTestRunner().run(fast)