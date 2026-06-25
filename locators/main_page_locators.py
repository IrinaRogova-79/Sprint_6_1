from selenium.webdriver.common.by import By

class MainPageLocators:
    """Локаторы для главной страницы"""
    
    # Кнопки "Заказать"
    ORDER_BUTTON_TOP = (By.XPATH, "//div[contains(@class, 'Header_Nav__AGCXC')]//button[contains(@class, 'Button_Button__ra12g')]")
    ORDER_BUTTON_BOTTOM = (By.XPATH, "//button[contains(@class, 'Button_Button__ra12g') and text()='Заказать']")
    
    # Логотипы
    SCOOTER_LOGO = (By.XPATH, "//img[@alt='Scooter']")
    YANDEX_LOGO = (By.XPATH, "//img[@alt='Yandex']")
    
    # Вопросы и ответы
    QUESTION_TEMPLATE = (By.ID, "accordion__heading-{}")
    ANSWER_TEMPLATE = (By.ID, "accordion__panel-{}")
    
    # Баннер куки
    COOKIE_BANNER = (By.CLASS_NAME, "App_CookieConsent__1yUIN")