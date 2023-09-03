import unittest
import os

from scheduler import Scheduler
from job import Job
from weather_informer.weather_fetch import YandexWeatherAPI


class TestSchedule(unittest.TestCase):

    def test_put_to_schedule(self):
        task = Job(YandexWeatherAPI(), work_list=['test3', 'test2', 'test1'])
        s = Scheduler()
        s.put_to_schedule(task)
        self.assertEqual(len(s.tasks_queue), 1)

    def test_serialize_object(self):
        task = Job(YandexWeatherAPI(), work_list=['test3', 'test2', 'test1'])
        s = Scheduler()
        s.serialize_object(task)
        self.assertTrue(os.path.exists(s.path_dump))

if __name__ == "__main__":
    unittest.main()
