from django.forms import ModelForm, CharField, IntegerField, HiddenInput
from django.forms.extras.widgets import SelectDateWidget
from journalists.models import *

class JournalistForm(ModelForm):
  class Meta:
    model = Journalist

class Journalist2PublisherForm(ModelForm):
  class Meta:
    model = Journalist2Publisher
    exclude = ('journalist', 'topics')
    widgets = {
      'start': SelectDateWidget(),
      'end': SelectDateWidget()
    }

class PublisherForm(ModelForm):
  class Meta:
    model = Publisher

class WorkForm(ModelForm):
  class Meta:
    model = Work
    exclude = ('journalist')
    widgets = {
      'date': SelectDateWidget(),
    }
