from .base_page import BasePage  # Если base_page.py находится в той же папке
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class OrderStatusPage(BasePage):

    # Локаторы
    PHONE_INPUT_LOCATOR = (By.XPATH, "//input[@id='client_phone']")
    LOGIN_LINK_LOCATOR = (By.XPATH, "//a[contains(@class, 'js-modal-toggler') and @data-target='.co-modal--login']")
    MODAL_WINDOW_LOCATOR = (By.XPATH, "//div[contains(@class, 'co-modal--login')]")
    MODAL_TITLE_LOCATOR = (By.XPATH, ".//h3[contains(@class, 'co-modal-title')]")
    EMAIL_INPUT_LOCATOR = (By.XPATH, ".//input[@name='email' and @type='text']")
    PASSWORD_INPUT_LOCATOR = (By.XPATH, ".//input[@name='psw' and @type='password']")
    LOGIN_BUTTON_LOCATOR = (By.XPATH, ".//button[contains(@class, 'js-modal-submit--login')]")
    CLOSE_MODAL_BUTTON_LOCATOR = (By.XPATH, "//button[contains(@class, 'co-modal-close')]")
    DELIVERY_LOCATION_INPUT_LOCATOR = (By.XPATH, "//input[@id='shipping_address_full_locality_name']")
    DELIVERY_ERROR_MESSAGE_LOCATOR = (By.XPATH,
                                      "//div[@id='delivery-location-not-valid' and contains(text(), 'Ошибка! Не удалось определить населенный пункт')]")
    TOTAL_PRICE_LOCATOR = (By.XPATH, "//div[@id='total_price']")
    DELIVERY_OPTION_LOCATOR = (By.XPATH, "//*[@id='delivery_variants']/div[2]/label[2]/span[1]/span")
    CLIENT_NAME_INPUT_LOCATOR = (By.XPATH, "//input[@id='client_name']")
    CONFIRM_ORDER_BUTTON_LOCATOR = (
    By.XPATH, "//button[@id='create_order' and contains(@class, 'js-button-checkout_submit')]")
    CLIENT_NAME_ERROR_LOCATOR = (By.CSS_SELECTOR, '.co-input-notice.co-notice--danger')
    #CLIENT_NAME_ERROR_MESSAGE_LOCATOR = (By.XPATH,
