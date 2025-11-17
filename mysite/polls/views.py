from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from . import forms

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    quetion_text = question.question_text
    form = forms.QuestionEditForm(instance=question)

    return render(
        request,
        "polls/detail.html",
        {
            "question": question,
            "form": form,
            "question_text": quetion_text,
        }
    )

def update(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.method == 'POST':
        form = forms.QuestionEditForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, "更新しました！")
            return redirect("polls:detail", pk=question.pk)
    else:
        form = forms.QuestionEditForm(instance=question)

    return render(request, 'polls/detail.html', {"question": question, 'form': form})

def choice_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    form = forms.ChoiceForm(request.POST)
    if form.is_valid():
        text = form.cleaned_data["choice_text"]
        Choice.objects.create(
            question=question,
            choice_text=text,
            )
        return redirect("polls:detail", pk=question.pk)
    else:
        form = forms.ChoiceForm()

    return render(request, "polls/detail.html", {
        "question": question,
        "form": form,
    })



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
