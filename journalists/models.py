from django.db import models
from djangotoolbox.fields import ListField
from django.template.defaultfilters import slugify
from publishers.models import Publisher

# Create your models here.
class Journalist(models.Model):
  first = models.CharField(max_length=200)
  middle = models.CharField(max_length=200, blank = True)
  last = models.CharField(max_length=200)
  suffix = models.CharField(max_length=200, blank = True)
  description = models.TextField(blank = True)

  # generated fields
  slug = models.SlugField(max_length=150, editable=False)
  
  def __unicode__(self):
    return "%s %s" % (self.first, self.last)
  def toString(self):
    return str(self)

  def save(self):
    index = 0
    slug = slugify("%s %s %s %s" % (self.last, self.first, self.middle, self.suffix))[:150]
    valid = False
    while not valid:
      if index:
        self.slug = slug + "-" + str(index)
      else:
        self.slug = slug

      
      if self.id > 0:
        count = Journalist.objects.filter(slug__exact = self.slug).exclude(id__exact = self.id).count()
      else:
        count = Journalist.objects.filter(slug__exact = self.slug).count()

      if count == 0:
        valid = True
      else:
        index = index + 1

    return super(Journalist, self).save()

class Journalist2Publisher(models.Model):
  journalist = models.ForeignKey(Journalist)
  publisher = models.ForeignKey(Publisher)

  start = models.DateField()
  end = models.DateField(null = True, blank = True)

  topics = ListField(default = [])

  def __unicode__(self):
    return "%s @ %s" % (self.journalist, self.publisher)

class Work(models.Model):
  journalist = models.ForeignKey(Journalist)

  title = models.CharField(max_length=200)
  date = models.DateField()

  permalink = models.CharField(max_length=200)
  def __unicode__(self):
    return self.title
