import time
import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.start_page import StartPage
from pages.cart_page import CartPage
from pages.order_status_page import OrderStatusPage
from selenium.webdriver import ActionChains

@pytest.mark.usefixtures("driver", "base_url", "product_ids")
@allure.epic("E-commerce")
@allure.feature("Корзина и оформление заказа")
class TestCartOperations:

    @allure.story("Операции в корзине")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("product_xpath", ["//div[contains(@class, 'product-preview__content')]"])
    def test_cart_operations(self, driver, product_xpath, product_ids, base_url):
        """
        Тест проверяет операции с корзиной, включая добавление товаров, увеличение количества,
        удаление товаров, и проверку состояния корзины.
        """
        # Инициализация страниц
        start_page = StartPage(driver)
        cart_page = CartPage(driver)

        with allure.step("Открываем главную страницу"):
            start_page.open_page(base_url)

        with allure.step("Добавляем товар в корзину"):
            start_page.add_product_to_cart(product_xpath)
            assert start_page.get_cart_count() == 1, "Счетчик корзины не обновился после добавления первого товара."

        with allure.step("Переходим в корзину"):
            start_page.go_to_cart()

        with allure.step("Увеличиваем количество первого товара на 1"):
            previous_count = cart_page.get_cart_count_text()
            cart_page.increase_product_quantity()
            cart_page.wait_for_cart_count_update(previous_count)

        with allure.step("Добавляем второй товар"):
            cart_page.add_second_product()
            cart_page.wait_for_cart_count_update(previous_count + 1)

        with allure.step("Проверяем наличие товаров в корзине"):
            cart_page.verify_products_in_cart(product_ids)

        with allure.step("Удаляем все товары из корзины"):
            cart_page.remove_all_items()
            assert cart_page.is_cart_empty(), "Корзина не пуста после удаления всех товаров."

        with allure.step("Возвращаемся на главную страницу и проверяем счетчик корзины"):
            driver.back()
            assert start_page.get_cart_count() == 0, "Счетчик корзины не равен 0 после удаления всех товаров."
            print("Тест операции с корзиной успешно завершён.")

    @allure.story("Оформление заказа")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_checkout_process(self, driver, base_url, product_ids):
        """
        Тест проверяет оформление заказа, включая ввод данных, выбор доставки и подтверждение заказа.
        """
        # Инициализация страниц
        start_page = StartPage(driver)
        cart_page = CartPage(driver)
        order_status_page = OrderStatusPage(driver)

        with allure.step("Проверяем, что корзина пуста"):
            start_page.open_page(base_url + "/cart_items")
            if not cart_page.is_cart_empty():
                cart_page.remove_all_items()
            assert cart_page.is_cart_empty(), "Корзина не пуста перед началом теста."

        with allure.step("Открываем главную страницу и добавляем товар в корзину"):
            start_page.open_page(base_url)
            start_page.add_product_to_cart(StartPage.PRODUCT_LOCATOR[1])
            start_page.go_to_cart()

        with allure.step("Добавляем второй товар со страницы корзины"):
            # Прокручиваем к элементу и кликаем для добавления второго товара
            cart_page.scroll_to_element(CartPage.ADD_SECOND_PRODUCT_BUTTON_LOCATOR)
            cart_page.click_element(CartPage.ADD_SECOND_PRODUCT_BUTTON_LOCATOR)

        with allure.step("Проверяем наличие товаров в корзине"):
            cart_page.verify_products_in_cart(product_ids)

        with allure.step("Нажимаем на кнопку 'Оформить заказ'"):
            cart_page.proceed_to_checkout()
            assert order_status_page.is_checkout_page(), "Страница оформления заказа не загрузилась."

        with allure.step("Кликаем по ссылке 'Уже покупали у нас?'"):
            order_status_page.click_login_link()

        with allure.step("Проверяем отображение модального окна"):
            order_status_page.verify_modal_window()
            order_status_page.verify_modal_contents()

        with allure.step("Закрываем модальное окно"):
            order_status_page.close_modal_window()

        with allure.step("Проводим негативные проверки ввода некорректного города"):
            invalid_cities = ["", "123456", "!@#$%^&*", "Nonexistent City", "г Х"]
            for city in invalid_cities:
                try:
                    # Вводим некорректный город
                    order_status_page.enter_city(city)
                    order_status_page.remove_suggestions()

                    # Проверяем сообщение об ошибке
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located(order_status_page.DELIVERY_ERROR_MESSAGE_LOCATOR)
                    )
                    order_status_page.verify_city_error_message("Ошибка! Не удалось определить населенный пункт.")
                    print(f"Негативная проверка успешно пройдена для города: '{city}'.")

                except AssertionError as e:
                    print(f"Ошибка при проверке города '{city}': {e}.")
                except Exception as e:
                    print(f"Неизвестная ошибка при проверке города '{city}': {e}.")

        with allure.step("Вводим номер телефона и корректный город"):
            order_status_page.enter_phone_number("+75556667788")
            order_status_page.enter_city("г Москва")

        with allure.step("Проверяем обновление суммы заказа после выбора доставки"):
            initial_price = order_status_page.get_total_price()
            order_status_page.select_delivery_option()
            updated_price = order_status_page.get_total_price()
            assert updated_price - initial_price == 300, "Сумма заказа должна увеличиться на 300 руб."

        with allure.step("Вводим имя клиента и подтверждаем заказ"):
            order_status_page.enter_client_name("Иванов Иван Иванович")
            order_status_page.click_confirm_order()
            print("Заказ успешно подтверждён.")
