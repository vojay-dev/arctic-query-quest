from enum import Enum
from pathlib import Path

import streamlit as st


class AppState(Enum):
    START = "start"
    QUIZ = "quiz"
    EVALUATE = "evaluate"


def apply_style():
    st.html(f"<style>{Path('style.css').read_text()}</style>")


def configure():
    st.set_page_config(layout="wide")

    if "app_state" not in st.session_state:
        st.session_state.app_state = AppState.START


def init_state():
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


def load_model():
    model = st.session_state.db_model
    if model and model == "Shop":
        return Path("models/shop.sql").read_text()
    elif model and model == "Game":
        return Path("models/game.sql").read_text()
    elif model and model == "Books":
        return Path("models/books.sql").read_text()
    else:
        return Path("models/shop.sql").read_text()
