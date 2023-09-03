from scheduler import Scheduler
from weather_informer.weather_fetch import YandexWeatherAPI, CITIES
from job import Job
from files_manager.writer import FileManager
from files_manager.reader import FileReader


def run_sched() -> None:
    """ Функция для запуска планировщика задач """

    job1 = Job(YandexWeatherAPI(), 3, 0, 4, work_list=list(CITIES.values())[:4])
    job2 = Job(YandexWeatherAPI(), 3, 0, 4, work_list=list(CITIES.values())[3:5], dependencies=[job1])
    job5 = Job(FileManager(), 1, 0, 4, work_list=['test_folder_1', 'test_folder_2', 'test_folder_3'])
    job6 = Job(FileReader(), 1, 0, 4, work_list=['queue_hist.json'], dependencies=[job1])

    s = Scheduler()
    s.put_to_schedule(job1)
    s.put_to_schedule(job2)
    s.put_to_schedule(job5)
    s.put_to_schedule(job6)

    s.run_schedule()


if __name__ == '__main__':
    run_sched()
