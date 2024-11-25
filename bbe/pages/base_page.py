from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def find_elements(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))

    def click_element(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
        element.click()

    def send_keys(self, locator, keys, timeout=10):
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(keys)

    def hover_over_element(self, element):
        ActionChains(self.driver).move_to_element(element).perform()

    def get_text(self, locator, timeout=10):
        element = self.find_element(locator, timeout)
        return element.text

    def is_element_displayed(self, locator, timeout=10):
        try:
            return self.find_element(locator, timeout).is_displayed()
        except:
            return False

    def wait_for_element_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def click_body(self):
        body = self.find_element((By.TAG_NAME, "body"))
        body.click()

