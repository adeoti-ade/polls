from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic


# def index(request):
#     template = 'article/index.html'
#     latest_questions = Question.objects.order_by("-pub_date")[:5]
#     return render(request, template, {'latest_questions': latest_questions})

# def detail(request, question_id):
#     template = 'article/detail.html'
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, template, {'question': question})


# def results(request, question_id):
#     template = 'article/result.html'
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, template, {'question': question})

class IndexView(generic.ListView):
    template_name = 'article/index.html'
    context_object_name = 'latest_questions'

    def queryset(self):

        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'article/detail.html'

class ResultView(generic.DetailView):
    model = Question
    template_name = 'article/result.html'


def vote(request, question_id):
    template = 'article/detail.html'
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, template, {'question': question,
                                          'error_message': "you didn't select a choice"})
    else:
        selected_choice.vote += 1
        selected_choice.save()

    return HttpResponseRedirect(reverse('article:results', args=(question.id,)))