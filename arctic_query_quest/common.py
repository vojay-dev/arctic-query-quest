import base64
import logging
from enum import Enum
from pathlib import Path

import streamlit as st
from streamlit_js_eval import streamlit_js_eval


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


def init_state():
    state_defaults = {
        "score": 0,
        "app_state": AppState.START,
        "db_model": None,
        "generated_quiz": None,
        "user_answer": None,
        "difficulty": None,
    }

    for key, default in state_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default


def menu():
    with st.sidebar:
        st.image("images/logo.png", use_column_width=True)

        st.markdown(f"""
        🏅 Your score: `{st.session_state.score}`\n
        - **Easy**: `1 point`
        - **Medium**: `2 points`
        - **Hard**: `3 points`
        """)
        st.divider()
        st.html("<h3 class='arctic'>🚀 Social</h3>")
        render_link_with_svg_icon(
            "https://www.linkedin.com/in/vjanz/",
            "LinkedIn",
            '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="white" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037c-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85c3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.06 2.06 0 0 1-2.063-2.065a2.064 2.064 0 1 1 2.063 2.065m1.782 13.019H3.555V9h3.564zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0z"/></svg>',
        )

        render_link_with_svg_icon(
            "https://vojay.medium.com/",
            "Medium",
            '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="white" d="M13.54 12a6.8 6.8 0 0 1-6.77 6.82A6.8 6.8 0 0 1 0 12a6.8 6.8 0 0 1 6.77-6.82A6.8 6.8 0 0 1 13.54 12m7.42 0c0 3.54-1.51 6.42-3.38 6.42s-3.39-2.88-3.39-6.42s1.52-6.42 3.39-6.42s3.38 2.88 3.38 6.42M24 12c0 3.17-.53 5.75-1.19 5.75s-1.19-2.58-1.19-5.75s.53-5.75 1.19-5.75S24 8.83 24 12"/></svg>',
        )

        render_link_with_svg_icon(
            "https://twitter.com/vojaydev",
            "X",
            '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="white" d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584l-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"/></svg>',
        )

        st.divider()
        st.html("<h3 class='arctic'>🧪 Debugging</h3>")
        st.markdown(f"Current app state: `{st.session_state.app_state.value}`")


def init_page():
    configure()
    init_state()
    apply_style()
    menu()


def load_model() -> str:
    model_files = {
        "Shop": "models/shop.sql",
        "Game": "models/game.sql",
        "Books": "models/books.sql",
    }

    model = st.session_state.db_model
    return read(model_files.get(model, "models/shop.sql"))


def render_link_with_svg_icon(link, text, svg):
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    svg = f'<img src="data:image/svg+xml;base64,{b64}"/>'
    link = f'<a style="margin-right: 5px; margin-left: 5px;" href="{link}" target="_blank">{text}</a>'
    html = f"{svg}{link}"
    st.write(html, unsafe_allow_html=True)


def console_log(text):
    try:
        text = text.replace("`", "\\`")
        streamlit_js_eval(js_expressions=f"console.log(`{text}`)")
    except Exception as e:
        logging.error(f"could not evaluate console.log JS: {e}")
