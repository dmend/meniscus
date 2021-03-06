import platform
import uuid

from datetime import datetime

import meniscus.api.utils.sys_assist as sys_assist


class Worker(object):
    def __init__(self, **kwargs):

        self._id = kwargs.get('_id', None)
        self.worker_id = kwargs.get('worker_id', str(uuid.uuid4()))
        self.worker_token = kwargs.get('worker_token', str(uuid.uuid4()))
        self.hostname = kwargs['hostname']
        self.callback = kwargs['callback']
        self.ip_address_v4 = kwargs['ip_address_v4']
        self.ip_address_v6 = kwargs['ip_address_v6']
        self.personality = kwargs['personality']
        self.status = kwargs['status']
        self.system_info = SystemInfo(**kwargs['system_info'])

    def format(self):
        return{
            'worker_id': self.worker_id,
            'worker_token': self.worker_token,
            'hostname': self.hostname,
            'callback': self.callback,
            'ip_address_v4': self.ip_address_v4,
            'ip_address_v6': self.ip_address_v6,
            'personality': self.personality,
            'status': self.status,
            'system_info': self.system_info.format()
        }

    def format_for_save(self):
        worker_dict = self.format()
        worker_dict['_id'] = self._id
        return worker_dict

    def get_registration_identity(self):
        return{
            'personality_module': 'meniscus.personas.{0}.app'
            .format(self.personality),
            'worker_id': self.worker_id,
            'worker_token': self.worker_token
        }

    def get_status(self):
        return{
            'hostname': self.hostname,
            'worker_id': self.worker_id,
            'ip_address_v4': self.ip_address_v4,
            'ip_address_v6': self.ip_address_v6,
            'personality': self.personality,
            'status': self.status,
            'system_info': self.system_info.format()
        }

    def get_route_info(self):
        return {
            'worker_id': self.worker_id,
            'ip_address_v4': self.ip_address_v4,
            'ip_address_v6': self.ip_address_v6,
            'status': self.status
        }


class WorkerRegistration(object):
    def __init__(self, personality, status='new'):
        self.hostname = platform.node()
        self.ip_address_v4 = sys_assist.get_lan_ip()
        self.ip_address_v6 = ""
        self.callback = self.ip_address_v4 + ':8080/v1/callback'
        self.personality = personality
        self.status = status
        self.system_info = SystemInfo()

    def format(self):
        return{
            'hostname': self.hostname,
            'callback': self.callback,
            'ip_address_v4': self.ip_address_v4,
            'ip_address_v6': self.ip_address_v6,
            'personality': self.personality,
            'status': self.status,
            'system_info': self.system_info.format()
        }


class SystemInfo(object):
    def __init__(self, **kwargs):
        if kwargs:
            self.cpu_cores = kwargs['cpu_cores']
            self.os_type = kwargs['os_type']
            self.memory_mb = kwargs['memory_mb']
            self.architecture = kwargs['architecture']
            self.load_average = kwargs['load_average']
            self.disk_usage = kwargs['disk_usage']
        else:
            self.cpu_cores = sys_assist.get_cpu_core_count()
            self.os_type = platform.platform()
            self.memory_mb = sys_assist.get_sys_mem_total_MB()
            self.architecture = platform.machine()
            self.load_average = sys_assist.get_load_average()
            self.disk_usage = sys_assist.get_disk_usage()

    def format(self):
        return {
            'cpu_cores': self.cpu_cores,
            'os_type': self.os_type,
            'memory_mb': self.memory_mb,
            'architecture': self.architecture,
            'load_average': self.load_average,
            'disk_usage': self.disk_usage
        }


class WorkerConfiguration(object):
    def __init__(self, personality, personality_module, worker_token,
                 worker_id, coordinator_uri):

        self.personality = personality
        self.personality_module = personality_module
        self.worker_token = worker_token
        self.worker_id = worker_id
        self.coordinator_uri = coordinator_uri

    def format(self):

        return{
            'personality': self.personality,
            'personality_module': self.personality_module,
            'worker_token': self.worker_token,
            'worker_id': self.worker_id,
            'coordinator_uri': self.coordinator_uri
        }


class WatchlistItem(object):
    """
    Watchlist table item for keeping track of workers that are unresponsive
    """
    def __init__(self, worker_id, last_changed=None, watch_count=None,
                 _id=None, ):

        self.worker_id = worker_id
        self._id = _id

        if _id is None:
            self.last_changed = datetime.now()
            self.watch_count = 1
        else:
            self.last_changed = last_changed
            self.watch_count = watch_count

    def format(self):
        return {
            'worker_id': self.worker_id,
            'last_changed': self.last_changed,
            'watch_count': self.watch_count,
        }

    def format_for_save(self):
        worker_dict = self.format()
        worker_dict['_id'] = self._id
        return worker_dict
