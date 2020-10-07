"""Начальный опрос подписчика"""
from bot_init.models import Subscriber
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


def start_survey(chat_id):
    """Функция начинает опрос"""
    survey_question = BeginSurveyQuestion.objects.filter(type="body")[0]
    keyboard = get_keyboard_for_question(survey_question.pk)
    answer = Answer(survey_question.text, keyboard=keyboard, chat_id=chat_id)
    return answer


def set_points(chat_id, question_pk, value):
    subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
    survey_question = BeginSurveyQuestion.objects.get(pk=question_pk)
    question_type = survey_question.type
    if question_type == 'body':
        subscriber.points_body += value
        subscriber.save()
    elif question_type == 'soul':
        subscriber.points_soul += value
        subscriber.save()
    elif question_type == 'spirit':
        subscriber.points_spirit += value
        subscriber.save()


def get_next_question(question_pk):
    """Возвращает следующий вопрос с клавиатурой"""
    survey_question = BeginSurveyQuestion.objects.get(pk=question_pk + 1)
    keyboard = get_keyboard_for_question(survey_question.pk)
    text = f"{survey_question.get_type_display()}\n\n{survey_question.text}"
    answer = Answer(text, keyboard=keyboard)
    return answer
