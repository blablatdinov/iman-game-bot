"""Начальный опрос подписчика"""
from game.models import BeginSurveyQuestion
from bot_init.markup import InlineKeyboard
from bot_init.schemas import Answer


def get_keyboard_for_question(question_pk):
    """
    Функция возвращает инлайн клавиатуру для вопросов начального тестирования

    Пример клавиатуры:
    1 2
    3 4
    5 6
    7 8
    9 10

    """
    template = 'begin_survey({}, ' + str(question_pk) + ')'
    buttons = []
    for i in range(1, 10, 2):
        i_plus = str(i + 1)
        i = str(i)
        buttons += (
            (i, template.format(i)), (i_plus, template.format(i_plus))
        ),
    keyboard = InlineKeyboard(buttons).keyboard
    return keyboard


def start_survey():
    """Функция начинает опрос"""
    survey_question = BeginSurveyQuestion.objects.filter(type="body")[0]
    keyboard = get_keyboard_for_question(survey_question.pk)
    answer = Answer(survey_question.text, keyboard=keyboard)
    answer.send(358610865)


def get_next_question(question_pk):
    """Возвращает следующий вопрос с клавиатурой"""
    survey_question = BeginSurveyQuestion.objects.get(pk=question_pk + 1)
    keyboard = get_keyboard_for_question(survey_question.pk)
    answer = Answer(survey_question.text, keyboard=keyboard)
    return answer
    