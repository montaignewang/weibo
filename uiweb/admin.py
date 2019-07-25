from django.contrib import admin

# Register your models here.
from . import models
admin.site.register(models.Weibo)
admin.site.register(models.Comment)
admin.site.register(models.UserProfile)
admin.site.register(models.Topic)
admin.site.register(models.Category)
admin.site.register(models.Tags)