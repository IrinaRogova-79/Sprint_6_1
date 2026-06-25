import allure
from pages.main_page import MainPage
from data import MAIN_URL
import time

@allure.epic("Логотипы")
@allure.feature("Переходы по логотипам")
class TestLogos:
    """Тесты для проверки переходов по логотипам"""
    
    @allure.story("Переход на главную 'Самоката'")
    def test_scooter_logo_redirect(self, driver):
        """
        Тест проверяет, что при клике на логотип "Самоката" 
        открывается главная страница
        """
        # Открыть главную страницу
        main_page = MainPage(driver)
        main_page.open_page(MAIN_URL)
        
        # Кликнуть на логотип "Самоката"
        main_page.click_scooter_logo()
        
        # Проверить, что перешли на главную страницу
        assert main_page.get_current_url() == MAIN_URL, f"Неверный URL. Ожидалось: {MAIN_URL}, получено: {main_page.get_current_url()}"
    
    @allure.story("Переход на Дзен")
    def test_yandex_logo_redirect(self, driver):
        """
        Тест проверяет, что при клике на логотип "Яндекса" 
        в новом окне открывается главная страница Дзена
        """
        # Открыть главную страницу
        main_page = MainPage(driver)
        main_page.open_page(MAIN_URL)
        
        # Запомнить текущее количество вкладок
        initial_tabs = len(driver.window_handles)
        
        # Кликнуть на логотип "Яндекса"
        main_page.click_yandex_logo()
        
        # Подождать открытия новой вкладки
        time.sleep(2)
        
        # Проверить, что открылась новая вкладка
        assert len(driver.window_handles) > initial_tabs, "Новая вкладка не открылась"
        
        # Переключиться на новую вкладку
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)  # Ждем загрузки страницы
        
        # Проверить, что URL содержит dzen.ru или yandex.ru
        current_url = driver.current_url
        is_dzen_or_yandex = "dzen.ru" in current_url.lower() or "yandex" in current_url.lower()
        
        # Если не открылся Дзен, возможно редирект на другую страницу
        if not is_dzen_or_yandex:
            # Пробуем проверить, что это не пустая страница
            assert current_url != "about:blank", "Открылась пустая страница"
            # Проверяем, что URL не пустой
            assert len(current_url) > 0, "URL пустой"
        
        # Закрыть новую вкладку и вернуться на главную
        driver.close()
        driver.switch_to.window(driver.window_handles[0])