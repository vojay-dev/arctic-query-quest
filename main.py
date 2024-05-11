import json

import streamlit as st
from langchain_community.llms.replicate import Replicate

from common import AppState, init_page, load_model, read
from prompt import PromptGenerator, get_difficulty_by_name

prompt_generator: PromptGenerator = PromptGenerator()

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
            st.markdown(read("intro.md"))
            with st.expander(f"Open to see a system overview..."):
                st.image("images/overview.png", use_column_width=True)

        with col2:
            db_model = st.radio(
                ":book: Choose a database model to explore:",
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

            difficulty = st.select_slider(
                label=":star: Select difficulty level:",
                options=["Easy", "Medium", "Hard"]
            )
            st.session_state.difficulty = difficulty

        st.divider()
        model = load_model()
        with st.expander(f"Open to see selected database model (`{st.session_state.db_model}`)..."):
            st.code(model, language="sql")
        st.button(":video_game: Start the Quest!", on_click=set_state, args=(AppState.QUIZ,))


def answer(generated_quiz, user_answer):
    st.session_state.generated_quiz = generated_quiz
    st.session_state.user_answer = user_answer
    set_state(AppState.EVALUATE)


def quiz():
    with placeholder.container():
        st.html("<h1 class='arctic'>🏔️ Arctic Query Quest</h1>")
        st.divider()

        st.markdown("## :books: Model")
        model = load_model()
        with st.expander("Open to see database model..."):
            st.code(model, language="sql")

        st.divider()

        generated_quiz = None
        with st.spinner("Exploring the Arctic for you..."):
            try:
                llm = Replicate(
                    model="snowflake/snowflake-arctic-instruct",
                    model_kwargs={
                        "top_k": 50,
                        "top_p": 0.8,
                        "temperature": 0.5,
                        "max_new_tokens": 3072,
                        "stop_sequences": "<|im_end|>",
                        "prompt_template": "<|im_start|>system\nYou're a helpful assistant<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n\n<|im_start|>assistant\n",
                        "presence_penalty": 1.15,
                        "frequency_penalty": 0.2
                    }
                )

                chunks = []

                prompt = prompt_generator.generate_prompt(
                    model=model,
                    difficulty=get_difficulty_by_name(st.session_state.difficulty),
                )

                for chunk in llm.stream(prompt):
                    chunks.append(chunk)

                output = "".join(chunks)
                generated_quiz = json.loads(output)
            except Exception as e:
                st.markdown(f"An error occurred: {e}")
                st.divider()
                st.markdown("Don't Worry, Be Happy - reload the page and try again!")

        if generated_quiz:
            st.markdown("## :speech_balloon: Question")
            with st.chat_message("assistant"):
                st.markdown(generated_quiz["question"])
            st.markdown("## :bulb: Answers")
            with st.chat_message("assistant"):
                st.markdown(f"1) {generated_quiz['answer_1']}")
                st.markdown(f"2) {generated_quiz['answer_2']}")
                st.markdown(f"3) {generated_quiz['answer_3']}")

            st.markdown("Choose wisely:")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button(":one:", on_click=answer, args=(generated_quiz, 1,), use_container_width=True)
            with col2:
                st.button(":two:", on_click=answer, args=(generated_quiz, 2,), use_container_width=True)
            with col3:
                st.button(":three:", on_click=answer, args=(generated_quiz, 3,), use_container_width=True)


def evaluate():
    with placeholder.container():
        generated_quiz = st.session_state.generated_quiz
        user_answer = st.session_state.user_answer
        correct_answer = generated_quiz["correct_answer"]

        st.html("<h1 class='arctic'>🏔️ Arctic Query Quest</h1>")
        st.divider()

        if user_answer == correct_answer:
            st.success(f"Answer {user_answer} is correct 🎉")
            st.balloons()

            difficulty = st.session_state.difficulty
            points = 1 if difficulty == "Easy" else 2 if difficulty == "Medium" else 3
            st.session_state.score += points
        else:
            st.warning(f"Answer {user_answer} is wrong 😢")

        st.markdown(f"**The correct answer is**: {generated_quiz['answer_' + str(correct_answer)]}")
        st.markdown(f"**Because**: {generated_quiz['explanation']}")
        st.divider()
        st.button(":arrow_left: Back to start!", on_click=set_state, args=(AppState.START,))


if st.session_state.app_state == AppState.START:
    start()
elif st.session_state.app_state == AppState.QUIZ:
    quiz()
elif st.session_state.app_state == AppState.EVALUATE:
    evaluate()
