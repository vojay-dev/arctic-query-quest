import logging
import time

import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from streamlit_lottie import st_lottie

from arctic import ArcticClient, ArcticQuiz
from common import AppState, load_model, read
from prompt import PromptGenerator, get_difficulty_by_name
from tts import SpeechClient

logger = logging.getLogger(__name__)


class ArcticQueryQuest:

    def __init__(self):
        self.prompt_generator: PromptGenerator = PromptGenerator()
        self.arctic_client: ArcticClient = ArcticClient()
        self.tts_client: SpeechClient = SpeechClient(
            st.secrets.gcp.project_id,
            st.secrets.gcp.private_key_id,
            st.secrets.gcp.private_key,
            st.secrets.gcp.client_email,
            st.secrets.gcp.client_id,
            st.secrets.gcp.client_x509_cert_url
        )

        self.placeholder = st.empty()

    def set_state(self, state: AppState):
        logger.info(f"switching state to {state}")
        self.placeholder.empty()
        st.session_state.app_state = state

    def start(self):
        with self.placeholder.container():
            st.html("<h1 class='arctic'>🏔️ Arctic Query Quest</h1>")

            tab_start, tab_about = st.tabs(["⚙️ Start", "🎓 About the project"])

            with tab_start:
                col1, col2 = st.columns(2)

                with col1:
                    db_model = st.radio(
                        ":book: Choose a database model to explore:",
                        ["Shop", "Game", "Books"],
                        captions=["Database model for a shop", "Database model for an online game",
                                  "Database model about books"]
                    )

                    st.session_state.db_model = db_model

                    model_backgrounds = {
                        "Shop": "https://files.janz.sh/arctic/model-shop.jpg",
                        "Game": "https://files.janz.sh/arctic/model-game.jpg",
                        "Books": "https://files.janz.sh/arctic/model-books.jpg"
                    }

                    if background := model_backgrounds.get(db_model, ""):
                        st.html(f"<style>.stRadio {{ background: url({background}); }}</style>")

                    difficulty = st.select_slider(
                        label=":star: Select difficulty level:",
                        options=["Easy", "Medium", "Hard"]
                    )
                    st.session_state.difficulty = difficulty
                with col2:
                    st_lottie("https://lottie.host/fe98088d-45bc-4b23-b45c-5b9d97dfab74/h8Y01cq58s.json", width=350)

            with tab_about:
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(read("intro.md"))

                with col2:
                    with st.expander("Open to see a system overview..."):
                        st.image("images/overview.png", use_column_width=True)

            model = load_model()
            with st.expander(f"Open to see selected database model (`{st.session_state.db_model}`)..."):
                st.code(model, language="sql")

            with st.container(border=True):
                st.button(":video_game: Start the Quest!", on_click=self.set_state, args=(AppState.QUIZ,))

    def answer(self, generated_quiz: ArcticQuiz, user_answer: int):
        st.session_state.generated_quiz = generated_quiz
        st.session_state.user_answer = user_answer
        self.set_state(AppState.EVALUATE)

    def quiz(self):
        with self.placeholder.container():
            st.html("<h1 class='arctic'>🏔️ Arctic Query Quest</h1>")
            st.divider()

            st.markdown("## :books: Model")
            model = load_model()
            with st.expander("Open to see database model..."):
                st.code(model, language="sql")

            st.divider()

            generated_quiz: ArcticQuiz | None = None

            progress_bar = st.progress(0, text="Exploring the Arctic for you 🏔️...")

            loading_placeholder = st.empty()
            with loading_placeholder.container():
                st_lottie("https://lottie.host/44ed2dbd-c55b-49c5-9031-873c231768b2/TmmqUQG5Bt.json", width=400)

            time.sleep(2)

            try:
                progress_bar.progress(20, text="Generating a quiz for you 🤖...")
                prompt = self.prompt_generator.generate_prompt(
                    model=model,
                    difficulty=get_difficulty_by_name(st.session_state.difficulty),
                )

                generated_quiz = self.arctic_client.invoke(prompt)

                progress_bar.progress(60, text="Generating speech 💬...")
                speech_question = self.tts_client.synthesize(generated_quiz.question)

                progress_bar.progress(100, text="Get ready for the Arctic Query Quiz 🏔️...")
                time.sleep(1)

                loading_placeholder.empty()

            except Exception as e:
                logger.error(f"error in quiz generation: {e}")
                st.markdown(f"An error occurred: {e}")
                st.divider()
                st.markdown("Don't Worry, Be Happy - reload the page and try again!")
                st.button(":repeat: Reload", on_click=lambda: streamlit_js_eval(js_expressions="parent.window.location.reload()"))

            if generated_quiz:
                st.markdown("## :speech_balloon: Question")
                with st.chat_message("assistant"):
                    st.markdown(generated_quiz.question)

                st.audio(speech_question, format="audio/mpeg", autoplay=True)

                st.markdown("## :bulb: Answers")
                with st.chat_message("assistant"):
                    st.markdown(f"1) {generated_quiz.answer_1}")
                    st.markdown(f"2) {generated_quiz.answer_2}")
                    st.markdown(f"3) {generated_quiz.answer_3}")

                st.markdown("Choose wisely:")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.button(":one:", on_click=self.answer, args=(generated_quiz, 1,), use_container_width=True)
                with col2:
                    st.button(":two:", on_click=self.answer, args=(generated_quiz, 2,), use_container_width=True)
                with col3:
                    st.button(":three:", on_click=self.answer, args=(generated_quiz, 3,), use_container_width=True)

    def evaluate(self):
        with self.placeholder.container():
            generated_quiz: ArcticQuiz = st.session_state.generated_quiz
            user_answer = st.session_state.user_answer
            correct_answer = generated_quiz.correct_answer

            st.html("<h1 class='arctic'>🏔️ Arctic Query Quest</h1>")
            st.divider()

            if user_answer == correct_answer:
                st.success(f"Answer {user_answer} is correct 🎉")
                st.balloons()

                difficulty = st.session_state.difficulty
                points = 1 if difficulty == "Easy" else 2 if difficulty == "Medium" else 3
                st.session_state.score += points

                st.toast(
                    f"You got {points} point{'s' if points > 1 else ''}. Total score: {st.session_state.score}",
                    icon="⭐️"
                )
            else:
                st.warning(f"Answer {user_answer} is wrong 😢")

            correct_answer_text = getattr(generated_quiz, f"answer_{correct_answer}")
            st.markdown(f"**The correct answer is**: {correct_answer_text}")
            st.markdown(f"**Because**: {generated_quiz.explanation}")
            st.divider()
            st.button(":arrow_left: Back to start!", on_click=self.set_state, args=(AppState.START,))
