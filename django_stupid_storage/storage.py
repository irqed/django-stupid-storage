import re
import uuid
import random
import urlparse
import easywebdav

from types import MethodType

from django.conf import settings
from django.core.files import base
from django.core.files.storage import Storage
from django.core.exceptions import ImproperlyConfigured

from django_stupid_storage import tasks


def exists(self, remote_path):
    """
    Unfortunately easywebdav doesn't have this method at the moment.
    And my pull request is left without any attention.
    """
    response = self._send('HEAD', remote_path, (200, 201, 404))

    return True if response.status_code != 404 else False

#Monkeypatch Client class
easywebdav.Client.exists = MethodType(exists, None, easywebdav.Client)


class WebDAVStorage(Storage):
    """
    WebDAVStorage saves files by copying them on several servers listed in
    settings.WEBDAV_HOSTS
    """
    def __init__(self, hosts=None, storage_url=None, use_queue=False, **kwargs):
        super(WebDAVStorage, self).__init__(**kwargs)
        self.use_queue = use_queue
        if hosts is None:
            try:
                self.hosts = settings.WEBDAV_HOSTS
            except:
                raise ImproperlyConfigured('WEBDAV_HOSTS is not defined in'
                                           'settings.py.'
                                           'And hosts argument is None')
        if storage_url is None:
            try:
                self.storage_url = settings.STUPID_STORAGE_URL
            except:
                raise ImproperlyConfigured('STUPID_STORAGE_URL'
                                           'is not defined in settings.py.'
                                           'And storage_url argument is None')

    def _open(self, name, mode='rb'):
        if mode != 'rb':
            raise IOError('Illegal mode "%s". Only "rb" is supported.')
        host = random.choice(self.hosts)
        webdav = easywebdav.Client(host[0], host[1])
        return base.ContentFile(webdav.download(name))

    def _save(self, name, content):
        """
        Puts a task on a queue.
        """
        if self.use_queue:
            tasks.upload.delay(self.hosts, content.file.temporary_file_path(),
                               name)
        else:
            tasks.upload(self.hosts, content.file.temporary_file_path(), name)

        return name

    def exists(self, name):
        """
        Returns True if a file referensed by the given name already exists
        in the storage cluster, or False if the name is available for
        a new file.
        """
        for host in self.hosts:
            webdav = easywebdav.Client(host[0], host[1])
            if webdav.exists(name):
                return True

        return False

    def url(self, name):
        return urlparse.urljoin(self.storage_url, name).replace('\\', '/')

    def delete(self, name):
        for host in self.hosts:
            webdav = easywebdav.Client(host[0], host[1])
            webdav.delete(name)

    def get_valid_name(self, name):
        if not (re.match('^[a-zA-Z0-9-_]*$', name)):
            ext = name.split('.')[-1]
            name = str(uuid.uuid4()) + '.' + ext.lower()
        return name
