import unittest
import EllucianEthosPythonClient
import pytz
import datetime

class test_WorkerThread_prefCounterTimeValueISBefore(unittest.TestCase):

  def test_nextTimeSimple(self):
    self.assertEqual(
      EllucianEthosPythonClient.getNextWorkerTime(
        lastRunTime=pytz.timezone('UTC').localize(datetime.datetime(2020, 1, 14, 23, 3, second=5)),
        curTime=pytz.timezone('UTC').localize(datetime.datetime(2020, 1, 14, 23, 3, second=10)),
        frequency=6
      ),
      pytz.timezone('UTC').localize(datetime.datetime(2020, 1, 14, 23, 3, second=11))
    )

  def test_nextTimeMissedRun(self):
    self.assertEqual(
      EllucianEthosPythonClient.getNextWorkerTime(
        lastRunTime=pytz.timezone('UTC').localize(datetime.datetime(2020, 1, 14, 23, 3, second=5)),
        curTime=pytz.timezone('UTC').localize(datetime.datetime(2020, 1, 14, 23, 3, second=13)),
        frequency=6
      ),
      pytz.timezone('UTC').localize(datetime.datetime(2020, 1, 14, 23, 3, second=17))
    )
