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

def paramsOr404(id=None, slug=None):
  if id:
    journalist = get_object_or_404(Journalist, pk=id)
    return {'journalist': journalist, 'publishers': journalist.journalist2publisher_set.all(), 
      'works': journalist.work_set.all()}
  elif slug:
    journalist = get_object_or_404(Journalist, slug=slug)
    return {'journalist': journalist, 'publishers': journalist.journalist2publisher_set.all(), 
      'works': journalist.work_set.all()}
  else:
    raise Http404

def profile(request, params = {}, template="profile"):
  params['edit'] = template != "profile";
  return render_to_response('journalists/' + template + '.xhtml', params, context_instance=RequestContext(request))

def viewJournalist(request, id=None, slug=None):
  return profile(request, paramsOr404(id, slug))

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
  params = paramsOr404(id, slug)
  if request.method == 'POST':
    form = JournalistForm(request.POST, instance=params['journalist'])
    if form.is_valid():
      journalist = form.save()
      messages.success(request, "Saved")
      return HttpResponseRedirect('/journalist/' + str(journalist.slug) +'/')
  else:
    form = JournalistForm(instance=params['journalist'])
  params['form'] = form

  return profile(request, params, 'edit')

def editPublishing(request, id=None, slug=None):
  params = paramsOr404(id, slug)
  existing = params['publishers']
  factory = modelformset_factory(Journalist2Publisher, Journalist2PublisherForm, extra=0)
  if request.method == 'POST':
    formset = factory(request.POST, prefix="pub")
    if (formset.is_valid()):
      existing_ids = map(lambda x: x.id, existing)
      links = formset.save(commit=False)
      for link in links:
        link.journalist = params['journalist']
        if link.id and not (link.id in existing_ids):
          continue
        elif link.id:
          existing_ids.remove(link.id)
        link.save()
      # Delete the others
      Journalist2Publisher.objects.filter(id__in=existing_ids).delete()
      return HttpResponseRedirect('/journalist/' + str(params['journalist'].slug) + '/')
  else:
    formset = factory(prefix="pub", queryset=existing)

  params['formset'] = formset

  return profile(request, params, 'publishing-history')

def editWork(request, id=None, slug=None):
  params = paramsOr404(id, slug)
  existing = params['works']
  factory = modelformset_factory(Work, WorkForm, extra=0)
  if request.method == 'POST':
    formset = factory(request.POST, prefix="work")
    if (formset.is_valid()):
      existing_ids = map(lambda x: x.id, existing)
      works = formset.save(commit=False)
      print works
      for work in works:
        work.journalist = params['journalist']
        if work.id and not (work.id in existing_ids):
          continue
        elif work.id:
          existing_ids.remove(work.id)
        work.save()
      # Delete the others
      Work.objects.filter(id__in=existing_ids).delete()
      return HttpResponseRedirect('/journalist/' + str(params['journalist'].slug) + '/')
  else:
    formset = factory(prefix="work", queryset=existing)

  params['formset'] = formset

  return profile(request, params, 'work')
