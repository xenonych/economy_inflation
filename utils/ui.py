import streamlit as st


def setup_page():
    """
    Настройка параметров страницы Streamlit.
    """

    st.set_page_config(
        page_title="Анализ зарплат в России",
        page_icon="Ы",
        layout="wide",
        initial_sidebar_state="collapsed"
    )


def init_theme():

    if "theme" not in st.session_state:
        st.session_state.theme = "dark"


def toggle_theme():

    if "theme" not in st.session_state:
        st.session_state.theme = "dark"



def load_css():

    if st.session_state.theme == "dark":

        theme_css = """
        <style>

        :root {
            --bg: #0a0a0a;
            --card: rgba(255,255,255,0.04);
            --shadow rgba(0,0,0,0.20)
            --border: rgba(255,255,255,0.08);
            --text: #f3f4f6;
            --muted: #9ca3af;
            --accent: #8b5cf6;
        }

        .stApp {
            background:
                radial-gradient(
                    circle at top left,
                    rgba(139,92,246,0.15),
                    transparent 30%
                ),
                radial-gradient(
                    circle at bottom right,
                    rgba(59,130,246,0.12),
                    transparent 25%
                ),
                var(--bg);

            color: var(--text);
        }

        </style>
        """


    base_css = """
    <style>

    section.main > div {
        padding-top: 2rem;
    }

    .hero {
        position: relative;

        padding: 3rem;
        margin-bottom: 2rem;

        background: var(--card);

        border: 1px solid var(--border);

        backdrop-filter: blur(20px);

        overflow: hidden;

        border-radius: 23px;

        box-shadow:  14px 14px 28px rgba(0, 0, 0, .075),
               inset 2px 2px 2px rgba(255, 255, 255, .075),
               inset 2px 2px 4px rgba(0, 0, 0, .15);
        padding: 5%;  
        text-shadow: 2px 2px 3px rgb(10, 10, 10); 
    }

    .hero::before {

        content: "";

        position: absolute;

        width: 400px;
        height: 400px;

        right: -120px;
        top: -120px;

        background: var(--accent);

        opacity: 0.15;

        filter: blur(120px);

        border-radius: 50%;
    }

    .hero h1 {

        font-size: 3.2rem;
        font-weight: 800;

        margin-bottom: 0.5rem;

        letter-spacing: -2px;
    }



    div.stButton > button {

        border-radius: 16px;

        border: 1px solid var(--border);

        background: var(--card);

        color: var(--text);

        backdrop-filter: blur(12px);

        transition: 0.2s ease;

        height: 48px;
    }

    div.stButton > button:hover {

        border-color: var(--accent);

        transform: translateY(-2px);
    }

    [data-testid="stMetric"] {

        background: var(--card);

        border: 1px solid var(--border);

        padding: 1rem;

        border-radius: 20px;
    }

    </style>
    """

    st.markdown(
        theme_css + base_css,
        unsafe_allow_html=True
    )


def show_header():
    """
    Отображение шапки приложения.
    """

    top1, top2 = st.columns([8, 1])



    st.markdown(
        """
<div class="hero">

<h1>
Анализ зарплат в России
</h1>

<p>
Интерактивная аналитика зарплат
с учётом инфляции
</p>

</div>
        """,
        unsafe_allow_html=True
    )