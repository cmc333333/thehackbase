from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from journalists.forms import *
from django.forms.models import modelformset_factory
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
  params = {'publishers': Journalist2Publisher.objects.filter(journalist = instance)}
  return profile(request, instance, params)

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
  existing = instance.journalist2publisher_set.all()
  factory = modelformset_factory(Journalist2Publisher, Journalist2PublisherForm, extra=0)
  if request.method == 'POST':
    formset = factory(request.POST, prefix="pub")
    if (formset.is_valid()):
      existing_ids = map(lambda x: x.id, existing)
      links = formset.save(commit=False)
      for link in links:
        link.journalist = instance
        if link.id and not (link.id in existing_ids):
          continue
        link.save()
        existing_ids.remove(link.id)
      # Delete the others
      Journalist2Publisher.objects.filter(id__in=existing_ids).delete()
      return HttpResponseRedirect('/journalist/' + str(instance.slug) + '/')
  else:
    formset = factory(prefix="pub", queryset=existing)

  return profile(request, instance, {"form": formset.empty_form, "formset": formset 
    }, 'publishing-history')
