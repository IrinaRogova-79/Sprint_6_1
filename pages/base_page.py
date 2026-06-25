from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure
import time

class BasePage:
    """Базовый класс для всех страниц"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
    
    @allure.step("Открыть страницу {url}")
    def open_page(self, url):
        """Открыть страницу по URL"""
        self.driver.get(url)
        time.sleep(2)  # Даем странице загрузиться
    
    @allure.step("Найти элемент: {locator}")
    def find_element(self, locator):
        """Найти элемент с ожиданием его видимости"""
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    @allure.step("Найти несколько элементов: {locator}")
    def find_elements(self, locator):
        """Найти несколько элементов"""
        return self.driver.find_elements(*locator)
    
    @allure.step("Кликнуть на элемент: {locator}")
    def click_element(self, locator, timeout=10):
        """Кликнуть на элемент с обработкой перекрытия"""
        try:
            # Ждем, пока элемент станет кликабельным
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable(locator))
            element.click()
            return
        except Exception as e:
            # Если не получилось, пробуем через JavaScript
            try:
                element = self.driver.find_element(*locator)
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                time.sleep(0.5)
                self.driver.execute_script("arguments[0].click();", element)
                return
            except Exception as e2:
                # Пробуем скрыть баннер куки
                try:
                    self.hide_cookie_banner()
                    time.sleep(0.5)
                    element = self.driver.find_element(*locator)
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", element)
                    return
                except Exception as e3:
                    raise AssertionError(f"Не удалось кликнуть на элемент: {locator}. Ошибки: {e}, {e2}, {e3}")
    
    @allure.step("Ввести текст в поле: {locator}")
    def input_text(self, locator, text):
        """Ввести текст в поле ввода"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    @allure.step("Получить текст элемента: {locator}")
    def get_text(self, locator):
        """Получить текст элемента"""
        try:
            element = self.find_element(locator)
            return element.text
        except:
            return ""
    
    @allure.step("Проверить видимость элемента: {locator}")
    def is_element_visible(self, locator, timeout=10):
        """Проверить, видим ли элемент"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    @allure.step("Проверить, что элемент присутствует: {locator}")
    def is_element_present(self, locator):
        """Проверить, присутствует ли элемент в DOM"""
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False
    
    @allure.step("Получить текущий URL")
    def get_current_url(self):
        """Получить текущий URL страницы"""
        return self.driver.current_url
    
    @allure.step("Переключиться на новую вкладку")
    def switch_to_new_window(self):
        """Переключиться на новую вкладку"""
        self.driver.switch_to.window(self.driver.window_handles[1])
    
    @allure.step("Закрыть текущую вкладку и вернуться на предыдущую")
    def close_current_window(self):
        """Закрыть текущую вкладку и вернуться на предыдущую"""
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
    
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
            time.sleep(0.5)
        except:
            pass