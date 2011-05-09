from journalists.models import Publisher
from journalists.forms import PublisherForm
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import messages

def listPublishers(request):
  params = {"publishers": Publisher.objects.order_by('slug') }
  return render_to_response('publishers/list.xhtml', params, context_instance=RequestContext(request))

def editPublisher(request, id=None, slug=None):
  if not id and not slug:
    instance = Publisher()
  elif id:
    instance = get_object_or_404(Publisher, pk=id)
  elif slug:
    instance = get_object_or_404(Publisher, slug=slug)

  if request.method == 'POST':
    form = PublisherForm(request.POST, instance=instance)
    if form.is_valid():
      instance = form.save()
      messages.success(request, "Saved")
      return HttpResponseRedirect('/publishers/list/')
  else:
    form = PublisherForm(instance=instance)

  return render_to_response('publishers/edit.xhtml', {'publisher': instance, 'form': form},
    context_instance=RequestContext(request))
