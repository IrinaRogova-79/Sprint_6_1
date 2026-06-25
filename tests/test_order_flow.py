import allure
import pytest
from pages.main_page import MainPage
from pages.order_page import OrderPage
from data import MAIN_URL, TestData
import time

@allure.epic("Сценарий заказа")
@allure.feature("Позитивный сценарий заказа самоката")
class TestOrderFlow:
    """Тесты для сценария заказа самоката"""
    
    @allure.story("Заказ с верхней кнопки")
    @pytest.mark.parametrize("order_data", [TestData.ORDER_DATA_1, TestData.ORDER_DATA_2])
    def test_order_from_top_button(self, driver, order_data):
        """
        Тест проверяет позитивный сценарий заказа самоката 
        через верхнюю кнопку "Заказать"
        """
        # Открыть главную страницу
        main_page = MainPage(driver)
        main_page.open_page(MAIN_URL)
        
        # Кликнуть на верхнюю кнопку "Заказать"
        main_page.click_order_button_top()
        
        # Заполнить первую страницу заказа
        order_page = OrderPage(driver)
        order_page.fill_first_page(
            order_data["name"],
            order_data["surname"],
            order_data["address"],
            order_data["metro"],
            order_data["phone"]
        )
        
        # Заполнить вторую страницу заказа
        order_page.fill_second_page(
            order_data["date"],
            order_data["rental_period"],
            order_data["color"],
            order_data["comment"]
        )
        
        # Подтвердить заказ
        order_page.confirm_order()
        
        # Проверить, что заказ успешно создан
        assert order_page.check_order_success(), "Сообщение об успешном создании заказа не появилось"
    
    @allure.story("Заказ с нижней кнопки")
    @pytest.mark.parametrize("order_data", [TestData.ORDER_DATA_1, TestData.ORDER_DATA_2])
    def test_order_from_bottom_button(self, driver, order_data):
        """
        Тест проверяет позитивный сценарий заказа самоката 
        через нижнюю кнопку "Заказать"
        """
        # Открыть главную страницу
        main_page = MainPage(driver)
        main_page.open_page(MAIN_URL)
        
        # Кликнуть на нижнюю кнопку "Заказать"
        main_page.click_order_button_bottom()
        
        # Заполнить первую страницу заказа
        order_page = OrderPage(driver)
        order_page.fill_first_page(
            order_data["name"],
            order_data["surname"],
            order_data["address"],
            order_data["metro"],
            order_data["phone"]
        )
        
        # Заполнить вторую страницу заказа
        order_page.fill_second_page(
            order_data["date"],
            order_data["rental_period"],
            order_data["color"],
            order_data["comment"]
        )
        
        # Подтвердить заказ
        order_page.confirm_order()
        
        # Проверить, что заказ успешно создан
        assert order_page.check_order_success(), "Сообщение об успешном создании заказа не появилось"