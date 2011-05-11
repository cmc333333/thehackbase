from django.forms import ModelForm, CharField, IntegerField, HiddenInput
from journalists.models import *

class JournalistForm(ModelForm):
  class Meta:
    model = Journalist

class Journalist2PublisherForm(ModelForm):
  topics = CharField()
  j2p_id = IntegerField(widget=HiddenInput())
  class Meta:
    model = Journalist2Publisher
    exclude = ('journalist', 'topics')

class PublisherForm(ModelForm):
  class Meta:
    model = Publisher
