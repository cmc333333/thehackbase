from django.db import models
from djangotoolbox.fields import ListField

# Create your models here.
class Journalist(models.Model):
  first = models.CharField(max_length=200)
  middle = models.CharField(max_length=200, blank = True)
  last = models.CharField(max_length=200)
  suffix = models.CharField(max_length=200, blank = True)

  # generated fields
  normalized_name = models.CharField(max_length=800, editable=False)

  def __unicode__(self):
    return "%s %s" % (self.first, self.last)

  def save(self):
    self.normalized_name = ("%s, %s %s %s" % (self.last.lower(), self.first.lower(), self.middle.lower(), 
      self.suffix.lower())).strip()
    return super(Journalist, self).save()

class Publisher(models.Model):
  name = models.CharField(max_length=200)
  
  city = models.CharField(max_length=100)
  state = models.CharField(max_length=100)
  country = models.CharField(max_length=100)

  def __unicode__(self):
    return self.name

class Journalist2Publisher(models.Model):
  journalist = models.ForeignKey(Journalist)
  publisher = models.ForeignKey(Publisher)

  start = models.DateField()
  end = models.DateField(null = True, blank = True)

  topics = ListField(default = [])

  def __unicode__(self):
    return "%s @ %s" % (self.journalist, self.publisher)
