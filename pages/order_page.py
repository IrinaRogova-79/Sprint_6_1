from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage
from locators.order_page_locators import OrderPageLocators
import allure

class OrderPage(BasePage):
    """Класс для работы со страницей заказа"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = OrderPageLocators()
    
    def _fill_name(self, name):
        self.input_text(self.locators.NAME_INPUT, name)
    
    def _fill_surname(self, surname):
        self.input_text(self.locators.SURNAME_INPUT, surname)
    
    def _fill_address(self, address):
        self.input_text(self.locators.ADDRESS_INPUT, address)
    
    def _fill_phone(self, phone):
        phone_input = self.find_element(self.locators.PHONE_INPUT)
        phone_input.clear()
        if not phone.startswith("+"):
            phone_input.send_keys("+" + phone)
        else:
            phone_input.send_keys(phone)
    
    def _select_metro_station(self, metro):
        """Выбор станции метро из выпадающего списка"""
        metro_input = self.find_element(self.locators.METRO_INPUT)
        metro_input.click()
        
        metro_input.clear()
        metro_input.send_keys(metro)
        
        self.wait.until(lambda driver: len(driver.find_elements(By.XPATH, "//div[@class='select-search__select']//button")) > 0)
        
        stations = self.find_elements((By.XPATH, "//div[@class='select-search__select']//button"))
        
        for station in stations:
            station_text = station.text.strip()
            if station_text == metro or metro.lower() in station_text.lower():
                self.scroll_to_element((By.XPATH, f"//div[@class='select-search__select']//button[contains(text(), '{station_text}')]"))
                station.click()
                return
        
        raise AssertionError(f"Не удалось выбрать станцию метро: {metro}")
    
    def _click_next_button(self):
        self.click_element(self.locators.NEXT_BUTTON)
    
    def _wait_for_second_page(self):
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
        date_input = self.find_element(self.locators.DATE_INPUT)
        date_input.click()
        
        day = date.split('.')[0]
        date_elements = self.find_elements((By.XPATH, "//div[contains(@class, 'react-datepicker__day') and not(contains(@class, 'react-datepicker__day--outside-month'))]"))
        for element in date_elements:
            if element.text.strip() == day:
                element.click()
                break
    
    @allure.step("Выбрать срок аренды: {rental_period}")
    def _select_rental_period(self, rental_period):
        self.click_element(self.locators.RENTAL_PERIOD_INPUT)
        rental_option_locator = (self.locators.RENTAL_PERIOD_OPTION[0], 
                                self.locators.RENTAL_PERIOD_OPTION[1].format(rental_period))
        self.click_element(rental_option_locator)
    
    @allure.step("Выбрать цвет самоката: {color}")
    def _select_color(self, color):
        if color == "чёрный жемчуг":
            self.click_element(self.locators.COLOR_BLACK)
        elif color == "серая безысходность":
            self.click_element(self.locators.COLOR_GREY)
    
    @allure.step("Заполнить комментарий: {comment}")
    def _fill_comment(self, comment):
        if comment:
            self.input_text(self.locators.COMMENT_INPUT, comment)
    
    @allure.step("Нажать кнопку 'Заказать' на второй странице")
    def _click_order_button(self):
        order_button = self.find_element(self.locators.ORDER_BUTTON)
        self.scroll_to_element(self.locators.ORDER_BUTTON)
        order_button.click()
    
    @allure.step("Ожидать появления модального окна")
    def _wait_for_modal(self):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'Order_Modal')]")))
    
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
        self.click_element(self.locators.CONFIRM_ORDER_BUTTON)
    
    @allure.step("Проверить успешность создания заказа")
    def check_order_success(self):
        """Проверить, что заказ успешно создан"""
        return self.is_element_visible(self.locators.ORDER_SUCCESS_MESSAGE, timeout=15)