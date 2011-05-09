from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Publisher(models.Model):
  name = models.CharField(max_length=200)
  
  city = models.CharField(max_length=100)
  state = models.CharField(max_length=100)
  country = models.CharField(max_length=100)

  # generated fields
  slug = models.SlugField(max_length=150, editable=False)

  def __unicode__(self):
    return self.name

  def save(self):
    index = 0
    slug = slugify(self.name)
    valid = False
    while not valid:
      if index:
        self.slug = slug + "-" + str(index)
      else:
        self.slug = slug

      
      if self.id > 0:
        count = Publisher.objects.filter(slug__exact = self.slug).exclude(id__exact = self.id).count()
      else:
        count = Publisher.objects.filter(slug__exact = self.slug).count()

      if count == 0:
        valid = True
      else:
        index = index + 1

    return super(Publisher, self).save()
