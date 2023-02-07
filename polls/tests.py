# -*- coding: utf-8 -*-

"""This is the main tests file for the polls' app.

"""

# ====================IMPORTS=======================================
from datetime import timedelta
from typing import Callable

from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Question


# ====================TESTING UTILITIES===============================
def add_question_with_timedelta_offset(
        text: str = "Ipsum lorem.", weeks: int = 0, days: int = 0,
        hours: int = 0, minutes: int = 0, seconds: int = 0,
) -> Question:
    """
    Add a new question to the test db with a timedelta offset from now.

    :param text: The text for the new question's question_text field,
                    defaults to "Ipsum lorem".
    :param weeks: The weeks argument to be passed to the timedelta object.
    :param days: The days argument to be passed to the timedelta object.
    :param hours: The hours argument to be passed to the timedelta object.
    :param minutes: The minutes argument to be passed to the timedelta object.
    :param seconds: The seconds argument to be passed to the timedelta object.
    :return: A new instance of the Question model with its publication_date
                attribute offset from now by the timedelta indicated by the
                weeks/days/hours/minutes/seconds arguments.
    """
    question = Question(
        question_text=text,
        publication_date=timezone.now() + timedelta(
            weeks=weeks, days=days,
            hours=hours, minutes=minutes, seconds=seconds
        )
    )
    question.save()
    return question


def date_error_msg(
        question: Question, method: Callable = None, extra_msg: str = "",
) -> str:
    return (
        f"\ntest for: {question.__class__}."
        f"{method.__name__ if method else '<-no method->'}\n"
        f"problem: {extra_msg}\n"
        f"current datetime:     {str(timezone.now())}\n"
        f"publication datetime: {str(question.publication_date)}"
    )


# ====================MODELS TESTS==================================
class QuestionModelTests(TestCase):

    # -- tests for method: is_future_publication() --
    def test_is_future_pub_with_future_date(self):
        """
        Test if the is_future_publication() method returns True for
        questions with a publication date in the future.
        """
        question = add_question_with_timedelta_offset(minutes=+1)
        self.assertTrue(
            question.is_future_publication(),
            date_error_msg(
                question=question,
                method=question.is_future_publication,
                extra_msg="future publication date reported as non-future."
            )
        )

    def test_is_future_publication_with_non_future_publication_date(self):
        """
        Test if the is_future_publication() method returns False for
        questions with a publication date that is not in the future.
        """
        question = add_question_with_timedelta_offset(minutes=-1)
        self.assertFalse(
            question.is_future_publication(),
            date_error_msg(
                question=question,
                method=question.is_future_publication,
                extra_msg="non-future publication date reported as future."
            )
        )

    # -- tests for method: is_recent_publication() --
    def test_is_recent_publication_with_future_publication_date(self):
        """
        Test if the is_recent_publication() method returns False for
        questions with a publication date in the future.
        """
        question = add_question_with_timedelta_offset(minutes=+1)
        self.assertFalse(
            question.is_recent_publication(),
            date_error_msg(
                question=question,
                method=question.is_recent_publication(),
                extra_msg="future publication date reported as recent."
            )
        )

    def test_is_recent_publication_with_recent_publication_date(self):
        """
        Test if the is_recent_publication() method returns True for
        questions with a publication date in the last day.
        """
        test_offsets = ({"minutes": -1}, {"days": -1, "minutes": +1})
        for test_offset in test_offsets:
            question = add_question_with_timedelta_offset(**test_offset)
            self.assertTrue(
                question.is_recent_publication(),
                date_error_msg(
                    question=question,
                    method=question.is_recent_publication,
                    extra_msg="recent publication date reported as non recent."
                )
            )

    def test_is_recent_publication_with_past_publication_date(self):
        """
        Test if the is_recent_publication() method returns False for
        questions with a publication date older than a day.
        """
        question = add_question_with_timedelta_offset(days=-1, minutes=-1)
        self.assertFalse(
            question.is_recent_publication(),
            date_error_msg(
                question=question,
                method=question.is_recent_publication(),
                extra_msg="past publication date reported as recent."
            )
        )


