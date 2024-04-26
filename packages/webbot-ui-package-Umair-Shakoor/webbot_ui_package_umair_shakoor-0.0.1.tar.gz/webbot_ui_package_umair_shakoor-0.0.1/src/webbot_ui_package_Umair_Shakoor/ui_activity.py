from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class UIActivity:
        
    def __init__(self, driver):
        self.driver = driver
        self.root_window_handle = driver.current_window_handle
        self.action = ActionChains(driver)
    
    def hover_on(self, by, element_name, parent_element=None):
        element = self.get_element(by, element_name, parent_element)
        self.action.move_to_element(element)
        self.action.perform()
    
    def dummy_send(self, element, word, delay, append=False):
        if not append:
            element.clear()
        for c in word:
            element.send_keys(c)
            sleep(delay)

    def switch_to_frame(self, frame_index):
        try:
            self.driver.switch_to.frame(frame_index)
            sleep(3)
        except Exception as e:
            raise(e)
    
    def switch_to_default_frame(self):
            self.driver.switch_to.default_content()
    
    def switch_to_window(self, window_index):
        try:
            all_handles = self.driver.window_handles
            self.driver.switch_to.window(all_handles[window_index])
            sleep(3)
        except Exception as e:
            raise(e)
        
    def switch_to_default_window(self):
            self.driver.switch_to.window(self.root_window_handle)
        
    def highlight(self, element, effect_time, color, border):
        driver = element._parent
        def apply_style(s):
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                element, s)
        original_style = element.get_attribute('style')
        apply_style("border: {0}px solid {1};".format(border, color))
        sleep(effect_time)
        apply_style(original_style)

    def write_on(self, by, element_name, element_value, append=False, parent_element=None):
        element = self.click_on(by, element_name, parent_element)    
        self.dummy_send(element, element_value, 0.1, append)

    def click_on(self, by, element_name, parent_element=None):
        element = self.get_element(by, element_name, parent_element)
        element.click()
    
        return element

    def get_elements(self, by, element_name):
        elements = self.driver.find_elements(by, element_name)
        
        return elements
    
    def get_element(self, by, element_name, parent_element=None):
        element_finder = parent_element if parent_element is not None else self.driver
        element = element_finder.find_element(by, element_name)
        self.highlight(element, 3, "blue", 5)
    
        return element

    def delay_click_on(self, by, element_name, time_out):
        try:    
            self.wait_for_element_appear(by, element_name, time_out)
            self.click_on(by, element_name)
        except Exception as e:
            raise(e)

    def wait_for_url_change(self, time_out):
        try:
            WebDriverWait(self.driver, time_out).until(EC.url_changes(self.driver.current_url))
        except Exception as e:
            raise(e)

    def wait_for_element_appear(self, by, element_name, time_out):
        try:    
            element_locator = (by, element_name)
            WebDriverWait(self.driver, time_out).until(EC.element_to_be_clickable(element_locator))
        except Exception as e:
            raise(e)

    def wait_for_element_disappear(self, by, element_name, time_out):
        try:    
            element_locator = (by, element_name)
            WebDriverWait(self.driver, time_out).until_not(EC.visibility_of_element_located(element_locator))
        except Exception as e:
            raise(e)