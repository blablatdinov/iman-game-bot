# Generated by Django 3.0.7 on 2020-09-26 09:11

from django.db import migrations


def create_daily_tasks(apps, schema_editor):
    Model = apps.get_model("game", "DailyTask")
    dict_ = {
        "body": [
            "Растяжка - Ровный руку",
            "Нейрофитнес - С мозгом на Ты ",
            "Эспандер. 100х - Нафс в крепких руках",
            "Отжимания - сильные руки для Дуа",
            "Пробежка - спешит за савабом",
            "Выпить 2 литра воды - Корабль города",
            "Турники - Подтянутый Иман",
            "Отказаться от сахара и сладкого - Не прельщен Дуньей   ",
            "Проснуться на час раньше обычного - Ранний баракат",
            "Приседы - Твердый шаг к довольству",
            "Планка - Стоек к трудностям",
            "Прогулка перед сном 20 минут -  Свежий сон",
            "Пресс - Чрево не для чрезмерного ",
            "Обливание - Закаленный льдом",
            "Совместная воинская тренировка \"I'MAN\" - Мирный воин",
            "Фруктовый день - Садовый фруктоежка",
            "Термопроцедуры. Баня, сауна, хаммам. - Закаленный жаром ",
            "Набивка - В крепком теле - крепкий Дух",
        ],
        "soul": [
            "Навести порядок. Расхламление. - В дунье налегке ",
            "Книга - Книжный барс",
            "Список долгов. Сделать одно дело из списка. - Верный слову. ",
            "Делай необычно. Новый способ сделать обычные дела. - Трансформер   ",
            "Писать все дела в течении дня. Сколько времени заняло. Тайм шит - Цена секунды ",
            "Финансовая привычка.- Финансист 2.0",
            "Встреча клуба - Место силы",
            "Работа над улучшением памяти. - Вспомнить всё",
            "Медитация, 20 минут - Обнуленный",
            "Полезные уроки. Конспект - Шакирд длинною в жизнь",
            "Отдых - Не бездельник, а восстанавливающийся",
            "Час тишины - Делу время, а тишине час",
            "10 часов без соц.сетей - Изгой-один",
            "Новое знакомство - Коммуникабельный брат",
            "Поделиться чем-то полезным из своих знаний/опыта. - стратег “Выиграл - Выиграл” ",
            "Самоанализ. Выводы за неделю. - Отчет до Дня отчета",
            "Новый источник дохода - Добытчик каменных джунглей ",
            "Полезная практика. - Гадәт файдасы",
            "Путешествие. - Мусафир по красотам Аллаха",
        ],
        "spirit": [
            "Пост - Обрадованный дважды",
            "Выучить 5 новых аятов.- Куръан хафиз",
            "1 доброе дело. - Саваб в малом",
            "Читать Куръан - наполненный чтением",
            "Прослушать урок по Фикху. - Факих истины",
            "Повторить заученные аяты, суры. - Главное, запомнить главное     ",
            "Урок Арабского языка - На языке Истины ",
            "Угостить Соседа/коллегу чем нибудь вкусным - Юмарт брат",
            "Восполнить 5 намазов. (Если нет - 5 нафиль намазов) - Нафиль PRO",
            "Ввести в практику сунну - по следам Пророка (с.г.в.)",
            "Прочитать суру Кахф после ахшама. - Озаряя пятницу",
            "Прочитать зикр. Салават - Тасбих скроллер",
            "Дать садака - Саваплы инвестор",
            "Сунна - внедрил лучший Пример ",
            "Навестить родных. Поговорить с родителями. - Баракатле кунак",
            "Урок Сиры.- Изучил лучший Пример",
            "Отказаться от обеда. - Хлебом не корми, дай Нафс укрепить!",
            "Проект \"Чистая мечеть\" - Абу Проппер",
        ]
    }
    for key, value in dict_.items():
        for elem in value:
            Model.objects.create(task_type=key, text=elem)


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_dailytask'),
    ]

    operations = [
        migrations.RunPython(create_daily_tasks)
    ]
