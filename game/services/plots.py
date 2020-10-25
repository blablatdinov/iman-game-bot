import io

import matplotlib.pyplot as plt
import pandas as pd
from math import pi
from loguru import logger

log = logger.bind(task="statistic")


def create_statistic_plot(prev_values, now_values):
    """
    Функция принимает в кач-ве аргументов 2 именованных кортежа и по ним создает график

    В кортежах должны быть поля: body, spirit, soul

    """
    styles = ['Solarize_Light2', '_classic_test_patch', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-dark', 'seaborn-dark-palette', 'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid', 'tableau-colorblind10']
    plt.style.use(styles[25])
# 10
# 21
# 22
# 25
    df = pd.DataFrame({
        'group': ['A','B'],
        'тело': [prev_values[0], now_values[0]],
        'душа': [prev_values[1], now_values[1]],
        'дух': [prev_values[2], now_values[2]],
    })
    from pprint import pprint
    pprint(df)

    categories=list(df)[1:]
    N = len(categories)

    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    ax = plt.subplot(111, polar=True)

    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    plt.xticks(angles[:-1], categories)

    ax.set_rlabel_position(0)
    plt.yticks([20,40,60,80,100], ["20","40","60","80","100"], color="grey", size=7)
    plt.ylim(0,100)

    values=df.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="Прошлый замер")
    ax.fill(angles, values, 'yellow', alpha=0.1)

    values=df.loc[1].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="Сейчас")
    ax.fill(angles, values, 'black', alpha=0.1)

    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf

