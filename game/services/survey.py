"""Начальный опрос подписчика"""
from game.models import BeginSurveyAnswer
from bot_init.markup import InlineKeyboard
from bot_init.schemas import Answer


def start_survey():
    survey_answer = BeginSurveyAnswer.objects.filter(type="body")[0]
    buttons = [
        ((x, f'blabla(answer_num={survey_answer})'),) for x in range(1, 11)
    ]
    template = 'blabla({}, ' + str(survey_answer.pk) + ')'
    buttons = [
        (
            ('1', template.format('1')), ('2', template.format('2'))
        ),
        (
            ('3', template.format('3')), ('4', template.format('4'))
        ),
        (
            ('5', template.format('5')), ('6', template.format('6'))
        ),
        (
            ('7', template.format('7')), ('8', template.format('8'))
        ),
        (
            ('9', template.format('9')), ('10', template.format('10'))
        ),
    ]
    keyboard = InlineKeyboard(buttons).keyboard
    answer = Answer(survey_answer.text, keyboard=keyboard)
    answer.send(358610865)
