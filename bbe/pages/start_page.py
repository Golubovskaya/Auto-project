from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class StartPage(BasePage):
    # Локаторы
    PRODUCT_LOCATOR = (By.XPATH, "//div[contains(@class, 'product-preview__content')]")
    ADD_TO_CART_BUTTON_LOCATOR = (By.XPATH, "//button[contains(@class, 'button_wide product-preview__buy-btn')]")
    MICRO_ALERT_LOCATOR = (By.CLASS_NAME, "micro-alert")
    CART_ICON_LOCATOR = (By.XPATH, "//a[contains(@class, 'header__control-btn header__cart')]")
    CART_COUNTER_LOCATOR = (By.XPATH, "//span[@class='header__control-bage']")

    # Методы
    def open_page(self, base_url):
        self.driver.get(base_url)

    def add_product_to_cart(self, product_xpath):
        product_locator = (By.XPATH, product_xpath)
        product_element = self.find_element(product_locator)
        self.hover_over_element(product_element)
        self.click_element(self.ADD_TO_CART_BUTTON_LOCATOR)
        alert = self.wait_for_element_visible(self.MICRO_ALERT_LOCATOR)
        assert alert.is_displayed(), "Элемент micro-alert не появился после добавления товара в корзину."

    def go_to_cart(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.invisibility_of_element_located(self.MICRO_ALERT_LOCATOR)
            )
        except TimeoutException:
            print("Элемент micro-alert не исчез, продолжаем выполнение.")

        try:
            self.click_element(self.CART_ICON_LOCATOR)
        except Exception as e:
            # Если элемент перекрыт, используем JavaScript для клика
            cart_icon = self.find_element(self.CART_ICON_LOCATOR)
            self.driver.execute_script("arguments[0].click();", cart_icon)

    def get_cart_count(self):
        try:
            cart_counter = self.find_element(self.CART_COUNTER_LOCATOR)
            count_text = cart_counter.text.strip()
            return int(count_text) if count_text.isdigit() else 0
        except Exception:
            return 0
