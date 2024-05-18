import os
import unittest

from streamlit.testing.v1 import AppTest


class TestApp(unittest.TestCase):

    def test_run_app(self):
        os.environ["REPLICATE_API_TOKEN"] = "dummy"
        at = AppTest.from_file("arctic_query_quest/main.py")
        at.run()
        assert not at.exception

    def test_state_initialization(self):
        os.environ["REPLICATE_API_TOKEN"] = "dummy"
        at = AppTest.from_file("arctic_query_quest/main.py")
        at.run()

        states = [
            "score",
            "app_state",
            "db_model",
            "generated_quiz",
            "user_answer",
            "difficulty"
        ]

        for key in states:
            assert key in at.session_state
