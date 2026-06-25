import allure
import pytest
from pages.main_page import MainPage
from pages.order_page import OrderPage
from data import MAIN_URL, TestData


@allure.epic("Сценарий заказа")
@allure.feature("Позитивный сценарий заказа самоката")
class TestOrderFlow:
    """Тесты для сценария заказа самоката"""
    
    @allure.title("Заказ через верхнюю кнопку с данными: {order_data[name]}")
    @pytest.mark.parametrize("order_data", [TestData.ORDER_DATA_1, TestData.ORDER_DATA_2])
    def test_order_from_top_button(self, driver, order_data):
        """
        Тест проверяет позитивный сценарий заказа самоката 
        через верхнюю кнопку "Заказать"
        """
        main_page = MainPage(driver)
        main_page.open_page(MAIN_URL)
        main_page.click_order_button_top()
        
        order_page = OrderPage(driver)
        order_page.fill_first_page(
            order_data["name"],
            order_data["surname"],
            order_data["address"],
            order_data["metro"],
            order_data["phone"]
        )
        order_page.fill_second_page(
            order_data["date"],
            order_data["rental_period"],
            order_data["color"],
            order_data["comment"]
        )
        order_page.confirm_order()
        
        assert order_page.check_order_success(), "Сообщение об успешном создании заказа не появилось"
    
    @allure.title("Заказ через нижнюю кнопку с данными: {order_data[name]}")
    @pytest.mark.parametrize("order_data", [TestData.ORDER_DATA_1, TestData.ORDER_DATA_2])
    def test_order_from_bottom_button(self, driver, order_data):
        """
        Тест проверяет позитивный сценарий заказа самоката 
        через нижнюю кнопку "Заказать"
        """
        main_page = MainPage(driver)
        main_page.open_page(MAIN_URL)
        main_page.click_order_button_bottom()
        
        order_page = OrderPage(driver)
        order_page.fill_first_page(
            order_data["name"],
            order_data["surname"],
            order_data["address"],
            order_data["metro"],
            order_data["phone"]
        )
        order_page.fill_second_page(
            order_data["date"],
            order_data["rental_period"],
            order_data["color"],
            order_data["comment"]
        )
        order_page.confirm_order()
        
        assert order_page.check_order_success(), "Сообщение об успешном создании заказа не появилось"