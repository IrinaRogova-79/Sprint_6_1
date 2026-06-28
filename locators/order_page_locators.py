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
    ORDER_SUCCESS_MESSAGE = (By.XPATH, ".//div[contains(@class, 'Order_ModalHeader__3FDaJ')]")
    
    # Модальное окно
    MODAL_WINDOW = (By.XPATH, "//div[contains(@class, 'Order_Modal')]")
    
    # Локаторы для списка станций метро
    METRO_STATION = (By.XPATH, "//div[@class='select-search__select']//button")
    METRO_STATION_BY_TEXT = (By.XPATH, "//div[@class='select-search__select']//button[contains(text(), '{}')]")
    METRO_STATION_LIST = (By.XPATH, "//div[@class='select-search__select']//button")
    
    # Локаторы для даты
    DATE_DAY = (By.XPATH, "//div[contains(@class, 'react-datepicker__day') and not(contains(@class, 'react-datepicker__day--outside-month'))]")
    
    # Локаторы для кнопки "Заказать" на второй странице
    ORDER_BUTTON_IN_CONTENT = (By.XPATH, "//div[contains(@class, 'Order_Content')]//button[text()='Заказать']")
    ORDER_BUTTON_IN_BUTTONS = (By.XPATH, "//div[contains(@class, 'Order_Buttons')]//button[text()='Заказать']")
    ORDER_BUTTON_IN_FORM = (By.XPATH, "//form//button[text()='Заказать']")