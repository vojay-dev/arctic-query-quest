from enum import Enum
from pathlib import Path

import streamlit as st


class AppState(Enum):
    START = "start"
    QUIZ = "quiz"
    EVALUATE = "evaluate"


def read(path: str) -> str:
    return Path(path).read_text()


def apply_style():
    st.html(f"<style>{Path('style.css').read_text()}</style>")


def configure():
    st.set_page_config(layout="wide")

    if "app_state" not in st.session_state:
        st.session_state.app_state = AppState.START


def init_state():
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "app_state" not in st.session_state:
        st.session_state.app_state = AppState.START
    if "db_model" not in st.session_state:
        st.session_state.db_model = None
    if "generated_quiz" not in st.session_state:
        st.session_state.generated_quiz = None
    if "user_answer" not in st.session_state:
        st.session_state.user_answer = None
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = None


def menu():
    with st.sidebar:
        st.image("images/logo.png", use_column_width=True)

        st.markdown(f"""
        Your score: `{st.session_state.score}`\n
        - Easy: `1 point`
        - Medium: `2 points`
        - Hard: `3 points`
        """)
        st.divider()
        st.markdown("### 🚀 Social")
        st.page_link("https://www.linkedin.com/in/vjanz/", label="LinkedIn")
        st.page_link("https://vojay.medium.com/", label="Medium")
        st.page_link("https://twitter.com/vojaydev", label="X")

        st.divider()
        st.markdown("### 🧪 Debugging")
        st.markdown(f"Current app state: `{st.session_state.app_state.value}`")


def init_page():
    configure()
    init_state()
    apply_style()
    menu()


def load_model() -> str:
    model = st.session_state.db_model
    if model and model == "Shop":
        return read("models/shop.sql")
    elif model and model == "Game":
        return read("models/game.sql")
    elif model and model == "Books":
        return read("models/books.sql")
    else:
        return read("models/shop.sql")
