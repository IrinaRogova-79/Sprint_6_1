from selenium.webdriver.common.by import By

class MainPageLocators:
    """Локаторы для главной страницы"""
    
    # Кнопки "Заказать"
    ORDER_BUTTON_TOP = (By.XPATH, "//button[text()='Заказать']")
    ORDER_BUTTON_BOTTOM = (By.XPATH, "//button[contains(@class, 'Button_Button__ra12g') and text()='Заказать']")
    
    # Логотипы
    SCOOTER_LOGO = (By.XPATH, "//img[@alt='Scooter']")
    YANDEX_LOGO = (By.XPATH, "//img[@alt='Yandex']")
    
    # Раздел "Вопросы о важном"
    FAQ_SECTION = (By.CLASS_NAME, "Home_FourPart__1uthg")
    
    # Вопросы и ответы
    QUESTION_TEMPLATE = (By.ID, "accordion__heading-{}")
    ANSWER_TEMPLATE = (By.ID, "accordion__panel-{}")