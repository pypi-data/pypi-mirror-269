import logging
import time
from threading import Semaphore, Thread
from typing import Optional, Callable, Dict, Any

logger = logging.getLogger(__name__)


class ThreadController:
    def __init__(self, thread_size: int):
        self.sema = Semaphore(thread_size)
        self.thread_size = thread_size

        # a lock/queue for task that are acquiring semaphore
        self.acquiring_lock = []

    def create_thread(self, target: Callable, *, args: Optional[tuple] = None, kwargs: Optional[Dict[str, Any]] = None,
                      disable_sema: Optional[bool] = False, join: Optional[bool] = False):
        self.acquiring_lock.append(1)  # add to queue
        if not disable_sema:
            self.sema.acquire()
            self.acquiring_lock.pop()  # release the acquire lock
        thread = Thread(target=target, args=args, kwargs=kwargs)
        thread.start()
        if join:
            self.sema.acquire()
            if not disable_sema:
                self.sema.release()

    def acquire(self):
        self.sema.acquire()

    def release(self):
        self.sema.release()

    def wait_all_to_finish(self):
        """Check is all the thread completely by acquire"""
        slept_secs = 0
        # wait until no task are asking for semaphore
        max_wait = 12 * 60 * 60  # 12 hours
        while len(self.acquiring_lock) > 0:
            time.sleep(1)
            slept_secs += 1
            if slept_secs % 300 == 0:
                if slept_secs >= max_wait:
                    raise ValueError("Max iteration reached")

        for i in range(self.thread_size):
            self.sema.acquire()
        self.sema.release(n=self.thread_size)


def threaded(*, sema: Optional[Semaphore] = None, join: Optional[bool] = False):
    def threaded_func(func):
        """
        Decorator that multithreads the target function
        with the given parameters. Returns the thread
        created for the function
        """

        def wrapper(*args, **kwargs):
            # acquire sema if sema is provided
            if sema is not None:
                sema.acquire()
            try:
                if args is None: args = tuple()
                if kwargs is None: kwargs = {}
                thread = Thread(target=func, args=args, kwargs=kwargs)
                thread.start()
                if join:
                    thread.join()  # join if sema is provided, and then release
                    if sema is not None:
                        sema.release()
            except Exception as e:
                logger.critical(f"[Helper] Failed to run thread due to exception {e}")
                raise e  # bubble up the exception
            return thread

        return wrapper

    return threaded_func
