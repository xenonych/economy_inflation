"""
Модуль построения графиков Plotly.
"""

import plotly.express as px
import plotly.graph_objects as go


# =========================================================
# ГРАФИК ЗАРПЛАТ
# =========================================================

def create_salary_chart(combined, chart_style, base_year):
    """
    График сравнения
    номинальных и реальных зарплат.
    """

    fig = px.line(
            combined,
            x="Год",
            y="Зарплата",
            color="Отрасль",
            line_dash="Тип",
            markers=True,
            title=f"Зарплаты (база {base_year})"
        )


    fig.update_layout(
        hovermode="x unified"
    )

    return fig


# =========================================================
# ЛИНИЯ ИНФЛЯЦИИ
# =========================================================

def add_inflation_line(fig, inflation_df):
    """
    Добавление линии инфляции.
    """

    fig.add_trace(
        go.Scatter(
            x=inflation_df["Год"],
            y=inflation_df["Инфляция"],
            mode="lines+markers",
            name="Инфляция",
            line=dict(
                dash="dash",
                color="red"
            )
        )
    )

    return fig


# =========================================================
# ГРАФИК ТЕМПОВ РОСТА
# =========================================================

def create_growth_chart(growth_long):
    """
    График темпов роста зарплат.
    """

    fig = px.line(
        growth_long,
        x="Год",
        y="Рост, %",
        color="Отрасль",
        markers=True,
        labels={
            "Год": "Год",
            "Рост, %": "Рост, %"
        }
    )

    return fig





# =========================================================
# ГРАФИК ИНДЕКСА ЗАРПЛАТ
# =========================================================

def create_index_chart(index_long, cum_infl_df):
    """
    График индекса зарплат
    и накопленной инфляции.
    """

    fig = px.line(
        index_long,
        x="Год",
        y="Индекс зарплат",
        color="Отрасль",
        markers=True,
        labels={
            "Индекс зарплат":
                "Индекс",

            "Год":
                "Год"
        }
    )

    fig.add_trace(
        go.Scatter(
            x=cum_infl_df["Год"],
            y=cum_infl_df["Индекс цен"],
            mode="lines+markers",
            name="Инфляция (индекс цен)"
        )
    )
    return fig


# =========================================================
# ГРАФИК ТОПА РОСТА
# =========================================================

def create_top_growth_chart(growth_df, title):
    """
    Горизонтальный график
    лидеров роста зарплат.
    """

    fig = px.bar(
        growth_df,
        x="Рост",
        y="Отрасль",
        orientation="h",
        title=title
    )

    fig.update_layout(
        yaxis={
            "categoryorder":
                "total ascending"
        }
    )
    return fig

# =========================================================
# BOXPLOT
# =========================================================

def create_boxplot(box_data, box_year):
    """
    Boxplot распределения зарплат.
    """
    fig = px.box(
        y=box_data,
        points="all",
        labels={
            "y": "Зарплата, ₽"
        },
        title=(
            "Распределение зарплат "
            f"по отраслям в {box_year} году"
        )
    )
    return fig