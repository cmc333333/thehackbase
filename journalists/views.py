from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from journalists.forms import *
from journalists.models import *
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
import logging

def listJournalists(request):
  params = {"journalists": Journalist.objects.order_by('slug') }
  return render_to_response('journalists/list.xhtml', params, context_instance=RequestContext(request))

def journalistOr404(id=None, slug=None):
  if id:
    return get_object_or_404(Journalist, pk=id)
  elif slug:
    return get_object_or_404(Journalist, slug=slug)
  else:
    raise Http404

def profile(request, journalist, params = {}, template="profile"):
  params['journalist'] = journalist;
  params['edit'] = template != "profile";
  return render_to_response('journalists/' + template + '.xhtml', params, context_instance=RequestContext(request))


def viewJournalist(request, id=None, slug=None):
  instance = journalistOr404(id, slug)
  return profile(request, instance)

def newJournalist(request):
  instance = Journalist()
  if request.method == 'POST':
    form = JournalistForm(request.POST, instance=instance)
    if form.is_valid():
      instance = form.save()
      messages.success(request, "Saved")
      return HttpResponseRedirect('/journalist/' + str(instance.slug) +'/')
  else:
    form = JournalistForm(instance=instance)

  return render_to_response('journalists/new.xhtml', {'journalist': instance, 'form': form},
    context_instance=RequestContext(request))

def editJournalist(request, id=None, slug=None):
  instance = journalistOr404(id, slug)
  if request.method == 'POST':
    form = JournalistForm(request.POST, instance=instance)
    if form.is_valid():
      instance = form.save()
      messages.success(request, "Saved")
      return HttpResponseRedirect('/journalist/' + str(instance.slug) +'/')
  else:
    form = JournalistForm(instance=instance)

  return profile(request, instance, {'form': form}, 'edit')

def editPublishing(request, id=None, slug=None):
  instance = journalistOr404(id, slug)

  return profile(request, instance, {"publishers": Publisher.objects.order_by('name')}, 'publishing-history')
