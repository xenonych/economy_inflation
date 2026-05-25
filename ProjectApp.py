import pandas as pd
import streamlit as st
import plotly.express as px
from io import BytesIO


from utils.ui import (
    setup_page,
    init_theme,
    load_css,
    show_header
)


from utils.loaders import (
    load_salary,
    load_inflation
)


from utils.calculations import (
    build_deflator,
    adjust_for_inflation,

    create_long_format,

    calculate_growth,
    prepare_growth_long,

    calculate_share_above_inflation,

    calculate_salary_index,
    prepare_index_long,

    calculate_cumulative_inflation,

    calculate_top_growth,

    prepare_boxplot_data,

    calculate_summary_metrics
)


from utils.charts import (
    create_salary_chart,
    add_inflation_line,
    create_top_growth_chart,

    create_growth_chart,


    create_boxplot
)


setup_page()
init_theme()
load_css()
show_header()

st.markdown("## Загрузка данных")


salary_file = st.file_uploader(
        "Таблица зарплат",
        type=["xlsx"]
    )
inflation_file = st.file_uploader(
        "Таблица инфляции",
        type=["xlsx"]
    )


if salary_file and inflation_file:


    salary_df = load_salary(salary_file)

    inflation_df = load_inflation(
        inflation_file
    )


    year_cols_all = [
        c for c in salary_df.columns
        if c != "Отрасль"
        and c.isdigit()
    ]

    years_in_salary = sorted(
        [int(c) for c in year_cols_all]
    )

    if not years_in_salary:
        st.error(
            """
            Не удалось найти столбцы
            с годами в файле зарплат.
            """
        )
        st.stop()
    st.success("Данные успешно загружены")



    st.sidebar.markdown(
        "## ⚙️ Параметры"
    )

    available_years = sorted(
        inflation_df["Год"].unique()
    )


    base_year = st.sidebar.selectbox(
        "Базовый год",

        options=available_years,

        index=(
            available_years.index(2020)
            if 2020 in available_years
            else 0
        )
    )

    all_sectors = (
        salary_df["Отрасль"]
        .unique()
        .tolist()
    )

    default_sectors = (
        ["Всего"]

        if "Всего" in all_sectors

        else all_sectors[:5]
    )

    selected_sectors = (
        st.sidebar.multiselect(
            "Отрасли",

            options=all_sectors,

            default=default_sectors
        )
    )


    year_range = st.sidebar.slider(
        "Диапазон лет",

        min_value=min(years_in_salary),

        max_value=max(years_in_salary),

        value=(
            min(years_in_salary),
            max(years_in_salary)
        )
    )


    filtered_salary = salary_df[
        salary_df["Отрасль"]
        .isin(selected_sectors)
    ]

    year_cols = [

        str(y)

        for y in range(
            year_range[0],
            year_range[1] + 1
        )

        if str(y) in filtered_salary.columns
    ]

    if not year_cols:

        st.error(
            "Нет данных для выбранного диапазона"
        )

        st.stop()


    df_nominal = (
        filtered_salary[
            ["Отрасль"] + year_cols
        ]
        .set_index("Отрасль")
    )

    deflator = build_deflator(
        inflation_df,
        base_year
    )


    df_real = (
        adjust_for_inflation(
            df_nominal.reset_index(),
            base_year,
            deflator
        )
        .set_index("Отрасль")
    )

    all_nominal = (
        salary_df[
            ["Отрасль"] + year_cols
        ]
        .set_index("Отрасль")
    )

    all_real = (
        adjust_for_inflation(
            all_nominal.reset_index(),
            base_year,
            deflator
        )
        .set_index("Отрасль")
    )

    nominal_long = create_long_format(
        df_nominal,
        "Номинальная"
    )

    real_long = create_long_format(
        df_real,
        "Реальная"
    )

    combined = pd.concat([
        nominal_long,
        real_long
    ])


    (
        tab1,
        tab2,
        tab3
    ) = st.tabs([
        "Динамика",
        "Итоги",
        "Сравнение"
    ])


    with tab1:
        st.subheader(
            "Сравнение номинальных "
            "и реальных зарплат"
        )

        chart_type = ()


        fig_salary = create_salary_chart(
            combined,
            chart_type,
            base_year
        )

        st.plotly_chart(
            fig_salary,
            use_container_width=True
        )
        
        st.markdown(
            "### Лидеры роста зарплат"
        )

        top_nominal = (
            calculate_top_growth(
                all_nominal
            )
        )

        top_real = (
            calculate_top_growth(
                all_real
            )
        )

        col_top1, col_top2 = st.columns(2)


        with col_top1:
            fig_top_nom = (
                create_top_growth_chart(
                    top_nominal,
                    "Номинальный рост"
                )
            )

            st.plotly_chart(
                fig_top_nom,
                use_container_width=True
            )

        with col_top2:
            fig_top_real = (
                create_top_growth_chart(
                    top_real,
                    "Реальный рост"
                )
            )

            st.plotly_chart(
                fig_top_real,
                use_container_width=True
            )


        st.subheader(
            "Темпы роста зарплат"
        )

        growth = calculate_growth(
            df_nominal
        )

        growth_long = (
            prepare_growth_long(growth)
        )

        fig_growth = create_growth_chart(
            growth_long
        )

        infl_compare = inflation_df[
            inflation_df["Год"].between(
                year_range[0],
                year_range[1]
            )
        ]

        fig_growth = add_inflation_line(
            fig_growth,
            infl_compare
        )

        st.plotly_chart(
            fig_growth,
            use_container_width=True
        )


    with tab2:
        st.subheader(
            "Итоговые показатели"
        )

        metrics = (
            calculate_summary_metrics(
                all_nominal,
                inflation_df
            )
        )

        salary_range = (
            f"{metrics['min_salary']:,.0f}"
            f" – "
            f"{metrics['max_salary']:,.0f} ₽"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                (
                    "Минимальная зарплата "
                    f"({metrics['current_year']})"
                ),
                f"{metrics['min_salary']:,.0f} ₽"
            )

            st.metric(
                (
                    "Средняя зарплата "
                    f"({metrics['current_year']})"
                ),
                f"{metrics['avg_salary']:,.0f} ₽"
            )

            st.metric(
                (
                    "Максимальная зарплата "
                    f"({metrics['current_year']})"
                ),
                f"{metrics['max_salary']:,.0f} ₽"
            )

        with col2:
            st.metric(
                (
                    "Медианная зарплата "
                    f"({metrics['current_year']})"
                ),
                f"{metrics['median_salary']:,.0f} ₽"
            )

            st.metric(
                (
                    "Размах "
                    f"({metrics['current_year']})"
                ),
                salary_range
            )


        with col3:
            st.metric(
                (
                    "Инфляция "
                    f"({metrics['current_year']})"
                ),
                f"{metrics['inflation']:.1f}%"
            )

            st.metric(
                "Рост за период",
                f"{metrics['total_growth']:.1f}%"
            )
        with tab3:

            st.subheader(
                "Сравнение отраслей"
             )

            growth_df = calculate_growth(
                all_nominal
            )

            growth_long = prepare_growth_long(
                growth_df
            )

            industries = sorted(
                growth_long["Отрасль"].unique()
            )

            col1, col2 = st.columns(2)

            with col1:

                industry1 = st.selectbox(
                    "Область 1",
                    industries,
                    index=0
                )

            with col2:

                industry2 = st.selectbox(
                    "Область 2",
                    industries,
                    index=min(
                        1,
                        len(industries) - 1
                    )
                )

            compare_df = growth_long[
                growth_long["Отрасль"].isin(
                    [
                        industry1,
                        industry2
                    ]
                )
            ]

            fig_compare = px.line(
                compare_df,
                x="Год",
                y="Рост, %",
                color="Отрасль",
                markers=True,
                title=(
                    "Сравнение темпов роста зарплат"
                )
            )

            fig_compare.update_layout(
                template="plotly_white",
                hovermode="x unified",
                xaxis_title="Год",
                yaxis_title="Темп роста (%)",
                legend_title="Отрасль",
                height=600
            )
            

            st.plotly_chart(
                fig_compare,
                use_container_width=True
            )


