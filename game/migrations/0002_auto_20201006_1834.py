# Generated by Django 3.0.7 on 2020-10-06 15:34

from django.db import migrations


def create_answers(apps, schema_editor):
    Model = apps.get_model('game', 'BeginSurveyQuestion')
    dict_ = {
        "body": [
            "1. Я всегда себя прекрасно чувствую",
            "2. Я сплю 7-8 часов в день",
            "3. Я крайне редко болею",
            "4. Я регулярно занимаюсь физическими упражнениями.",
            "5. Я пью 2 литра воды в день.",
            "6. Я каждый день бываю на свежем воздухе.",
            "7. Я сбалансированно и регулярно питаюсь.",
            "8. Я регулярно принимаю контрастный душ.",
            "9. Мой вес в норме. ",
            "10. Я планирую свой отдых.",
        ],
        "soul": [
            "1. Моя основная деятельность доставляет мне удовольствие.",
            "2. Моя работа не идёт в ущерб всем другим аспектам моей жизни, включая семью.",
            "3. У меня много друзей и знакомых.",
            "4. Я понимаю, что мы все разные и мерить всех по одним стандартам не эффективно.",
            "5. Я сам делаю свою жизнь интереснее, а не жду когда что-то извне само начнёт происходить. ",
            "6. Я посвящаю достаточно времени себе.",
            "7. Я осознаю, что я сегодняшний результат не только генов и воспитания, но и моих: решений, привычек, слов и даже мыслей в прошлом.",
            "8. Я не боюсь изменений и «поворотов судьбы».",
            "9. Я открыт для конструктивной критики, и благодарен, когда близкие подсказывают и направляют меня когда я откровенно заблуждаюсь.",
            "10. Я придерживаюсь правила «Деньги - хороший слуга, но плохой господин».",
        ],
        "spirit": [
            "1. Я не пропускаю намазы и соблюдаю все предписанные обязательства религии. ",
            "2. Я стараюсь получать как можно больше знаний об Исламе. ",
            "3. Я регулярно делаю самоанализ.",
            "4. Вспоминая свою жизнь я могу с уверенностью сказать, что я могу быть благодарным и в богатстве и в бедности, и в болезни и в здравии, и в процессе и в результате, и в кругу близких и в полном одиночестве.",
            "5. Я регулярно участвую в благотворительности, безвозмездно вкладывая своё время и /или деньги на социально значимые области.",
            '6. Я прекрасно осознаю внутреннюю борьбу в моей душе и знаю свои "слабости"',
            "7. У меня есть наставник(и).",
            "8. Я регулярно заучиваю Куръан. ",
            "9. Я много делаю дополнительных поклонений. ",
            "10. Я не даю эмоциям и жизненным обстоятельствам власти над собой. Я помню что все является благом для меня.",
        ],
    }
    for key, value in dict_.items():
        for elem in value:
            Model.objects.create(type=key, text=elem)


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_answers)
    ]



