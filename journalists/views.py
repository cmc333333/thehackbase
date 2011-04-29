from django.shortcuts import render_to_response

def newJournalist(request):
  return render_to_response('journalists/new.xhtml', {'title': 'New Journalist'})
