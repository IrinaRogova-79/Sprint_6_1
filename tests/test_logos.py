import allure
from pages.main_page import MainPage
from data import MAIN_URL


@allure.epic("Логотипы")
@allure.feature("Переходы по логотипам")
class TestLogos:
    """Тесты для проверки переходов по логотипам"""
    
    @allure.title("Переход на главную страницу 'Самоката' по логотипу")
    def test_scooter_logo_redirect(self, driver):
        """
        Тест проверяет, что при клике на логотип "Самоката" 
        открывается главная страница
        """
        main_page = MainPage(driver)
        main_page.open_page(MAIN_URL)
        main_page.click_scooter_logo()
        
        assert main_page.get_current_url() == MAIN_URL, \
            f"Неверный URL. Ожидалось: {MAIN_URL}, получено: {main_page.get_current_url()}"
    
    @allure.title("Переход на Дзен по логотипу Яндекса")
    def test_yandex_logo_redirect(self, driver):
        """
        Тест проверяет, что при клике на логотип "Яндекса" 
        в новом окне открывается главная страница Дзена
        """
        main_page = MainPage(driver)
        main_page.open_page(MAIN_URL)
        
        initial_tabs = len(driver.window_handles)
        main_page.click_yandex_logo()
        main_page.wait_for_new_window(initial_tabs)
        main_page.switch_to_new_window()
        
        current_url = main_page.get_current_url()
        assert "dzen.ru" in current_url.lower(), \
            f"Ожидается переход на Дзен, получено: {current_url}"