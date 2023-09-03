import os
import json
import pickle
from queue import Queue
from job import Job
from utils.enumString import Status
from utils.get_configs import SettingsFile
from utils.logger import log

settings = SettingsFile().settings


class ProcessNotFinishedException(Exception):
    pass


class Scheduler:
    def __init__(self, pool_size: int = 10) -> None:
        log.info('Scheduler object initialized')
        self.tasks_queue_dict = {}
        self.tasks_queue = Queue()
        self.pool_size = pool_size
        self.tasks_statuses = {}
        self.dependencies = {}
        self.cors_queue = []
        self.path_dump = settings.dump_path

    def put_to_schedule(self, task: Job) -> None:
        if self.tasks_queue.qsize() <= self.pool_size:
            task_run = task.run()
            self.dependencies[task] = task.dependencies
            self.tasks_queue_dict[task] = task_run
            self.tasks_queue.put(task)
            log.info(f'A new task {task} added to the queue')
            self.serialize_object(list(self.tasks_queue_dict.keys()))
        else:
            log.warning('queue is overloaded, task didn`t put')

    def write_to_json(self, task_name: str, task_status: str) -> None:
        self.tasks_statuses[str(task_name)] = {'status': task_status}
        with open(settings.queue_hist_path, 'w') as fp:
            json.dump(self.tasks_statuses, fp, indent=4, skipkeys=True)
        log.info('JSON file refreshed')

    def serialize_object(self, queue: list) -> None:
        if not os.path.exists(os.path.dirname(self.path_dump)):
            os.makedirs(os.path.dirname(self.path_dump))
        with open(self.path_dump, 'wb') as fp:
            pickle.dump(queue, fp)
        log.info(f'File {self.path_dump} serialized')

    def deserialize_objects(self) -> None:
        if os.path.exists(self.path_dump):
            with open(self.path_dump, "rb") as fp:
                self.dump_loaded = pickle.load(fp)
            log.info('dump file loaded')
        else:
            log.info('there is no dump file')

    @staticmethod
    def run_coroutine(coroutin) -> None:
        coroutin.send(None)

    def run_schedule(self) -> None:
        log.info('Schedule started')
        while self.tasks_queue.queue:
            job = self.tasks_queue.get()

            if set(job.dependencies) & set(self.tasks_queue.queue):
                if job.tries:
                    job.tries -= 1
                    self.tasks_queue.put(job)
                    continue
                else:
                    job.status = Status.NO_MORE_TRIES

            try:
                if job.tries:
                    job.tries -= 1
                    job.status = Status.IN_PROGRESS
                    self.tasks_queue_dict[job].send(None)
                    self.tasks_queue.put(job)
                else:
                    job.status = Status.NO_MORE_TRIES
            except StopIteration:
                job.status = Status.FINISHED
            finally:
                self.write_to_json(job, job.status)
                self.serialize_object(list(self.tasks_queue_dict.keys()))
        log.info('All jobs are done!')

    def restore_schedule(self) -> None:
        self.deserialize_objects()
        for task in self.dump_loaded:
            self.put_to_schedule(task)
        self.run_schedule()
        log.warning('queue continued')
