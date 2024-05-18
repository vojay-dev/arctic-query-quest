import os
import unittest

from arctic_query_quest.arctic import ArcticClient, ArcticQuiz


class TestGemini(unittest.TestCase):

    def test_extract_json(self):
        arctic_reply = """
            Here is the generated quiz:
            {
                "question": "What stands SQL for?",
                "answer_1": "Structured Query Language",
                "answer_2": "Standard Query Language",
                "answer_3": "Simple Query Language",
                "correct_answer": 1,
                "explanation": "SQL stands for Structured Query Language"
            }
            Some more text
        """
        json = ArcticClient._extract_json(arctic_reply)

        self.assertEqual(json[0], "{")
        self.assertEqual(json[-1], "}")

    def test_parse_output(self):
        arctic_reply = """
            Here is the generated quiz:
            {
                "question": "What stands SQL for?",
                "answer_1": "Structured Query Language",
                "answer_2": "Standard Query Language",
                "answer_3": "Simple Query Language",
                "correct_answer": 1,
                "explanation": "SQL stands for Structured Query Language"
            }
            Some more text
        """

        os.environ["REPLICATE_API_TOKEN"] = "dummy"

        arctic_client: ArcticClient = ArcticClient()
        arctic_quiz: ArcticQuiz = arctic_client._parse_output(arctic_reply)

        self.assertEqual(arctic_quiz.question, "What stands SQL for?")
        self.assertEqual(arctic_quiz.answer_1, "Structured Query Language")
        self.assertEqual(arctic_quiz.answer_2, "Standard Query Language")
        self.assertEqual(arctic_quiz.answer_3, "Simple Query Language")
        self.assertEqual(arctic_quiz.correct_answer, 1)
        self.assertEqual(arctic_quiz.explanation, "SQL stands for Structured Query Language")


if __name__ == '__main__':
    unittest.main()
