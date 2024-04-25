###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
import traceback
from concurrent.futures import ThreadPoolExecutor, Future, wait
from contextvars import Context, copy_context
from threading import Thread as _Thread, Semaphore
from typing import Any
from everysk.core.log import Logger


# Create a Thread log to print all errors
log = Logger(name='everysk-thread-error-log')


class Thread(_Thread):
    results: list = None
    semaphore: Semaphore = None

    def __init__(self, target: callable, args: tuple = (), kwargs: dict = None, results: list = None, semaphore: Semaphore = None):
        """
        Base class to implement Threads, the main difference for a normal Thread is the use
        of semaphores and store the results of every call.
        We need to pass the function that will be executed in the Thread.
        Semaphore needs to be created before to works.

        Args:
            target (callable): The function that will be executed in the Thread.
            args (tuple, optional): The arguments that are needed to this function. Defaults to ().
            kwargs (dict, optional): The keyword arguments that are needed to this function. Defaults to None.
            results (list, optional): A list to store the result from the target. Defaults to None.
            semaphore (Semaphore, optional): The semaphore to control the rate execution. Defaults to None.

        Example:

            >>> from everysk.core.threads import Thread
            >>> def sum(a: int, b: int) -> int:
            ...     return a + b

            >>> results = []
            >>> Thread(target=sum, args=(1, 1), results=results).start()
            >>> Thread(target=sum, args=(2, 2), results=results).start()
            >>> results
            [2, 4]

        """
        self.results = results
        self.semaphore = semaphore
        super().__init__(target=target, args=args, kwargs=kwargs)

    def start(self) -> None:
        """
        Send the execution of the "target" inside a Thread, if semaphore exists this
        function will be blocked until we have a free slot.
        """
        if self.semaphore is None or self.semaphore.acquire(blocking=True):
            super().start()

    def run(self) -> None:
        """
        Method that really execute the "target".
        After it finish it's execution we release the semaphore if needed.
        """
        try:
            if self._target is not None:
                try:
                    # To avoid infinite running Threads we capture the exception and log it.
                    result = self._target(*self._args, **self._kwargs)

                    # Then we store the result
                    if self.results is not None:
                        self.results.append(result)

                except Exception: # pylint: disable=broad-exception-caught
                    log.error(
                        'Thread execution error. target: %s, args: %s, kwargs: %s, traceback: %s',
                        self._target,
                        self._args,
                        self._kwargs,
                        traceback.format_exc()
                    )

        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs

        if self.semaphore is not None:
            self.semaphore.release()


class ThreadPool(ThreadPoolExecutor):
    context: Context = None
    default_error_value: Any = Undefined
    futures: list[Future] = None
    results: list = None
    silent: bool = True

    def __init__(self, concurrency: int | None = None, silent: bool = True, default_error_value: Any = Undefined) -> None:
        """
        ThreadPool is a queue to execute threads and control the concurrency.
        If some error occur inside a Thread, we raise the exception or just log the exception.
        If concurrency is not passed, then the default value is min(32, os.cpu_count() + 4).

        Args:
            concurrency (int | None, optional): The number of Threads that will be running simultaneously. Defaults to None.
            silent (bool, optional): To log the error or raise. Defaults to True.
            default_error (Any, optional): The default value to be stored as result if an error occur. Defaults to Undefined.

        Example:

            >>> from time import sleep
            >>> from everysk.core.datetime import DateTime
            >>> from everysk.core.threads import ThreadPool

            >>> def sum(a: int, b: int) -> int:
            ...     print(DateTime.now().strftime('%H:%M:%S'))
            ...     sleep(1)
            ...     return a + b

            >>> pool = ThreadPool(6)
            >>> for i in range(0, 6):
            ...     pool.add(target=sum, args=(i, i))
            >>> pool.wait()
            19:24:22
            19:24:22
            19:24:22
            19:24:22
            19:24:22
            19:24:22
            >>> pool.results
            [0, 2, 4, 6, 8, 10]

            >>> pool = ThreadPool(2)
            >>> for i in range(0, 6):
            ...     pool.add(target=sum, args=(i,i))
            >>> pool.wait()
            19:25:09
            19:25:09
            19:25:10
            19:25:10
            19:25:11
            19:25:11
            >>> pool.results
            [0, 2, 4, 6, 8, 10]
        """
        self.context = copy_context()
        self.futures = []
        self.results = []
        self.silent = silent
        self.default_error_value = default_error_value
        super().__init__(concurrency, initializer=self._set_child_context)

    def _set_child_context(self) -> None:
        """ Used to pass the context values to the child Threads. """
        for var, value in self.context.items():
            var.set(value)

    def add(self, target: callable, args: tuple = (), kwargs: dict = None) -> None:
        """
        Add the target to the queue to be processed later in a Thread.

        Args:
            target (callable): The function that will be executed in the Thread.
            args (tuple, optional): The arguments that are needed to this function. Defaults to ().
            kwargs (dict, optional): The keyword arguments that are needed to this function. Defaults to None.
        """
        if kwargs is None:
            kwargs = {}

        future = self.submit(target, *args, **kwargs)
        # We add these info on the future to be used later if some error occur
        future.target = target
        future.args = args
        future.kwargs = kwargs

        self.futures.append(future)

    def wait(self) -> None:
        """ This method is used to wait for all threads to complete and generate the results. """
        wait(self.futures)

        for future in self.futures:
            try:
                self.results.append(future.result())
            except Exception as error: # pylint: disable=broad-exception-caught
                if self.silent:
                    self.results.append(self.default_error_value)
                    log.error(
                        'Thread execution error -> target: %s, args: %s, kwargs: %s, traceback: %s',
                        future.target,
                        future.args,
                        future.kwargs,
                        traceback.format_exc()
                    )
                else:
                    raise error

        # This is a Garbage Collector for the ThreadPool
        self.shutdown()
