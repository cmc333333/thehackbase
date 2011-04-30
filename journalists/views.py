from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from journalists.forms import JournalistForm
from journalists.models import Journalist
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template import RequestContext

def editJournalist(request, journalist_id=None):
  if journalist_id:
    instance = get_object_or_404(Journalist, pk=journalist_id)
    title = str(instance)
  else:
    instance = Journalist()
    title = 'New Journalist'
  if request.method == 'POST':
    form = JournalistForm(request.POST, instance=instance)
    if form.is_valid():
      instance = form.save()
      messages.success(request, "Saved")
      return HttpResponseRedirect('/journalist/' + str(instance.id))
  else:
    form = JournalistForm(instance=instance)

  params = {'title': title, 'form': form}
  params.update(csrf(request))

  return render_to_response('journalists/new.xhtml', params, context_instance=RequestContext(request))
