from django.forms import ModelForm
from journalists.models import *

class JournalistForm(ModelForm):
  class Meta:
    model = Journalist

class PublisherForm(ModelForm):
  class Meta:
    model = Publisher
