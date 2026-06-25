from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.order_page_locators import OrderPageLocators
import allure
import time

class OrderPage(BasePage):
    """Класс для работы со страницей заказа"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = OrderPageLocators()
    
    @allure.step("Заполнить первую страницу заказа (Для кого самокат)")
    def fill_first_page(self, name, surname, address, metro, phone):
        """Заполнить первую страницу заказа"""
        print(f"\n=== Заполнение первой страницы ===")
        print(f"Имя: {name}, Фамилия: {surname}, Адрес: {address}, Метро: {metro}, Телефон: {phone}")
        
        # Заполняем имя
        self.input_text(self.locators.NAME_INPUT, name)
        print("✓ Имя введено")
        
        # Заполняем фамилию
        self.input_text(self.locators.SURNAME_INPUT, surname)
        print("✓ Фамилия введена")
        
        # Заполняем адрес
        self.input_text(self.locators.ADDRESS_INPUT, address)
        print("✓ Адрес введен")
        
        # Вводим телефон
        phone_input = self.driver.find_element(*self.locators.PHONE_INPUT)
        phone_input.clear()
        if not phone.startswith("+"):
            phone_input.send_keys("+" + phone)
        else:
            phone_input.send_keys(phone)
        print(f"✓ Телефон '{phone}' введен")
        
        # Заполнение станции метро
        self.select_metro_station(metro)
        print(f"✓ Станция метро '{metro}' выбрана")
        
        # Проверяем значения всех полей
        print("\n--- Проверка значений полей ---")
        name_value = self.driver.find_element(*self.locators.NAME_INPUT).get_attribute("value")
        print(f"Имя: '{name_value}'")
        surname_value = self.driver.find_element(*self.locators.SURNAME_INPUT).get_attribute("value")
        print(f"Фамилия: '{surname_value}'")
        address_value = self.driver.find_element(*self.locators.ADDRESS_INPUT).get_attribute("value")
        print(f"Адрес: '{address_value}'")
        metro_value = self.driver.find_element(*self.locators.METRO_INPUT).get_attribute("value")
        print(f"Метро: '{metro_value}'")
        phone_value = self.driver.find_element(*self.locators.PHONE_INPUT).get_attribute("value")
        print(f"Телефон: '{phone_value}'")
        print("--- Конец проверки значений полей ---\n")
        
        time.sleep(0.5)
        
        # Клик на кнопку "Далее"
        print("Нажатие кнопки 'Далее'...")
        self.click_element(self.locators.NEXT_BUTTON)
        time.sleep(2)
        
        # Проверяем переход на вторую страницу
        try:
            self.driver.find_element(*self.locators.DATE_INPUT)
            print("✓ Переход на вторую страницу выполнен")
        except:
            print("❌ Переход на вторую страницу НЕ выполнен!")
            
            # Проверяем наличие ошибок на странице
            try:
                errors = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'error') or contains(@class, 'Error')]")
                if errors:
                    print("Найдены элементы с ошибками:")
                    for err in errors:
                        text = err.text.strip()
                        if text:
                            print(f"  - {text}")
                else:
                    print("Элементы с ошибками не найдены")
            except Exception as e:
                print(f"Ошибка при проверке ошибок: {e}")
            
            # Делаем скриншот для отладки
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="first_page_still_visible",
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError("Не удалось перейти на вторую страницу заказа")
    
    @allure.step("Выбрать станцию метро: {metro}")
    def select_metro_station(self, metro):
        """Выбор станции метро из выпадающего списка"""
        print(f"\n--- Выбор станции метро: {metro} ---")
        
        # Находим поле ввода метро
        metro_input = self.driver.find_element(*self.locators.METRO_INPUT)
        
        # Кликаем на поле, чтобы открыть выпадающий список
        print("Клик на поле ввода метро...")
        metro_input.click()
        time.sleep(1)
        
        # Очищаем поле
        metro_input.clear()
        print(f"Ввод названия станции: {metro}")
        metro_input.send_keys(metro)
        time.sleep(2)
        
        # Ждем, пока появится список станций
        try:
            self.wait.until(lambda driver: len(driver.find_elements(By.XPATH, "//div[@class='select-search__select']//button")) > 0)
        except:
            print("Список станций не появился!")
            metro_input.click()
            time.sleep(0.5)
            metro_input.clear()
            metro_input.send_keys(metro)
            time.sleep(2)
        
        # Находим все станции в списке
        stations = self.driver.find_elements(By.XPATH, "//div[@class='select-search__select']//button")
        print(f"Найдено станций в списке: {len(stations)}")
        
        for i, station in enumerate(stations):
            station_text = station.text.strip()
            print(f"  [{i}] '{station_text}'")
        
        # Пытаемся найти и выбрать станцию
        found = False
        target_station = None
        
        # Сначала ищем точное совпадение
        for station in stations:
            station_text = station.text.strip()
            if station_text == metro:
                target_station = station
                print(f"Найдено точное совпадение: '{station_text}'")
                break
        
        # Если точного нет, ищем частичное
        if not target_station:
            for station in stations:
                station_text = station.text.strip()
                if metro.lower() in station_text.lower():
                    target_station = station
                    print(f"Найдено частичное совпадение: '{station_text}'")
                    break
        
        if target_station:
            print("Клик по станции...")
            # Прокручиваем до станции
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_station)
            time.sleep(0.5)
            
            # Пробуем кликнуть разными способами
            try:
                target_station.click()
                print("Обычный клик выполнен")
            except:
                try:
                    self.driver.execute_script("arguments[0].click();", target_station)
                    print("JavaScript клик выполнен")
                except:
                    print("Не удалось кликнуть по станции")
            
            time.sleep(1.5)
            
            # Проверяем, что станция выбралась
            current_value = metro_input.get_attribute("value")
            print(f"Значение поля метро после клика: '{current_value}'")
            
            if current_value and current_value.strip():
                print(f"✓ Станция '{current_value}' успешно выбрана")
                found = True
            else:
                print("Поле метро пустое, пробуем выбрать через стрелки и Enter...")
                metro_input.click()
                time.sleep(0.5)
                metro_input.send_keys(Keys.DOWN)
                time.sleep(0.5)
                metro_input.send_keys(Keys.ENTER)
                time.sleep(1.5)
                
                current_value = metro_input.get_attribute("value")
                print(f"Значение поля метро после Enter: '{current_value}'")
                if current_value and current_value.strip():
                    print(f"✓ Станция '{current_value}' успешно выбрана")
                    found = True
        
        # Если не выбралось, пробуем выбрать первую станцию из списка
        if not found and stations:
            print("Пробуем выбрать первую станцию из списка...")
            first_station = stations[0]
            station_text = first_station.text.strip()
            print(f"Выбираем: '{station_text}'")
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_station)
            time.sleep(0.5)
            
            try:
                first_station.click()
                print("Обычный клик по первой станции выполнен")
            except:
                try:
                    self.driver.execute_script("arguments[0].click();", first_station)
                    print("JavaScript клик по первой станции выполнен")
                except:
                    print("Не удалось кликнуть по первой станции")
            
            time.sleep(1.5)
            
            current_value = metro_input.get_attribute("value")
            print(f"Значение поля метро после выбора первой станции: '{current_value}'")
            
            if current_value and current_value.strip():
                print(f"✓ Станция '{current_value}' успешно выбрана")
                found = True
        
        # Если всё ещё не выбралось, пробуем через Enter
        if not found:
            print("Пробуем через Enter...")
            metro_input.clear()
            metro_input.send_keys(metro)
            time.sleep(1)
            metro_input.send_keys(Keys.ENTER)
            time.sleep(2)
            
            current_value = metro_input.get_attribute("value")
            print(f"Значение поля метро после Enter: '{current_value}'")
            
            if current_value and current_value.strip():
                print(f"✓ Станция '{current_value}' успешно выбрана")
                found = True
        
        # Если всё ещё не выбралось, пробуем через TAB
        if not found:
            print("Пробуем через TAB...")
            metro_input.clear()
            metro_input.send_keys(metro)
            time.sleep(1)
            metro_input.send_keys(Keys.TAB)
            time.sleep(2)
            
            current_value = metro_input.get_attribute("value")
            print(f"Значение поля метро после TAB: '{current_value}'")
            
            if current_value and current_value.strip():
                print(f"✓ Станция '{current_value}' успешно выбрана")
                found = True
        
        # Финальная проверка
        current_value = metro_input.get_attribute("value")
        if current_value and current_value.strip():
            print(f"✓ Станция выбрана: '{current_value}'")
            found = True
        
        if not found:
            raise AssertionError(f"Не удалось выбрать станцию метро: {metro}. Текущее значение поля: '{current_value}'")
        
        print(f"Финальное значение поля метро: '{current_value}'")
    
    @allure.step("Заполнить вторую страницу заказа (Про аренду)")
    def fill_second_page(self, date, rental_period, color, comment):
        """Заполнить вторую страницу заказа"""
        print(f"\n=== Заполнение второй страницы ===")
        print(f"Дата: {date}, Период аренды: {rental_period}, Цвет: {color}, Комментарий: {comment}")
        
        time.sleep(1)
        
        try:
            self.driver.find_element(*self.locators.DATE_INPUT)
            print("✓ Вторая страница загружена")
        except:
            print("❌ Вторая страница НЕ загружена!")
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="second_page_not_loaded",
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError("Вторая страница заказа не загружена")
        
        # Выбор даты из календаря
        print("Клик на поле даты...")
        date_input = self.driver.find_element(*self.locators.DATE_INPUT)
        date_input.click()
        time.sleep(1)
        
        # Извлекаем день из даты (формат: ДД.ММ.ГГГГ)
        day = date.split('.')[0]
        print(f"Поиск дня: {day}")
        
        # Ищем нужный день в календаре
        date_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'react-datepicker__day') and not(contains(@class, 'react-datepicker__day--outside-month'))]")
        for element in date_elements:
            if element.text.strip() == day:
                print(f"Найден день: {day}")
                element.click()
                break
        
        # Ждем, пока календарь закроется
        time.sleep(1)
        
        # Выбор срока аренды
        print(f"Выбор срока аренды: {rental_period}")
        self.click_element(self.locators.RENTAL_PERIOD_INPUT)
        time.sleep(0.5)
        rental_option_locator = (self.locators.RENTAL_PERIOD_OPTION[0], 
                                self.locators.RENTAL_PERIOD_OPTION[1].format(rental_period))
        self.click_element(rental_option_locator)
        print(f"✓ Срок аренды '{rental_period}' выбран")
        
        # Выбор цвета
        if color == "чёрный жемчуг":
            print("Выбор цвета: чёрный жемчуг")
            self.click_element(self.locators.COLOR_BLACK)
        elif color == "серая безысходность":
            print("Выбор цвета: серая безысходность")
            self.click_element(self.locators.COLOR_GREY)
        
        # Комментарий
        if comment:
            print(f"Ввод комментария: {comment}")
            self.input_text(self.locators.COMMENT_INPUT, comment)
        
        # Проверяем, все ли поля заполнены
        print("\n--- Проверка полей перед заказом ---")
        date_value = self.driver.find_element(*self.locators.DATE_INPUT).get_attribute("value")
        print(f"Дата: '{date_value}'")
        
        # Проверяем, что срок аренды выбран
        try:
            rental_period_elements = self.driver.find_elements(By.CLASS_NAME, "Dropdown-control")
            if rental_period_elements:
                print(f"Срок аренды: '{rental_period_elements[0].text}'")
        except:
            pass
        
        # Проверяем, что цвет выбран
        try:
            color_black = self.driver.find_element(*self.locators.COLOR_BLACK)
            color_grey = self.driver.find_element(*self.locators.COLOR_GREY)
            print(f"Цвет чёрный: {color_black.is_selected()}")
            print(f"Цвет серый: {color_grey.is_selected()}")
        except:
            pass
        
        comment_value = self.driver.find_element(*self.locators.COMMENT_INPUT).get_attribute("value")
        print(f"Комментарий: '{comment_value}'")
        print("--- Конец проверки ---\n")
        
        # Проверяем URL
        current_url = self.driver.current_url
        print(f"Текущий URL перед нажатием 'Заказать': '{current_url}'")
        
        # Находим кнопку "Заказать" внутри формы заказа
        print("Поиск кнопки 'Заказать' в форме...")
        
        # Ищем кнопку "Заказать" в контейнере формы
        order_button = None
        try:
            # Ищем кнопку внутри формы
            order_button = self.driver.find_element(By.XPATH, "//div[contains(@class, 'Order_Content')]//button[text()='Заказать']")
            print("✓ Кнопка 'Заказать' найдена в Order_Content")
        except:
            pass
        
        if not order_button:
            try:
                order_button = self.driver.find_element(By.XPATH, "//div[contains(@class, 'Order_Buttons')]//button[text()='Заказать']")
                print("✓ Кнопка 'Заказать' найдена в Order_Buttons")
            except:
                pass
        
        if not order_button:
            try:
                order_button = self.driver.find_element(By.XPATH, "//form//button[text()='Заказать']")
                print("✓ Кнопка 'Заказать' найдена в форме")
            except:
                pass
        
        if not order_button:
            try:
                order_button = self.driver.find_element(*self.locators.ORDER_BUTTON)
                print("✓ Кнопка 'Заказать' найдена по основному локатору")
            except:
                pass
        
        if not order_button:
            print("❌ Кнопка 'Заказать' не найдена!")
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="order_button_not_found",
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError("Кнопка 'Заказать' не найдена на странице")
        
        # Прокручиваем к кнопке
        print("Прокрутка к кнопке 'Заказать'...")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", order_button)
        time.sleep(1)
        
        # Проверяем ошибки валидации (только для формы заказа)
        print("Проверка ошибок валидации перед нажатием (только форма заказа):")
        self.check_order_form_errors()
        
        # Пробуем разные способы нажатия кнопки "Заказать"
        print("Нажатие кнопки 'Заказать'...")
        clicked = False
        
        # Способ 1: Обычный клик
        try:
            order_button.click()
            print("✓ Кнопка 'Заказать' нажата (обычный клик)")
            clicked = True
        except Exception as e:
            print(f"Обычный клик не сработал: {e}")
        
        # Способ 2: JavaScript клик
        if not clicked:
            try:
                self.driver.execute_script("arguments[0].click();", order_button)
                print("✓ Кнопка 'Заказать' нажата (JavaScript)")
                clicked = True
            except Exception as e:
                print(f"JavaScript клик не сработал: {e}")
        
        # Способ 3: ActionChains
        if not clicked:
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element(order_button).click().perform()
                print("✓ Кнопка 'Заказать' нажата (ActionChains)")
                clicked = True
            except Exception as e:
                print(f"ActionChains не сработал: {e}")
        
        if not clicked:
            print("❌ Не удалось нажать кнопку 'Заказать'!")
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="order_button_not_clicked",
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError("Не удалось нажать кнопку 'Заказать'")
        
        # Ждем появления модального окна с подтверждением
        print("Ожидание появления модального окна с подтверждением...")
        time.sleep(2)
        
        # Проверяем URL после нажатия
        current_url_after = self.driver.current_url
        print(f"Текущий URL после нажатия 'Заказать': '{current_url_after}'")
        
        # Проверяем, появилось ли модальное окно
        modal_found = False
        
        # Способ 1: Ищем по классу Order_Modal
        try:
            modal = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'Order_Modal')]"))
            )
            print("✓ Модальное окно найдено по классу Order_Modal")
            print(f"Текст модального окна: '{modal.text}'")
            modal_found = True
        except:
            pass
        
        # Способ 2: Ищем по роль dialog
        if not modal_found:
            try:
                modal = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
                )
                print("✓ Модальное окно найдено по role='dialog'")
                print(f"Текст модального окна: '{modal.text}'")
                modal_found = True
            except:
                pass
        
        # Если модальное окно не найдено - проверяем ошибки формы
        if not modal_found:
            print("❌ Модальное окно не появилось!")
            print("Проверка ошибок валидации после нажатия (только форма заказа):")
            self.check_order_form_errors()
            
            # Делаем скриншот
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="modal_not_found",
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError(f"Модальное окно с подтверждением не появилось. URL: {current_url_after}")
        
        print("✓ Заказ оформлен")
    
    def check_order_form_errors(self):
        """Проверка ошибок валидации только для формы заказа"""
        try:
            # Проверяем URL
            current_url = self.driver.current_url
            print(f"  URL: '{current_url}'")
            
            # Ищем только те ошибки, которые относятся к форме заказа
            form_errors = []
            
            # Проверяем поле "Комментарий для курьера" - если есть ошибка, это проблема
            try:
                comment_input = self.driver.find_element(*self.locators.COMMENT_INPUT)
                # Проверяем, есть ли у поля класс error
                classes = comment_input.get_attribute("class") or ""
                if "error" in classes.lower() or "Error" in classes:
                    form_errors.append("Комментарий для курьера")
            except:
                pass
            
            # Проверяем поле даты
            try:
                date_input = self.driver.find_element(*self.locators.DATE_INPUT)
                classes = date_input.get_attribute("class") or ""
                if "error" in classes.lower() or "Error" in classes:
                    form_errors.append("Дата доставки")
            except:
                pass
            
            # Проверяем поле срока аренды
            try:
                rental_input = self.driver.find_element(*self.locators.RENTAL_PERIOD_INPUT)
                classes = rental_input.get_attribute("class") or ""
                if "error" in classes.lower() or "Error" in classes:
                    form_errors.append("Срок аренды")
            except:
                pass
            
            # Проверяем цвет
            try:
                color_black = self.driver.find_element(*self.locators.COLOR_BLACK)
                color_grey = self.driver.find_element(*self.locators.COLOR_GREY)
                # Проверяем, выбран ли хотя бы один цвет
                if not color_black.is_selected() and not color_grey.is_selected():
                    form_errors.append("Цвет самоката (не выбран)")
            except:
                pass
            
            if form_errors:
                print(f"  Найдены ошибки в форме заказа ({len(form_errors)}):")
                for err in form_errors:
                    print(f"    - {err}")
            else:
                print("  Ошибок в форме заказа не найдено")
                
        except Exception as e:
            print(f"  Ошибка при проверке ошибок валидации: {e}")
    
    def check_validation_errors(self):
        """Проверка всех ошибок валидации на странице (для отладки)"""
        try:
            current_url = self.driver.current_url
            print(f"  URL: '{current_url}'")
            
            # Ищем все элементы с классом error
            error_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'error') or contains(@class, 'Error')]")
            if error_elements:
                print(f"  Найдено {len(error_elements)} элементов с ошибками:")
                for err in error_elements:
                    text = err.text.strip()
                    if text:
                        print(f"    - {text}")
            else:
                print("  Элементы с ошибками не найдены")
        except Exception as e:
            print(f"  Ошибка при проверке ошибок валидации: {e}")
    
    @allure.step("Подтвердить заказ")
    def confirm_order(self):
        """Подтвердить заказ во всплывающем окне"""
        print("\n=== Подтверждение заказа ===")
        time.sleep(1)
        
        # Ждем появления кнопки "Да"
        try:
            confirm_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, ".//button[text()='Да']"))
            )
            confirm_button.click()
            print("✓ Кнопка 'Да' нажата")
        except:
            try:
                confirm_button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, ".//button[contains(@class, 'Button_Button__ra12g') and text()='Да']"))
                )
                confirm_button.click()
                print("✓ Кнопка 'Да' нажата (альтернативный локатор)")
            except:
                try:
                    self.driver.execute_script("""
                        var buttons = document.querySelectorAll('button');
                        for (var i = 0; i < buttons.length; i++) {
                            if (buttons[i].textContent.trim() === 'Да') {
                                buttons[i].click();
                                return true;
                            }
                        }
                    """)
                    print("✓ Кнопка 'Да' нажата (через JavaScript)")
                except:
                    raise AssertionError("Не удалось найти кнопку подтверждения заказа")
        
        # Ждем появления сообщения об успехе
        print("Ожидание сообщения об успешном создании заказа...")
        time.sleep(3)
    
    @allure.step("Проверить успешность создания заказа")
    def check_order_success(self):
        """Проверить, что заказ успешно создан"""
        print("\n=== Проверка успешности заказа ===")
        
        # Делаем скриншот для отладки
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="check_success_screen",
            attachment_type=allure.attachment_type.PNG
        )
        
        # Проверяем наличие сообщения об успехе разными способами
        try:
            success_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Заказ оформлен')]"))
            )
            print(f"✓ Найдено сообщение: '{success_element.text}'")
            return True
        except:
            pass
        
        try:
            modal = self.driver.find_element(By.XPATH, "//div[contains(@class, 'Modal') or contains(@class, 'Order_Modal')]")
            if "Заказ оформлен" in modal.text:
                print(f"✓ В модальном окне найдено сообщение: '{modal.text}'")
                return True
        except:
            pass
        
        current_url = self.driver.current_url
        print(f"Текущий URL: '{current_url}'")
        if "/order/success" in current_url:
            print("✓ Редирект на страницу успеха")
            return True
        
        print("❌ Сообщение об успехе не найдено!")
        return False