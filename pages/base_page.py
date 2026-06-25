from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure

class BasePage:
    """Базовый класс для всех страниц"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    @allure.step("Открыть страницу {url}")
    def open_page(self, url):
        """Открыть страницу по URL"""
        self.driver.get(url)
        self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    
    @allure.step("Найти элемент: {locator}")
    def find_element(self, locator, timeout=None):
        """Найти элемент с ожиданием его видимости"""
        wait = WebDriverWait(self.driver, timeout or 10)
        return wait.until(EC.visibility_of_element_located(locator))
    
    @allure.step("Найти несколько элементов: {locator}")
    def find_elements(self, locator, timeout=None):
        """Найти несколько элементов"""
        wait = WebDriverWait(self.driver, timeout or 10)
        wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)
    
    @allure.step("Кликнуть на элемент: {locator}")
    def click_element(self, locator, timeout=10):
        """Кликнуть на элемент с ожиданием кликабельности"""
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    @allure.step("Кликнуть на элемент через JavaScript")
    def click_element_js(self, locator):
        """Кликнуть на элемент через JavaScript"""
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.driver.execute_script("arguments[0].click();", element)
    
    @allure.step("Ввести текст в поле: {locator}")
    def input_text(self, locator, text):
        """Ввести текст в поле ввода"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    @allure.step("Получить текст элемента: {locator}")
    def get_text(self, locator):
        """Получить текст элемента"""
        return self.find_element(locator).text
    
    @allure.step("Проверить видимость элемента: {locator}")
    def is_element_visible(self, locator, timeout=10):
        """Проверить, видим ли элемент"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    @allure.step("Проверить присутствие элемента: {locator}")
    def is_element_present(self, locator, timeout=10):
        """Проверить, присутствует ли элемент в DOM"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    @allure.step("Прокрутить до элемента: {locator}")
    def scroll_to_element(self, locator):
        """Прокрутить до элемента"""
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    
    @allure.step("Получить текущий URL")
    def get_current_url(self):
        """Получить текущий URL страницы"""
        return self.driver.current_url
    
    @allure.step("Переключиться на новую вкладку")
    def switch_to_new_window(self):
        """Переключиться на новую вкладку"""
        self.driver.switch_to.window(self.driver.window_handles[-1])
    
    @allure.step("Закрыть новую вкладку и вернуться на главную")
    def close_current_window(self):
        """Закрыть текущую вкладку и вернуться на предыдущую"""
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
    
    @allure.step("Ожидать открытия новой вкладки")
    def wait_for_new_window(self, initial_windows_count):
        """Ожидать открытия новой вкладки"""
        self.wait.until(lambda driver: len(driver.window_handles) > initial_windows_count)