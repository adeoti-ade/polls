from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone


# def index(request):
#     template = 'poll/index.html'
#     latest_questions = Question.objects.order_by("-pub_date")[:5]
#     return render(request, template, {'latest_questions': latest_questions})

# def detail(request, question_id):
#     template = 'poll/detail.html'
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, template, {'question': question})


# def results(request, question_id):
#     template = 'poll/result.html'
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, template, {'question': question})

class IndexView(generic.ListView):
    template_name = 'poll/index.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())\
                                .order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'poll/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultView(generic.DetailView):
    model = Question
    template_name = 'poll/result.html'


def vote(request, question_id):
    template = 'poll/detail.html'
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, template, {'question': question,
                                          'error_message': "you didn't select a choice"})
    else:
        selected_choice.vote += 1
        selected_choice.save()

    return HttpResponseRedirect(reverse('poll:results', args=(question.id,)))