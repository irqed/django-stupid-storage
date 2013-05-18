import easywebdav

from django_rq import job


@job('django_stupid_storage_queue')
def upload(hosts, temp_path, name):
    """
    Uploads file to the storeage using webdav
    """
    for host in hosts:
        webdav = easywebdav.Client(host[0], host[1])
        webdav.upload(temp_path, name)

    return name
