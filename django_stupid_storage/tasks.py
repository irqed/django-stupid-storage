import os
import easywebdav

from django_rq import job


def upload(hosts, temp_path, destination):
    """
    Uploads file to the storeage using webdav
    """
    for host in hosts:
        webdav = easywebdav.Client(host[0], host[1])
        webdav.upload(temp_path, destination)

    try:
        os.remove(temp_path)
    except:
        pass
    return destination
