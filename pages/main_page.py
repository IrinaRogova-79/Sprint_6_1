from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators
import allure

class MainPage(BasePage):
    """Класс для работы с главной страницей"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = MainPageLocators()
    
    @allure.step("Скрыть баннер куки")
    def hide_cookie_banner(self):
        """Скрыть баннер с куки"""
        try:
            self.driver.execute_script("""
                var cookieBanner = document.querySelector('.App_CookieConsent__1yUIN');
                if (cookieBanner) {
                    cookieBanner.style.display = 'none';
                }
            """)
        except:
            pass
    
    @allure.step("Кликнуть на кнопку 'Заказать' вверху страницы")
    def click_order_button_top(self):
        """Кликнуть на верхнюю кнопку 'Заказать'"""
        self.click_element(self.locators.ORDER_BUTTON_TOP)
    
    @allure.step("Кликнуть на кнопку 'Заказать' внизу страницы")
    def click_order_button_bottom(self):
        """Кликнуть на нижнюю кнопку 'Заказать'"""
        self.hide_cookie_banner()
        self.click_element(self.locators.ORDER_BUTTON_BOTTOM)
    
    @allure.step("Кликнуть на логотип 'Самоката'")
    def click_scooter_logo(self):
        """Кликнуть на логотип 'Самоката'"""
        self.click_element(self.locators.SCOOTER_LOGO)
    
    @allure.step("Кликнуть на логотип 'Яндекса'")
    def click_yandex_logo(self):
        """Кликнуть на логотип 'Яндекса'"""
        self.click_element(self.locators.YANDEX_LOGO)
    
    @allure.step("Кликнуть на вопрос №{question_index}")
    def click_question(self, question_index):
        """Кликнуть на вопрос по индексу"""
        self.hide_cookie_banner()
        question_locator = (self.locators.QUESTION_TEMPLATE[0], 
                           self.locators.QUESTION_TEMPLATE[1].format(question_index))
        self.scroll_to_element(question_locator)
        self.click_element(question_locator)
    
    @allure.step("Получить текст ответа на вопрос №{question_index}")
    def get_answer_text(self, question_index):
        """Получить текст ответа на вопрос по индексу"""
        answer_locator = (self.locators.ANSWER_TEMPLATE[0], 
                         self.locators.ANSWER_TEMPLATE[1].format(question_index))
        self.wait.until(EC.visibility_of_element_located(answer_locator))
        return self.get_text(answer_locator)
    
    @allure.step("Проверить видимость ответа на вопрос №{question_index}")
    def is_answer_visible(self, question_index):
        """Проверить, виден ли ответ на вопрос"""
        answer_locator = (self.locators.ANSWER_TEMPLATE[0], 
                         self.locators.ANSWER_TEMPLATE[1].format(question_index))
        return self.is_element_visible(answer_locator)