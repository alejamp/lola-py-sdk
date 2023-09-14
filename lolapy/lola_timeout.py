import threading
import time
import warnings
import schedule
from lolapy.lola_context import LolaContext


class LolaTimeout:

    def __init__(self, callback, run_interval=1):
        self.jobs = {}
        self.callback = callback
        self.run_interval = run_interval
        self.timer = None

    def __handle_timeout(self, session, ctx: LolaContext, label):
        print ('Timeout! for session: ', session['id'])
        if self.callback:
            print('LolaTimeout -> Calling callback')
            self.callback(session, ctx, label)
        else:
            print('LolaTimeout -> No callback defined')

        # del jobs[session_id]
        return schedule.CancelJob

    def delete(self, session, ctx: LolaContext, label='default'):
        print(f'Deleting timeout for session: {session["id"]}')
        # Job_id is a combination of session_id and label
        job_id = f'{session["id"]}:{label}'
        if job_id in self.jobs:
            # cancel job
            schedule.cancel_job(self.jobs[job_id])
            del self.jobs[job_id]

    def set(self, session, ctx: LolaContext, timeout_in_seconds, label='default'):
        print(f'Adding timeout for {timeout_in_seconds} seconds')
        # Job_id is a combination of session_id and label
        job_id = f'{session["id"]}:{label}'

        # schedule job
        job = schedule.every(timeout_in_seconds).seconds.do(
                self.__handle_timeout, 
                session, 
                ctx, 
                label
            )
        
        # check if exists
        if job_id in self.jobs:
            # cancel job
            schedule.cancel_job(self.jobs[job_id])

        # register job
        self.jobs[job_id] = job

    def __run_async (self):
        """Continuously run, while executing pending jobs at each
        elapsed time interval.
        @return cease_continuous_run: threading. Event which can
        be set to cease continuous run. Please note that it is
        *intended behavior that run_continuously() does not run
        missed jobs*. For example, if you've registered a job that
        should run every minute and you set a continuous run
        interval of one hour then your job won't be run 60 times
        at each interval but only once.
        """
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    schedule.run_pending()
                    time.sleep(self.run_interval)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run

    def start(self):
        # Start the background thread
        self.stop_run_continuously = self.__run_async()

    def stop(self):
        # Stop the background thread
        self.stop_run_continuously.set()


