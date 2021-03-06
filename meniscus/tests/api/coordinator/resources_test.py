import unittest

import falcon
from mock import MagicMock

from meniscus.api.coordinator.resources import WorkerRegistrationResource
from meniscus.api.coordinator.resources import WorkerRoutesResource
from meniscus.api.coordinator.resources import WorkerWatchlistResource
from meniscus.data.model.worker import Worker
from meniscus.data.model.worker import WorkerRegistration
from meniscus.openstack.common import jsonutils


def suite():
    suite = unittest.TestSuite()
    suite.addTest(WhenTestingWorkerRegistrationOnPost())
    suite.addTest(WhenTestingWorkerRoutesOnGet())
    suite.addTest(WhenTestingWatchlistResource)
    return suite


class WhenTestingWatchlistResource(unittest.TestCase):
    def setUp(self):
        self.db_handler = MagicMock()
        self.resource = WorkerWatchlistResource(self.db_handler)
        self.worker_id = "12345uniqueworkerid"
        self.req = MagicMock()
        self.resp = MagicMock()

    def test_returns_202_on_put(self):
        self.resource.on_put(self.req, self.resp, self.worker_id)
        self.assertEquals(self.resp.status, falcon.HTTP_202)


class WhenTestingWorkerRegistrationOnPost(unittest.TestCase):
    def setUp(self):

        self.db_handler = MagicMock()
        self.resource = WorkerRegistrationResource(self.db_handler)
        self.body = {'worker_registration':
                     WorkerRegistration('correlation').format()}
        self.body_bad_personality = {'worker_registration':
                                     WorkerRegistration(
                                         'bad_personality').format()}
        self.body_bad = {'worker_registration': 'bad_registration'}
        self.registration = jsonutils.dumps(
            {'worker_registration':
             WorkerRegistration('correlation').format()})
        self.req = MagicMock()
        self.req.stream.read.return_value = self.registration
        self.resp = MagicMock()

    def test_returns_202_on_post(self):
        self.resource.on_post(self.req, self.resp)
        self.assertEquals(self.resp.status, falcon.HTTP_202)

        resp_body = jsonutils.loads(self.resp.body)
        self.assertTrue('personality_module' in resp_body)
        self.assertTrue('worker_id' in resp_body)
        self.assertTrue('worker_token' in resp_body)


class WhenTestingWorkerRoutesOnGet(unittest.TestCase):
    def setUp(self):

        self.req = MagicMock()
        self.resp = MagicMock()
        self.registration = WorkerRegistration('correlation').format()
        self.worker_dict = Worker(**self.registration).format()
        self.worker_not_found = None
        self.db_handler = MagicMock()
        self.resource = WorkerRoutesResource(self.db_handler)
        self.worker_id = '51375fc4eea50d53066292b6'
        downstream_setup = WorkerRegistration('storage').format()
        self.downstream = [Worker(**downstream_setup).format(),
                           Worker(**downstream_setup).format(),
                           Worker(**downstream_setup).format()]

    def test_should_return_200(self):
        self.db_handler.find_one.return_value = self.worker_dict
        self.db_handler.find.return_value = self.downstream
        self.resource.on_get(self.req, self.resp, self.worker_id)
        self.assertEquals(self.resp.status, falcon.HTTP_200)
        resp_body = jsonutils.loads(self.resp.body)
        routes = resp_body['routes']
        for route in routes:
            self.assertTrue('service_domain' in route)
            self.assertTrue('targets' in route)
            targets = route['targets']
            for worker in targets:
                self.assertTrue('worker_id' in worker)
                self.assertTrue('ip_address_v4' in worker)
                self.assertTrue('ip_address_v6' in worker)
                self.assertTrue('status' in worker)

if __name__ == '__main__':
    unittest.main()
