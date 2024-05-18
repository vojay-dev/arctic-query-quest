import logging
import sys

import streamlit as st

from common import AppState, init_page
from app import ArcticQueryQuest

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.info("initializing app...")
    init_page()
    arctic_query_quest: ArcticQueryQuest = ArcticQueryQuest()

    state = st.session_state.app_state

    logging.info(f"rendering state: {state}")
    if state == AppState.START:
        arctic_query_quest.start()
    elif state == AppState.QUIZ:
        arctic_query_quest.quiz()
    elif state == AppState.EVALUATE:
        arctic_query_quest.evaluate()
