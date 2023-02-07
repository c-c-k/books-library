from django.shortcuts import (
    render, redirect, get_object_or_404)
from django.http import HttpRequest, HttpResponseRedirect
from django.views.generic import DetailView, ListView
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question
from .utils import repopulate_polls


class IndexView(ListView):
    template_name = "polls/index.html"
    context_object_name = 'questions_list'

    def get_queryset(self):
        return Question.objects.filter(
            publication_date__lte=timezone.now()).order_by(
            '-publication_date')[:3]


class QuestionDetails(DetailView):
    context_object_name = "question"
    model = Question
    template_name = "polls/detail.html"


class QuestionResults(DetailView):
    context_object_name = "question"
    model = Question
    template_name = "polls/results.html"


def vote(request, pk):
    question = get_object_or_404(Question, pk=pk)
    try:
        choice = Choice.objects.get(pk=request.POST["choice_id"])
    except (KeyError, Choice.DoesNotExist):
        context = {
            "question": question,
            "error_message": "You have not selected a valid choice."
        }
        return render(request, "polls/detail.html", context)
    else:
        choice.vote_tally += 1
        choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question.pk,)))


def repopulate(request):
    repopulate_polls()
    return redirect("polls:index")


def delete_question(request):
    question = get_object_or_404(Question, pk=request.GET["pk"])
    question.delete()
    return redirect("polls:index")


def delete_choice(request: HttpRequest):
    pk = request.GET["pk"]
    source = request.GET["source"]
    choice = get_object_or_404(Choice, pk=pk)
    choice.delete()
    return redirect(source)
