from threading import Timer
from multiprocessing import Process
from functools import wraps
from utils.enumString import Status
from utils.logger import log


def coroutine(func: object) -> object:
    @wraps(func)
    def wrap(*args, **kwargs):
        gen = func(*args, **kwargs)
        gen.send(None)
        return gen
    return wrap


class ProcessNotFinishedException(Exception):
    pass


class Job:
    def __init__(self, task: object, max_working_time: float = -1,
                 start_at: float = 0, tries: int = 0, dependencies: list = None,
                 work_list: list = None):
        """ Инициализация класса """
        self.work_list = work_list
        self.task = task
        self.start_at = start_at
        self.max_working_time = max_working_time
        self.tries = tries
        self.dependencies = dependencies
        if not self.dependencies:
            self.dependencies = []
        self.status = Status.NEW

    def start_process(self, i: str) -> None:
        """ Запуск процесса с учетом ограничений """

        p = Process(target=self.task.start, args=(i,))
        Timer(self.start_at, p.start())
        log.info(f'Process {i} started')
        p.join(timeout=self.max_working_time)
        if p.is_alive():
            p.terminate()
            log.info(f'Process {i} did not finish')
            self.status = Status.FAILED
            raise ProcessNotFinishedException('Процесс завершен с ошибкой')

    @coroutine
    def run(self) -> None:
        """ Запуск корутины с возможностью перезапуска процесса """
        if not self.work_list:
            self.work_list = []
        iteration_list = self.work_list.copy()
        log.info(f'Coroutine for {self.task} generated')
        for work in iteration_list:
            yield
            try:
                log.info(f'Starting {self.task} for {work}')
                self.start_process(work)
                self.work_list.remove(work)
            except ProcessNotFinishedException:
                log.info(f'{self.task} for {work} failed')
                continue
