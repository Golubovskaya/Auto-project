from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.remove_button_xpath = "//button[contains(@class, 'js-item-delete')]"  # Уникальный для корзины
        self.empty_cart_message_xpath = "//div[contains(@class, 'js-cart-empty') and contains(text(), 'Ваша корзина пуста')]"
    # Локаторы
    INCREASE_QUANTITY_BUTTON_LOCATOR = (By.XPATH, "//button[@data-quantity-change='1' and contains(@class, 'is-count-up')]")
    ADD_SECOND_PRODUCT_BUTTON_LOCATOR = (By.XPATH, "//*[@id='splide01-slide02']/div/form/div/div[4]/div/div[2]/div/button")
    CART_COUNTER_LOCATOR = (By.XPATH, "//span[@class='header__control-bage']")
    ORDER_BUTTON_LOCATOR = (By.XPATH, "//button[@data-cart-submit='' and contains(@class, 'button_size-l')]")
    PRODUCT_IN_CART_LOCATOR_TEMPLATE = "//div[@data-product-id='{}']"
    REMOVE_BUTTON_LOCATOR = (By.XPATH, "//button[contains(@class, 'js-item-delete')]")
    #REMOVE_BUTTON_LOCATOR = (By.CSS_SELECTOR, ".button js-item-delete")
    EMPTY_CART_MESSAGE_LOCATOR = (By.XPATH, "//div[contains(@class, 'js-cart-empty')]")

    # Методы
    def increase_product_quantity(self):
        self.click_element(self.INCREASE_QUANTITY_BUTTON_LOCATOR)
        print("Количество первого товара увеличено на 1.")

    def scroll_to_element(self, locator):
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def add_second_product(self):
        self.click_element(self.ADD_SECOND_PRODUCT_BUTTON_LOCATOR)
        print("Клик по кнопке добавления второго товара выполнен.")

    def get_cart_count_text(self):
        try:
            cart_counter = self.find_element(self.CART_COUNTER_LOCATOR)
            return int(cart_counter.text.strip()) if cart_counter.text.strip().isdigit() else 0
        except Exception:
            return 0

    def wait_for_cart_count_update(self, previous_count):
        WebDriverWait(self.driver, 30).until(
            lambda d: self.get_cart_count_text() > previous_count,
            message="Счетчик корзины не обновился после добавления второго товара."
        )
        print(f"Счетчик корзины обновился. Текущее количество: {self.get_cart_count_text()}")

    def verify_products_in_cart(self, product_ids):
        for product_id in product_ids:
            product_locator = (By.XPATH, self.PRODUCT_IN_CART_LOCATOR_TEMPLATE.format(product_id))
            assert self.is_element_displayed(product_locator), f"Товар с ID {product_id} не найден в корзине."
            print(f"Товар с ID {product_id} успешно находится в корзине.")

    def remove_all_items(self):
        """
        Удаляет все товары из корзины, используя JavaScript для клика по кнопкам удаления.
        """
        try:
            while True:
                # Находим все кнопки удаления
                remove_buttons = self.driver.find_elements(By.XPATH, self.remove_button_xpath)

                # Если кнопок больше нет, завершаем цикл
                if not remove_buttons:
                    print("Все товары удалены из корзины.")
                    break

                # Лог для отладки
                print(f"Найдено кнопок удаления: {len(remove_buttons)}")

                # Удаляем первый товар, используя JavaScript
                remove_button = remove_buttons[0]
                self.driver.execute_script("arguments[0].click();", remove_button)

                # Ждем, пока элемент будет удален из DOM
                WebDriverWait(self.driver, 10).until(EC.staleness_of(remove_button))
        except TimeoutException:
            print("Удаление завершено или кнопки удаления больше не доступны.")

    def is_cart_empty(self):
        """Проверяет, что корзина пуста"""
        empty_message = self.wait_for_element_visible(self.EMPTY_CART_MESSAGE_LOCATOR)
        return empty_message.is_displayed()

    def proceed_to_checkout(self):
        self.click_element(self.ORDER_BUTTON_LOCATOR)
        print("Кнопка 'Оформить заказ' нажата.")
