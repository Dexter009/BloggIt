

import os
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User
import hashlib

from django.utils import timezone
from django.utils.deconstruct import deconstructible

from pro import settings
from pro.settings import MEDIA_ROOT, MEDIA_URL


class Feeds(models.Model):
    content = models.CharField(max_length=512)
    user = models.ForeignKey(User)
    slug = models.SlugField(max_length=250,default='Feeds Title',
                            unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    creation_date = models.DateTimeField(auto_now=True, blank=True)

@deconstructible
class UploadToPathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):

        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
    image = models.ImageField(upload_to=UploadToPathAndRename(os.path.join(MEDIA_ROOT, 'upload', 'here')), blank=True, null=True)



User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

