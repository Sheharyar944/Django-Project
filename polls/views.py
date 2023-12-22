from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404 , HttpResponseRedirect
from django.urls import reverse
from django.views import generic


from .models import Question, Choice

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list" : latest_question_list,}
    return render(request, 'polls/index.html', context)

# Create your views here.
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)    
    return render(request, 'polls/details.html', {"question" : question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
         selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/details.html', {'question': question, 'error_message' : "you didn't select a choice.",},)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name  = "latest_question_list"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/details.html"

class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    


