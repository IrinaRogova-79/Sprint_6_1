from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.order_page_locators import OrderPageLocators
import allure


class OrderPage(BasePage):
    """Класс для работы со страницей заказа"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = OrderPageLocators()
    
    @allure.step("Заполнить поле имени: {name}")
    def _fill_name(self, name):
        """Заполнить поле имени"""
        self.input_text(self.locators.NAME_INPUT, name)
    
    @allure.step("Заполнить поле фамилии: {surname}")
    def _fill_surname(self, surname):
        """Заполнить поле фамилии"""
        self.input_text(self.locators.SURNAME_INPUT, surname)
    
    @allure.step("Заполнить поле адреса: {address}")
    def _fill_address(self, address):
        """Заполнить поле адреса"""
        self.input_text(self.locators.ADDRESS_INPUT, address)
    
    @allure.step("Заполнить поле телефона: {phone}")
    def _fill_phone(self, phone):
        """Заполнить поле телефона"""
        phone_input = self.find_element(self.locators.PHONE_INPUT)
        phone_input.clear()
        if not phone.startswith("+"):
            phone_input.send_keys("+" + phone)
        else:
            phone_input.send_keys(phone)
    
    @allure.step("Выбрать станцию метро: {metro}")
    def _select_metro_station(self, metro):
        """Выбор станции метро из выпадающего списка"""
        metro_input = self.find_element(self.locators.METRO_INPUT)
        metro_input.click()
        metro_input.clear()
        metro_input.send_keys(metro)
        
        # Ожидаем появления списка станций
        self.wait.until(
            lambda driver: len(driver.find_elements(*self.locators.METRO_STATION_LIST)) > 0
        )
        
        stations = self.find_elements(self.locators.METRO_STATION_LIST)
        
        for station in stations:
            station_text = station.text.strip()
            if station_text == metro or metro.lower() in station_text.lower():
                station.click()
                # Ожидаем, что поле заполнилось
                self.wait.until(lambda driver: metro_input.get_attribute("value") != "")
                return
        
        raise AssertionError(f"Не удалось выбрать станцию метро: {metro}")
    
    @allure.step("Нажать кнопку 'Далее'")
    def _click_next_button(self):
        """Нажать кнопку 'Далее'"""
        self.click_element(self.locators.NEXT_BUTTON)
    
    @allure.step("Ожидать загрузки второй страницы")
    def _wait_for_second_page(self):
        """Ожидать загрузки второй страницы"""
        self.wait.until(EC.visibility_of_element_located(self.locators.DATE_INPUT))
    
    @allure.step("Заполнить первую страницу заказа (Для кого самокат)")
    def fill_first_page(self, name, surname, address, metro, phone):
        """Заполнить первую страницу заказа"""
        self._fill_name(name)
        self._fill_surname(surname)
        self._fill_address(address)
        self._select_metro_station(metro)
        self._fill_phone(phone)
        self._click_next_button()
        self._wait_for_second_page()
    
    @allure.step("Выбрать дату доставки: {date}")
    def _select_date(self, date):
        """Выбор даты из календаря"""
        date_input = self.find_element(self.locators.DATE_INPUT)
        date_input.click()
        
        day = date.split('.')[0]
        
        # Ожидаем появления календаря
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "react-datepicker__day")))
        
        date_elements = self.find_elements(self.locators.DATE_DAY)
        for element in date_elements:
            if element.text.strip() == day:
                self.click_webelement_js(element)  # Используем JS клик для надёжности
                break
        
        # Ожидаем, что дата выбралась
        self.wait.until(lambda driver: date_input.get_attribute("value") != "")
    
    @allure.step("Выбрать срок аренды: {rental_period}")
    def _select_rental_period(self, rental_period):
        """Выбор срока аренды"""
        self.click_element(self.locators.RENTAL_PERIOD_INPUT)
        
        # Ожидаем появления выпадающего списка
        rental_option_locator = (
            self.locators.RENTAL_PERIOD_OPTION[0],
            self.locators.RENTAL_PERIOD_OPTION[1].format(rental_period)
        )
        self.wait.until(EC.element_to_be_clickable(rental_option_locator))
        self.click_element(rental_option_locator)
        
        # Ожидаем, что значение выбралось
        self.wait.until(
            lambda driver: driver.find_element(*self.locators.RENTAL_PERIOD_INPUT).get_attribute("value") != ""
        )
    
    @allure.step("Выбрать цвет самоката: {color}")
    def _select_color(self, color):
        """Выбор цвета самоката"""
        if color == "чёрный жемчуг":
            self.click_element(self.locators.COLOR_BLACK)
        elif color == "серая безысходность":
            self.click_element(self.locators.COLOR_GREY)
    
    @allure.step("Заполнить комментарий: {comment}")
    def _fill_comment(self, comment):
        """Заполнить поле комментария"""
        if comment:
            self.input_text(self.locators.COMMENT_INPUT, comment)
    
    @allure.step("Нажать кнопку 'Заказать' на второй странице")
    def _click_order_button(self):
        """Нажать кнопку 'Заказать'"""
        # Находим кнопку в контейнере формы
        try:
            order_button = self.find_element(self.locators.ORDER_BUTTON_IN_CONTENT)
        except:
            order_button = self.find_element(self.locators.ORDER_BUTTON_IN_BUTTONS)
        
        # Прокручиваем к кнопке
        self.scroll_to_webelement(order_button)
        
        # Ждем, пока кнопка станет кликабельной
        self.wait.until(EC.element_to_be_clickable(order_button))

        # Кликаем через JavaScript
        self.click_webelement_js(order_button)
    
    @allure.step("Ожидать появления модального окна")
    def _wait_for_modal(self):
        """Ожидать появления модального окна с подтверждением"""
        self.wait.until(EC.visibility_of_element_located(self.locators.MODAL_WINDOW))
    
    @allure.step("Заполнить вторую страницу заказа (Про аренду)")
    def fill_second_page(self, date, rental_period, color, comment):
        """Заполнить вторую страницу заказа"""
        self._select_date(date)
        self._select_rental_period(rental_period)
        self._select_color(color)
        self._fill_comment(comment)
        self._click_order_button()
        self._wait_for_modal()
    
    @allure.step("Подтвердить заказ")
    def confirm_order(self):
        """Подтвердить заказ во всплывающем окне"""
        self.wait.until(EC.element_to_be_clickable(self.locators.CONFIRM_ORDER_BUTTON))
        self.click_element(self.locators.CONFIRM_ORDER_BUTTON)
    
    @allure.step("Проверить успешность создания заказа")
    def check_order_success(self):
        """Проверить, что заказ успешно создан"""
        if self.is_element_visible(self.locators.ORDER_SUCCESS_MESSAGE, timeout=15):
            message = self.get_text(self.locators.ORDER_SUCCESS_MESSAGE)
            return "Заказ оформлен" in message
        return False