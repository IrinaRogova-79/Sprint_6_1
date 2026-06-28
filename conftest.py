import os
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

BROWSER = os.getenv("BROWSER", "firefox")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"


def get_firefox_driver():
    """Создание Firefox драйвера"""
    options = FirefoxOptions()
    if HEADLESS:
        options.add_argument("--headless")
    
    try:
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)
    except:
        return webdriver.Firefox(options=options)


def get_chrome_driver():
    """Создание Chrome драйвера"""
    options = ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless")
    
    try:
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    except:
        return webdriver.Chrome(options=options)


@pytest.fixture(scope="function")
def driver():
    """Фикстура для создания и закрытия драйвера"""
    if BROWSER.lower() == "chrome":
        driver = get_chrome_driver()
    else:
        driver = get_firefox_driver()
    
    driver.maximize_window()
    yield driver
    driver.quit()