# ====================VIEWS TESTS===================================
class IndexViewTests(TestCase):
    def test_no_questions(self):
        """
        Test that the Question queryset is empty and that
        the polls index page reports that there are no questions
        in the database.
        """
        response = self.client.get(reverse("polls:index"))
        # check that the index page is at all reachable.
        self.assertEqual(
            response.status_code, 200,
            msg="No status code 200 from index url with empty question db."
        )
        # check that the returned queryset contains no items.
        self.assertQuerysetEqual(
            response.context["questions_list"], [],
            msg="Question queryset not empty with no questions in the db."
        )
        # check that the index page displays the no questions message.
        self.assertContains(
            response, "There are no questions.",
            msg_prefix="No questions message doesn't appear on the index page"
                       "with no questions in the db.\n"
        )

    def test_only_future_questions(self):
        """
        Test that the polls index page reports that there are no questions
        when there are only questions with a future publication date in the
        database.
        """
        # populate db with future questions
        for days_offset in range(1, 4):
            add_question_with_timedelta_offset(days=days_offset)
        # get simulated server response
        response = self.client.get(reverse("polls:index"))
        # check that the index page is at all reachable.
        self.assertEqual(
            response.status_code, 200,
            msg="No status code 200 from index url with only future "
                "questions in the db."
        )
        # check that the returned queryset contains no items.
        self.assertQuerysetEqual(
            response.context["questions_list"], [],
            msg="Question queryset not empty with only future questions in "
                "the db."
        )
        # check that the index page displays the no questions message.
        self.assertContains(
            response, "There are no questions.",
            msg_prefix="No questions message doesn't appear on the index page"
                       "with only future questions in the db.\n"
        )

    def test_only_past_questions(self):
        """
        Test that the polls index page properly shows only the latest 3
        questions when there are only questions with a past publication date
        in the database.
        """
        # populate db with past questions
        past_questions = []
        for days_offset in range(-1, -6, -1):
            question = add_question_with_timedelta_offset(
                text="test_past_question",
                days=days_offset
            )
            past_questions.append(question)
        # get simulated server response
        response = self.client.get(reverse("polls:index"))
        # check that the index page is at all reachable.
        self.assertEqual(
            response.status_code, 200,
            msg="No status code 200 from index url with only past "
                "questions in the db."
        )
        # check that the returned queryset is not empty.
        self.assertGreater(
            response.context["questions_list"].count(), 0,
            msg="Question queryset empty with past questions in "
                "the db."
        )
        # check that the returned queryset contains only the latest 3
        # questions.
        self.assertQuerysetEqual(
            response.context["questions_list"], past_questions[:3],
            msg="Question queryset contains wrong questions with only past"
                "questions in the db."
        )
        # check that the index page displays the test questions.
        self.assertContains(
            response, "test_past_question",
            msg_prefix="Questions don't appear on the index page"
                       "with only past questions in the db.\n"
        )

    def test_future_and_past_questions(self):
        """
        Test that the polls index page properly shows only the latest 3
        questions when there are questions with both past and future
        publication dates in the database.
        """
        # populate db with past questions
        past_questions = []
        for days_offset in range(-1, -6, -1):
            question = add_question_with_timedelta_offset(
                text="test_past_question",
                days=days_offset
            )
            past_questions.append(question)
        # populate db with future questions
        for days_offset in range(1, 4):
            add_question_with_timedelta_offset(days=days_offset)
        # get simulated server response
        response = self.client.get(reverse("polls:index"))
        # check that the index page is at all reachable.
        self.assertEqual(
            response.status_code, 200,
            msg="No status code 200 from index url with both past and future "
                "questions in the db."
        )
        # check that the returned queryset is not empty.
        self.assertGreater(
            response.context["questions_list"].count(), 0,
            msg="Question queryset empty with both past and future questions "
                "in the db."
        )
        # check that the returned queryset contains only the latest 3
        # questions.
        self.assertQuerysetEqual(
            response.context["questions_list"], past_questions[:3],
            msg="Question queryset contains wrong questions with"
                "both past and future questions in the db."
        )
        # check that the index page displays the test questions.
        self.assertContains(
            response, "test_past_question",
            msg_prefix="Questions don't appear on the index page"
                       "with both past and future questions in the db.\n"
        )
