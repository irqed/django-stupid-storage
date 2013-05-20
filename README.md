#Django Stupid Storage

Django WebDAV storage written for a stupid infrastructure. Maybe it will be useful for someone else.

Since I've been using it for a big files mainly it uses RQ, but it's an option though.
Note that files uploaded in the loop, so if you gonna upload to many servers (or big files) use queue.

## Requirements

* Python (2.6.5+, 2.7)
* Django (1.4, 1.5)
* django-rq (0.4.6+)
* easywebdav (1.0.7)

## Installation
Install using `pip`

    pip install djangostupidstorage
    
or download from [PyPI](https://pypi.python.org/pypi/djangostupidstorage).

Add `'django_stupid_storage'` to your `INSTALLED_APPS` setting.
```python
    INSTALLED_APPS = (
        ...
        'django_stupid_storage',        
    )
```

Intsall and configure [django-rq](https://github.com/ui/django-rq/) if you don't use it yet.

Add `django_stupid_storage_queue` to `RQ_QUEUES`
```python
RQ_QUEUES = {
    'django_stupid_storage_queue': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    },
}
```

Don't forget to run one or more workers:

    python manage.py rqworker django_stupid_storage_queue

## Example #1
To use one stupid storage add to your settings.py:
```python
    WEBDAV_HOSTS = (
        ('localhost', 1080),
        ('localhost', 1081),
    )
    STUPID_STORAGE_URL = 'http://media.example.com/'
```
Example model:
```python
from django.db import models

from django_stupid_storage import WebDAVStorage

webdav_storage = WebDAVStorage()

class TestModel(models.Model):
    file = models.FileField(upload_to='files/%Y/%m/%d/', storage=webdav_storage)

    def get_absolute_url(self):
        return self.file.url
```
## Example #2
To use more stupid storages you can use class arguments instead of settings.py:
```python
image_storage = WebDAVStorage(upload_to='/%Y/%m/%d/', hosts=image_storage_hosts,
                              storage_url='http://i.example.com/')
video_storage = WebDAVStorage(upload_to='/%Y/%m/%d/', hosts=video_storage_hosts,
                              storage_url='http://v.example.com/', use_queue=True)
```


If you have any ideas feel free to contact me or just send me a pull request:)


