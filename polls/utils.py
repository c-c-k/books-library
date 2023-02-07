# -*- coding: utf-8 -*-

"""Summary

Description
"""

# --------------------
# IMPORTS
# --------------------
# Standard library modules:
from datetime import timedelta
from random import randint, sample

# Third party modules:
from django.db import models
from django.utils import timezone

# Local scripts and modules:
from .models import Question, Choice

# --------------------
# CONSTANTS
# --------------------


# --------------------
# CLASSES
# --------------------


# --------------------
# FUNCTIONS
# --------------------
def create_questions() -> list[Question]:
    return [
        Question(
            question_text="Ipsum lorem",
            publication_date=timezone.now() - timedelta(seconds=sec_diff)
        )
        for sec_diff
        in sample(range(int(timedelta(days=6).total_seconds())), k=6)
    ]


def create_choices(questions: list[Question]) -> list[Choice]:
    return [
        Choice(
            question=question,
            choice_text=f"Ipsum lorem --{num}--",
            # vote_tally=randint(0, 20),
            vote_tally=0,
        )
        for num
        in range(1, 5)
        for question
        in questions
    ]


def repopulate_polls():
    for model in (Question, Choice):
        model.objects.all().delete()
    questions = create_questions()
    choices = create_choices(questions)
    model_objects: list[models.Model] = [*questions, *choices]
    for model_object in model_objects:
        model_object.save()
