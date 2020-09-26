from pprint import pprint

from django.test import TestCase

from game.service import translate_tasks_in_keyboard, get_tasks, send_daily_tasks
from game.models import MembersGroup
from bot_init.markup import InlineKeyboard
from bot_init.models import Subscriber


class TranslateTasksInKeyboard(TestCase):

    def test_ok(self):
        tasks = (
            'first',
            'second',
            'third',
        )
        function_value = translate_tasks_in_keyboard(tasks).to_json()
        expected_value = InlineKeyboard([((x, "123"),) for x in tasks]).keyboard.to_json()
        self.assertEqual(expected_value, function_value)


# class GetTasks(TestCase):

#     def test_ok(self):
#         tasks = get_tasks()
#         self.assertEqual(tasks[0].task_type, 'body')
#         self.assertEqual(tasks[1].task_type, 'body')
#         self.assertEqual(tasks[2].task_type, 'body')
#         self.assertEqual(tasks[3].task_type, 'soul')
#         self.assertEqual(tasks[4].task_type, 'soul')
#         self.assertEqual(tasks[5].task_type, 'soul')
#         self.assertEqual(tasks[6].task_type, 'spirit')
#         self.assertEqual(tasks[7].task_type, 'spirit')
#         self.assertEqual(tasks[8].task_type, 'spirit')


class SendDailyTasks(TestCase):

    def test_ok(self):
        group = MembersGroup.objects.create(title='adsf')
        Subscriber.objects.create(tg_chat_id=358610865, members_group=group)
        send_daily_tasks()