#"//div[contains(@class, 'co-input-notice co-notice--danger') and contains(text(), 'Не заполнено обязательное поле')]")

    # Локатор для проверки страницы оформления заказа
    CHECKOUT_PAGE_LOCATOR = "//h1[contains(@class, 'co-title') and contains(text(), 'Оформление заказа')]"
    DELIVERY_LOCATION_INPUT_LOCATOR = (By.XPATH, "//input[@id='shipping_address_full_locality_name']")
    DELIVERY_ERROR_MESSAGE_LOCATOR = (By.XPATH,
                                      "//div[@id='delivery-location-not-valid' and contains(text(), 'Ошибка! Не удалось определить населенный пункт')]")
    # Ожидаемая часть URL
    expected_url_part = "/payments/"

    def is_checkout_page(self):
        try:
            # Проверка, что элемент с заголовком оформления заказа присутствует на странице
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.CHECKOUT_PAGE_LOCATOR))
            )
            return True
        except TimeoutException:
            return False

    # Ваши другие методы остаются без изменений

    def enter_phone_number(self, phone_number):
        self.send_keys(self.PHONE_INPUT_LOCATOR, phone_number)
        print(f"Номер телефона '{phone_number}' введен в поле.")

    def click_login_link(self):
        self.click_element(self.LOGIN_LINK_LOCATOR)
        print("Клик по ссылке 'Уже покупали у нас?' выполнен.")

    def verify_modal_window(self):
        modal_window = self.wait_for_element_visible(self.MODAL_WINDOW_LOCATOR)
        assert modal_window.is_displayed(), "Модальное окно 'Для постоянных покупателей' не отображается."
        print("Модальное окно 'Для постоянных покупателей' успешно отображается.")

    def verify_modal_contents(self):
        modal_window = self.find_element(self.MODAL_WINDOW_LOCATOR)
        modal_title = modal_window.find_element(*self.MODAL_TITLE_LOCATOR)
        assert modal_title.text == "Для постоянных покупателей", "Заголовок модального окна не соответствует ожидаемому."
        print("Заголовок модального окна корректен.")

        email_input = modal_window.find_element(*self.EMAIL_INPUT_LOCATOR)
        password_input = modal_window.find_element(*self.PASSWORD_INPUT_LOCATOR)
        login_button = modal_window.find_element(*self.LOGIN_BUTTON_LOCATOR)

        assert email_input.is_displayed(), "Поле для ввода email/телефона отсутствует в модальном окне."
        assert password_input.is_displayed(), "Поле для ввода пароля отсутствует в модальном окне."
        assert login_button.is_displayed(), "Кнопка 'Войти' отсутствует в модальном окне."
        print("Модальное окно содержит необходимые элементы: поле email, поле пароля и кнопку 'Войти'.")

    def close_modal_window(self):
        try:
            close_button = self.find_element(self.CLOSE_MODAL_BUTTON_LOCATOR)
            close_button.click()
            print("Модальное окно успешно закрыто.")
        except Exception:
            # Если кнопка закрытия недоступна, удаляем модальное окно через JavaScript
            modal_window = self.find_element(self.MODAL_WINDOW_LOCATOR)
            self.driver.execute_script("arguments[0].remove();", modal_window)
            print("Модальное окно закрыто с использованием JavaScript.")

    def enter_city(self, city_name):
        # Сохраняем текущее значение телефона
        phone_value = self.find_element(self.PHONE_INPUT_LOCATOR).get_attribute("value")

        # Очистка и ввод города
        city_input_field = self.find_element(self.DELIVERY_LOCATION_INPUT_LOCATOR)
        self.driver.execute_script("arguments[0].value = '';", city_input_field)
        self.send_keys(self.DELIVERY_LOCATION_INPUT_LOCATOR, city_name)
        self.click_body()

        # Восстановление значения телефона, если оно пропало
        if self.find_element(self.PHONE_INPUT_LOCATOR).get_attribute("value") != phone_value:
            self.send_keys(self.PHONE_INPUT_LOCATOR, phone_value)
            print(f"Поле телефона восстановлено: {phone_value}")

        print(f"Город '{city_name}' введен в поле.")

    def verify_city_error_message(self, expected_text):
        error_message = self.find_element(self.DELIVERY_ERROR_MESSAGE_LOCATOR)
        assert expected_text in error_message.text, f"Ошибка: сообщение '{error_message.text}' не содержит '{expected_text}'."
        print(f"Сообщение об ошибке для города '{expected_text}' отображено корректно.")

    def remove_suggestions(self):
        # Клик по телу страницы, чтобы закрыть подсказки
        self.driver.find_element(By.TAG_NAME, "body").click()
        print("Подсказки закрыты.")

    def wait_for_error_message_to_appear(self):
        try:
            # Ожидание появления сообщения об ошибке
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.DELIVERY_ERROR_MESSAGE_LOCATOR)
            )
            print("Сообщение об ошибке появилось.")
        except TimeoutException:
            print("Ошибка не появилась вовремя.")

    # Пример исправления в методе, где возникает ошибка

    def get_total_price(self):
        price_text = self.get_text(self.TOTAL_PRICE_LOCATOR).replace("руб", "").replace("\u00a0", "").strip()
        try:
            price = float(price_text)  # Преобразуем строку в число
            return price
        except ValueError:
            print(f"Ошибка преобразования цены '{price_text}' в число.")
            return 0.0  # Возвращаем 0.0, если преобразование не удалось

    def select_delivery_option(self):
        try:
            delivery_option = self.find_element(self.DELIVERY_OPTION_LOCATOR)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", delivery_option)
            self.driver.execute_script("arguments[0].click();", delivery_option)
            print("Радио-кнопка доставки успешно выбрана.")
        except Exception as e:
            print(f"Не удалось выбрать вариант доставки: {e}")

    def enter_client_name(self, name):
        """Метод для ввода имени клиента в соответствующее поле"""
        self.send_keys(self.CLIENT_NAME_INPUT_LOCATOR, name)
        print(f"Имя клиента '{name}' введено в поле.")

    def click_confirm_order(self):
        """Метод для клика по кнопке 'Подтвердить заказ'"""
        self.click_element(self.CONFIRM_ORDER_BUTTON_LOCATOR)
        print("Кнопка 'Подтвердить заказ' нажата.")



    def check_url_change(self, expected_substring):
        try:
            # Сохраняем текущий URL перед действием
            current_url = self.driver.current_url

            # Кликаем по кнопке "Оформить заказ"
            confirm_order_button = self.find_element(self.CONFIRM_ORDER_BUTTON_LOCATOR)
            confirm_order_button.click()
            print("Кнопка 'Оформить заказ' нажата.")

            # Ожидаем, что URL изменится
            WebDriverWait(self.driver, 30).until(
                lambda driver: expected_substring in driver.current_url and driver.current_url != current_url
            )

            print(f"URL изменился, текущий URL: {self.driver.current_url}")
            return True
        except Exception as e:
            print(f"Ошибка при проверке изменения URL: {e}")
            return False
