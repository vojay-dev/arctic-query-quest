import streamlit as st

from app import ArcticQueryQuest
from common import AppState, init_page, console_log

if __name__ == '__main__':
    init_page()
    console_log(f"init page done")
    arctic_query_quest: ArcticQueryQuest = ArcticQueryQuest()

    state = st.session_state.app_state

    console_log(f"rendering state: {state}")
    if state == AppState.START:
        arctic_query_quest.start()
    elif state == AppState.QUIZ:
        arctic_query_quest.quiz()
    elif state == AppState.EVALUATE:
        arctic_query_quest.evaluate()
