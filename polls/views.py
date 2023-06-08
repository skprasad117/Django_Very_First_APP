from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render # either render or loader can be used
from django.urls import reverse
# render provide much shorter apprach than loader

# using render can avoid the use of HttpResponse and loader giving much shorter approach


from .models import Question, Choice

# from django.http import HttpResponse
# from django.template import loader 
# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     template = loader.get_template("polls/index.html")
#     context = {
#         "latest_question_list": latest_question_list,
#     }
# def detail(request, question_id):
#     return HttpResponse("You're looking at the question %s." % question_id)



# Another Method

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list": latest_question_list,
    }
    
    return render(request,"polls/index.html", context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        # a shorter way
        # question = Question.objects.get_object_or_404(pk=question_id) 
        # return render(request, "polls/detail.html",{"question": question})
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request,"polls/detail.html",{"question":question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])

    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html",
        {"question" : question,
         "error_message" : "did not selected a choice"},)
    else: 
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))