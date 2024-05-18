import streamlit as st

from common import AppState, init_page
from app import ArcticQueryQuest

if __name__ == '__main__':
    init_page()
    arctic_query_quest: ArcticQueryQuest = ArcticQueryQuest()

    state = st.session_state.app_state
    if state == AppState.START:
        arctic_query_quest.start()
    elif state == AppState.QUIZ:
        arctic_query_quest.quiz()
    elif state == AppState.EVALUATE:
        arctic_query_quest.evaluate()
