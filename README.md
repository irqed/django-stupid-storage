#Django Stupid Storage

Django WebDAV storage written for a stupid infrastructure. Maybe it will be helpful for someone else.

Since I've been using it for a big files mainly it uses RQ, but it's an option though. 

## Requirements

* Python (2.6.5+, 2.7)
* Django (1.3, 1.4, 1.5)

## Installation
Install using `pip`...

    pip install djangostupidstorage
    
or download from [PyPI](https://pypi.python.org/pypi/djangostupidstorage).

Add `'django_stupid_storage'` to your `INSTALLED_APPS` setting.
```python
    INSTALLED_APPS = (
        ...
        'django_stupid_storage',        
    )
```
## Example #1
To use one stupid storage add to your settings.py:
```python
    WEBDAV_HOSTS = (
        ('localhost', 1080),
    )
    STUPID_STORAGE_URL = 'http://media.example.com/'
```
Example model:
```python
from django.db import models

from django_stupid_storage import WebDAVStorage

webdav_storage = WebDAVStorage()

class TestModel(models.Model):
    name = models.CharField(max_length=30)
    file = models.FileField(upload_to='files/%Y/%m/%d/', storage=webdav_storage)

    def get_absolute_url(self):
        return self.file.url
```
## Example #2
To use more stupid storages you can use class arguments:
```python
image_storage = WebDAVStorage(hosts=image_storage_hosts, storage_url='http://i.example.com/')
video_storage = WebDAVStorage(hosts=video_storage_hosts, storage_url='http://v.example.com/',
                              use_queue=True)
```





