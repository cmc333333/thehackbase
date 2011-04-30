from django.forms import ModelForm
from journalists.models import Journalist

class JournalistForm(ModelForm):
  class Meta:
    model = Journalist
