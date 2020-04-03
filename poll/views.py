from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import Q
from django.http import JsonResponse

from .models import Question, Choice
from .forms import QuestionForm, ChoiceForm

# Create your views here.

# Search Function
def search(request):
	queryset = []
	query = request.GET.get('q')
	queries = query.split(" ")
	if queries:
		for q1 in queries:
			searched_questions = Question.objects.filter(
								Q(question_text__icontains = q1) 
		#							Q(choice__icontains = q
								)

			for question in searched_questions:
				queryset.append(question)
	else:
		pass

	queryset = list(set(queryset))

	args = {'latest_question_list':queryset}
	return render(request,
				  'poll/index.html',
				  args)


# Get questions and display them
def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]

	# Question Creation/Delete Form
	form = QuestionForm()	
	context = {}
	query = ''

	if request.method == 'POST':

		if 'create' in request.POST:
			new_question = QuestionForm(request.POST)
			if new_question.is_valid():
				new_question.save()

				return redirect(reverse('poll:index'))

		if 'delete' in request.POST:
			deleted_question = Question.objects.get(pk = request.POST['delete'])
			deleted_question.delete()

			return redirect(reverse('poll:index'))

	args = {'latest_question_list': latest_question_list, 'form': form,}
	args.update(context)
	return render(request,  
				  'poll/index.html',
				  args)

# Display searched questions
def display_searched(request):
	pass

# Show specific question and choices
def detail(request, question_id):
	try:
		selected_question = Question.objects.get(pk=question_id)
		form = ChoiceForm()

		if request.method == 'POST':

			form = ChoiceForm(request.POST)

			if form.is_valid:
				new_choice = form.save(commit = False)
				new_choice.question = selected_question
				new_choice.save()
				return redirect(reverse('poll:detail', kwargs = {'question_id':question_id}))

	except Question.DoesNotExist:
		raise Http404('Question does not exist!')

	args = {'question':selected_question, 'form':form}
	return render(request, 
				  'poll/detail.html', 
				  args)

# Get question and display results
def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)

	args = {'question':question}
	return render(request, 
				  'poll/results.html', 
				  args)

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)

	if request.method == 'POST':

		try:
			selected_choice = question.choice_set.get(pk=request.POST['choice'])

		except(KeyError, Choice.DoesNotExist):
			args = {'question':question, 'error_message':"You didn't select a choice!"}
			# Display voting form
			return render(request,
						  'poll/detail.html',
						  args)

		else:
			selected_choice.votes += 1
			selected_choice.save()

			return redirect(reverse('poll:result', kwargs = {'question_id': question_id}))

def resultsData(request, obj):
	votedata = []

	question = Question.objects.get(id = obj)
	votes = question.choice_set.all()

	for i in votes:
		votedata.append({i.choice_text:i.votes})

	print(votedata)
	return JsonResponse(votedata, safe = False)









