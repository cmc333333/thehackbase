from django.forms import ModelForm
from publishers.models import *

class PublisherForm(ModelForm):
  class Meta:
    model = Publisher

