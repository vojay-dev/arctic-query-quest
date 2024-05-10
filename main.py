import json
from pathlib import Path

import streamlit as st
from langchain_community.llms.replicate import Replicate
from langchain_core.prompts import PromptTemplate

from common import AppState, init_page, load_model

init_page()

placeholder = st.empty()


def set_state(state):
    placeholder.empty()
    st.session_state.app_state = state


def start():
    with placeholder.container():
        st.html("<h1 class='arctic'>🏔️ Arctic Query Quest</h1>")
        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
                Welcome to the Arctic Query Quest! This is a fun and interactive way to learn SQL powered by the Snowflake Arctic
                model family.
            """)

        with col2:
            db_model = st.radio(
                "Choose your destiny",
                ["Shop", "Game", "Books"],
                captions=["Database model for a shop", "Database model for an online game", "Database model about books"]
            )

            st.session_state.db_model = db_model
            if st.session_state.db_model == "Shop":
                st.html("<style>.stRadio { background: url(https://files.janz.sh/arctic/model-shop.jpg); }</style>")
            elif st.session_state.db_model == "Game":
                st.html("<style>.stRadio { background: url(https://files.janz.sh/arctic/model-game.jpg); }</style>")
            elif st.session_state.db_model == "Books":
                st.html("<style>.stRadio { background: url(https://files.janz.sh/arctic/model-books.jpg); }</style>")

        model = load_model()
        with st.expander(f"Open to see selected database model (`{st.session_state.db_model}`)..."):
            st.code(model, language="sql")
        st.button("Start the Quest!", on_click=set_state, args=(AppState.QUIZ,))


def answer(generated_quiz, user_answer):
    st.session_state.generated_quiz = generated_quiz
    st.session_state.user_answer = user_answer
    set_state(AppState.EVALUATE)


def quiz():
    with placeholder.container():
        st.html("<h1 class='arctic'>🏔️ Arctic Query Quest</h1>")
        st.divider()

        st.markdown("## Model")
        model = load_model()
        with st.expander("Open to see database model..."):
            st.code(model, language="sql")

        st.divider()

        generated_quiz = None
        with st.spinner("Exploring the Arctic for you..."):
            try:
                prompt_template = PromptTemplate.from_file(template_file=Path("prompt.jinja"), template_format="jinja2")

                llm = Replicate(
                    model="snowflake/snowflake-arctic-instruct",
                    model_kwargs={
                        "top_k": 50,
                        "top_p": 0.8,
                        "temperature": 0.5,
                        "max_new_tokens": 1024,
                        "min_new_tokens": 0,
                        "stop_sequences": "<|im_end|>",
                        "prompt_template": "<|im_start|>system\nYou're a helpful assistant<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n\n<|im_start|>assistant\n",
                        "presence_penalty": 1.15,
                        "frequency_penalty": 0.2
                    }
                )

                output = llm.invoke(prompt_template.format(model=model))
                generated_quiz = json.loads(output)
            except Exception as e:
                st.markdown(f"An error occurred: {e}")
                raise e

        if generated_quiz:
            st.markdown("## Question")
            with st.chat_message("assistant"):
                st.markdown(generated_quiz["question"])
            st.markdown("## Answers")
            with st.chat_message("assistant"):
                st.markdown(f"1) {generated_quiz['answer_1']}")
                st.markdown(f"2) {generated_quiz['answer_2']}")
                st.markdown(f"3) {generated_quiz['answer_3']}")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("1", on_click=answer, args=(generated_quiz, 1,), use_container_width=True)
            with col2:
                st.button("2", on_click=answer, args=(generated_quiz, 2,), use_container_width=True)
            with col3:
                st.button("3", on_click=answer, args=(generated_quiz, 3,), use_container_width=True)


def evaluate():
    with placeholder.container():
        generated_quiz = st.session_state.generated_quiz
        user_answer = st.session_state.user_answer
        correct_answer = generated_quiz["correct_answer"]

        st.html("<h1 class='arctic'>🏔️ Arctic Query Quest</h1>")
        st.divider()

        if user_answer == correct_answer:
            st.success(f"Answer {user_answer} is correct 🎉")
        else:
            st.warning(f"Answer {user_answer} is wrong 😢")

        st.markdown(f"The correct answer is: {generated_quiz['answer_' + str(correct_answer)]}")
        st.markdown(f"Because: {generated_quiz['explanation']}")
        st.divider()
        st.button("Back to start!", on_click=set_state, args=(AppState.START,))


if st.session_state.app_state == AppState.START:
    start()
elif st.session_state.app_state == AppState.QUIZ:
    quiz()
elif st.session_state.app_state == AppState.EVALUATE:
    evaluate()
