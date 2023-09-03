from enum import StrEnum


class Status(StrEnum):
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    SUCCESS = 'success'
    FINISHED = 'finished'
    FAILED = 'failed'
    NO_MORE_TRIES = 'not_finished_no_more_tries'
