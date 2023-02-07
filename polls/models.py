from datetime import timedelta

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    publication_date = models.DateTimeField('date published')

    def is_future_publication(self):
        """
        Check if the question's publication date is in the future.

        :return: True if the question's publication date is greater than
            the current server time and False otherwise.
        """
        return self.publication_date > timezone.now()

    def is_recent_publication(self):
        """
        Check if the question was published within the last day.

        NOTE: A question with a future publication date is not considered
            to be a recent question.
        :return: True if the question's publication date is within the last
        day and False otherwise.
        """
        return (
                (self.publication_date >= timezone.now() - timedelta(days=1))
                and not self.is_future_publication()
        )

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    vote_tally = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
