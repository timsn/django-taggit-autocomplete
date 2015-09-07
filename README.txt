This is a fork of django-taggit-autocomplete, which can be found at:
https://github.com/Jaza/django-taggit-autocomplete

Made some changes to get it work with Django 1.6+ and removed the webservice (personal preference).
This version is now compatible with jQuery UI 1.11+

Requirements:
	* Django 1.6+
	* Django Taggit (http://github.com/alex/django-taggit)

*** Installation ***

   1. You need to have django-taggit already installed
   2. Download django-taggit-autocomplete and use setup.py to install it on your system:
		python setup.py install
   3. Download jquery and jquery-ui and put it in a folder named "jquery" in your media folder. the media folder is specified in your project's MEDIA_URL setting. If you want to put it somewhere else add TAGGIT_AUTOCOMPLETE_JS_BASE_URL to your project settings.
   4. Add "taggit_autocomplete" to installed apps in your project's settings.

You can customize the path to jquery and jquery-ui in widgets.py (Media class)

*** Usage ***
** Using the model field **

You can use TaggableManager to enable autocompletion right in your models.py file. In most cases this is the easiest solution. Example:

from django.db import models
from taggit_autocomplete.managers import TaggableManager

class SomeModel(models.Model):
        tags = TaggableManager()
