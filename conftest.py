import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import os

@pytest.fixture(scope="function")
def driver():
    """Фикстура для создания и закрытия драйвера Firefox"""
    # Настройка опций для Firefox
    options = Options()
    # options.add_argument("--headless")  # Раскомментировать для headless режима
    
    # Использование локального geckodriver
    driver_path = os.path.join(os.path.dirname(__file__), "drivers", "geckodriver.exe")
    service = Service(driver_path)
    
    # Создание драйвера
    driver = webdriver.Firefox(service=service, options=options)
    driver.maximize_window()
    
    yield driver
    
    # Закрытие браузера
    driver.quit()