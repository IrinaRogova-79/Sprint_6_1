from selenium.webdriver.common.by import By

class OrderPageLocators:
    """Локаторы для страницы заказа"""
    
    # Первая страница заказа - "Для кого самокат"
    NAME_INPUT = (By.XPATH, ".//input[@placeholder='* Имя']")
    SURNAME_INPUT = (By.XPATH, ".//input[@placeholder='* Фамилия']")
    ADDRESS_INPUT = (By.XPATH, ".//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_INPUT = (By.XPATH, ".//input[@placeholder='* Станция метро']")
    PHONE_INPUT = (By.XPATH, ".//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.XPATH, ".//button[text()='Далее']")
    
    # Вторая страница заказа - "Про аренду"
    DATE_INPUT = (By.XPATH, ".//input[@placeholder='* Когда привезти самокат']")
    RENTAL_PERIOD_INPUT = (By.CLASS_NAME, "Dropdown-control")
    RENTAL_PERIOD_OPTION = (By.XPATH, ".//div[contains(@class, 'Dropdown-option') and text()='{}']")
    COLOR_BLACK = (By.ID, "black")
    COLOR_GREY = (By.ID, "grey")
    COMMENT_INPUT = (By.XPATH, ".//input[@placeholder='Комментарий для курьера']")
    ORDER_BUTTON = (By.XPATH, ".//button[contains(@class, 'Button_Button__ra12g') and text()='Заказать']")
    
    # Подтверждение заказа
    CONFIRM_ORDER_BUTTON = (By.XPATH, ".//button[text()='Да']")
    CONFIRM_ORDER_BUTTON_ALT = (By.XPATH, ".//button[contains(@class, 'Button_Button__ra12g') and text()='Да']")
    
    # Сообщение об успешном создании заказа - исправленные локаторы
    ORDER_SUCCESS_MESSAGE = (By.XPATH, ".//div[contains(@class, 'Order_ModalHeader__3FDaJ')]")
    ORDER_SUCCESS_MESSAGE_ALT = (By.XPATH, ".//div[contains(text(), 'Заказ оформлен')]")
    ORDER_SUCCESS_MESSAGE_ALT2 = (By.XPATH, ".//div[contains(@class, 'Order_Modal')]//div[contains(text(), 'Заказ оформлен')]")
    ORDER_MODAL = (By.XPATH, ".//div[contains(@class, 'Order_Modal')]")