from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import Count

from polls2.models import Poll, Choice

### Without using generic templates
# def index(request):
# 	### Long way
# 	# latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
# 	# # output = ', '.join([p.question for p in latest_poll_list])	
# 	# template = loader.get_template('polls/index.html')
# 	# context = RequestContext(request, {'latest_poll_list': latest_poll_list})
# 	# return HttpResponse(template.render(context))
# 	latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
# 	context = {'latest_poll_list': latest_poll_list}
# 	return render(request, 'polls/index.html', context)

# def detail(request, poll_id):
# 	### Long was to raise 404
# 	# try:
# 	# 	poll = Poll.objects.get(pk=poll_id)
# 	# except Poll.DoesNotExist:
# 	# 	raise Http404
# 	poll = get_object_or_404(Poll, pk=poll_id)
# 	context = {'poll': poll}
# 	return render(request, 'polls/detail.html', context)

# def results(request, poll_id):
# 	poll = Poll.objects.get(pk=poll_id)
# 	return render(request, 'polls/results.html', {'poll': poll})

def vote(request, poll_id):
	poll = get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choice = poll.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {'poll': poll, 'error_message': "Please select a choice!"})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls2:results', args=(poll.id,)))


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_poll_list'

	def get_queryset(self):
		return Poll.objects.annotate(count = Count('choice')).filter(pub_date__lte=timezone.now(), count__gt=0).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
	model = Poll
	template_name = 'polls/detail.html'

	def get_queryset(self):
		return Poll.objects.annotate(count = Count('choice')).filter(pub_date__lte=timezone.now(), count__gt=0)


class ResultsView(generic.DetailView):
	model = Poll
	template_name = 'polls/results.html'

	def get_queryset(self):
		return Poll.objects.annotate(count = Count('choice')).filter(pub_date__lte=timezone.now(), count__gt=0)






