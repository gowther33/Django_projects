from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User

# We need our apps to be independent of other apps.
# To achive this we make generic relations
# ContentType model from django is used to create generic relations



class Tag(models.Model):
    label = models.CharField(max_length=255)


class TaggedItem(models.Model):
    # What tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    # To define generic relations we define 3 fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) # Type of content: product, video, image, article etc used for searching for table
    object_id = models.PositiveIntegerField() # object id
    content_object = GenericForeignKey() # Actual object
