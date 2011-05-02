from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from journalists.forms import JournalistForm
from journalists.models import Journalist
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext

def listJournalists(request):
  params = {"journalists": Journalist.objects.order_by('slug') }
  return render_to_response('journalists/list.xhtml', params, context_instance=RequestContext(request))

def editJournalist(request, id=None, slug=None):
  if id:
    instance = get_object_or_404(Journalist, pk=id)
    title = str(instance)
  elif slug:
    instance = get_object_or_404(Journalist, slug=slug)
    title = str(instance)
  else:
    instance = Journalist()
    title = 'New Journalist'
  if request.method == 'POST':
    form = JournalistForm(request.POST, instance=instance)
    if form.is_valid():
      instance = form.save()
      messages.success(request, "Saved")
      return HttpResponseRedirect('/journalist/' + str(instance.slug) +'/')
  else:
    form = JournalistForm(instance=instance)

  params = {'title': title, 'form': form, 'journalist': instance}
  params.update(csrf(request))

  return render_to_response('journalists/edit.xhtml', params, context_instance=RequestContext(request))

def viewJournalist(request, id=None, slug=None):
  if id:
    instance = get_object_or_404(Journalist, pk=id)
    title = str(instance)
  elif slug:
    instance = get_object_or_404(Journalist, slug=slug)
    title = str(instance)
  else:
    raise Http404

  params = {'title': title, 'journalist': instance}

  return render_to_response('journalists/profile.xhtml', params, context_instance=RequestContext(request))
