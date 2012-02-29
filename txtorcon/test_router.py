
import time
import datetime
from twisted.trial import unittest
from twisted.internet import defer

# outside this package, you can do
from txtorcon.router import Router

class FakeController(object):
    def get_info_raw(self, name):
        d = defer.Deferred()
        d.callback('127.0.0.1=ZZ\nOK')
        return d

class RouterTests(unittest.TestCase):

    def test_ctor(self):
        controller = object()
        router = Router(controller)
        router.update("foo",
                      "AHhuQ8zFQJdT8l42Axxc6m6kNwI",
                      "MAANkj30tnFvmoh7FsjVFr+cmcs",
                      "2011-12-16 15:11:34",
                      "77.183.225.114",
                      "24051", "24052")
        self.assertTrue(router.id_hex == "$00786E43CCC5409753F25E36031C5CEA6EA43702")
        self.assertTrue(router.get_policy() == '')

    def test_flags(self):
        controller = object()
        router = Router(controller)
        router.update("foo",
                      "AHhuQ8zFQJdT8l42Axxc6m6kNwI",
                      "MAANkj30tnFvmoh7FsjVFr+cmcs",
                      "2011-12-16 15:11:34",
                      "77.183.225.114",
                      "24051", "24052")
        router.set_flags("Exit Fast Named Running V2Dir Valid".split())
        self.assertTrue(router.name_is_unique == True)

    def test_policy_accept(self):
        controller = object()
        router = Router(controller)
        router.update("foo",
                      "AHhuQ8zFQJdT8l42Axxc6m6kNwI",
                      "MAANkj30tnFvmoh7FsjVFr+cmcs",
                      "2011-12-16 15:11:34",
                      "77.183.225.114",
                      "24051", "24052")
        router.set_policy("accept 25,128-256".split())
        self.assertTrue(router.accepts_port(25))
        for x in range(128,256):
            self.assertTrue(router.accepts_port(x))
        self.assertTrue(not router.accepts_port(26))
        self.assertTrue(router.get_policy() == 'accept 25,128-256')
        
    def test_policy_reject(self):
        controller = object()
        router = Router(controller)
        router.update("foo",
                      "AHhuQ8zFQJdT8l42Axxc6m6kNwI",
                      "MAANkj30tnFvmoh7FsjVFr+cmcs",
                      "2011-12-16 15:11:34",
                      "77.183.225.114",
                      "24051", "24052")
        router.set_policy("reject 500-600,655,7766".split())
        for x in range(1,500):
            self.assertTrue(router.accepts_port(x))
        for x in range(500,601):
            self.assertTrue(not router.accepts_port(x))

        self.assertTrue(router.get_policy() == 'reject 500-600,655,7766')

    def test_countrycode(self):
        controller = FakeController()
        router = Router(controller)
        router.update("foo",
                      "AHhuQ8zFQJdT8l42Axxc6m6kNwI",
                      "MAANkj30tnFvmoh7FsjVFr+cmcs",
                      "2011-12-16 15:11:34",
                      "127.0.0.1",
                      "24051", "24052")

    def test_policy_error(self):
        router = Router(object())
        try:
            router.set_policy('foo 123')
            self.fail()
        except Exception, e:
            self.assertTrue("Don't understand" in e.message)

    def test_policy_not_set_error(self):
        router = Router(object())
        try:
            router.accepts_port(123)
            self.fail()
        except Exception, e:
            self.assertTrue("set_policy" in e.message)

    def test_repr(self):
        router = Router(FakeController())
        router.update("foo",
                      "AHhuQ8zFQJdT8l42Axxc6m6kNwI",
                      "MAANkj30tnFvmoh7FsjVFr+cmcs",
                      "2011-12-16 15:11:34",
                      "1.2.3.4",
                      "24051", "24052")
        router.set_flags(['Named'])
        r = repr(router)
        
    def test_repr_no_update(self):
        router = Router(FakeController())
        r = repr(router)
        