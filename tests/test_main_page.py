import allure
import pytest
from pages.main_page import MainPage
from urls import MAIN_URL
from data import FAQ_DATA


@allure.epic("Главная страница")
@allure.feature("Раздел 'Вопросы о важном'")
class TestMainPage:
    """Тесты для главной страницы"""
    
    @allure.title("Проверка ответа на вопрос №{question_index}")
    @pytest.mark.parametrize("question_index, expected_answer", 
                             [(i, answer) for i, (_, answer) in enumerate(FAQ_DATA)])
    def test_faq_answer_text(self, driver, question_index, expected_answer):
        """
        Тест проверяет, что при клике на вопрос открывается правильный ответ
        """
        main_page = MainPage(driver)
        main_page.open_page(MAIN_URL)
        main_page.click_question(question_index)
        
        assert main_page.is_answer_visible(question_index), f"Ответ на вопрос {question_index} не виден"
        
        actual_answer = main_page.get_answer_text(question_index)
        assert actual_answer == expected_answer, f"Неверный текст ответа. Ожидалось: '{expected_answer}', получено: '{actual_answer}'"