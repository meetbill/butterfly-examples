# coding=utf8
from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.shelve_store import ShelveJobStore
import time
import datetime
import subprocess
import logging


class Result(object):
    def __init__(self, command=None, retcode=None, output=None, cost=None):
        self.command = command or ''
        self.retcode = retcode
        self.output = output
        self.success = False
        self.cost = cost
        if retcode == 0:
            self.success = True


def run_capture(command):
    start_time = time.time()
    outpipe = subprocess.PIPE
    errpipe = subprocess.STDOUT
    process = subprocess.Popen(command, shell=True, stdout=outpipe, stderr=errpipe)
    output, _ = process.communicate()
    output = output.strip('\n')
    end_time = time.time()
    cost = "%.6f" % (end_time - start_time)
    return Result(command=command, retcode=process.returncode, output=output, cost=cost)


def run_cmd(cmd):
    now = datetime.datetime.now()
    exe = run_capture(cmd)
    if exe.success:
        logging.debug(
            '[exe_cmd]:{cmd} [start_time]:{start_time} [cost]:{cost} [Result]:success'.format(
                cmd=cmd, start_time=now, cost=exe.cost))
    else:
        logging.error(
            '[exe_cmd]:{cmd} [start_time]:{start_time} [cost]:{cost} [Result]:error'.format(
                cmd=cmd, start_time=now, cost=exe.cost))


class Crontab(object):
    def __init__(self):
        self._scheduler = Scheduler()
        self._init_crontab()

    def _init_crontab(self):
        self._scheduler.add_jobstore(ShelveJobStore('example.db'), 'shelve')

    def add_job(self, name, rule, cmd):
        #cron_rule = "* * * * * *"
        cron_rule_list = rule.split(' ')
        if len(cron_rule_list) != 6:
            return False

        kwargs = {}
        kwargs["cmd"] = cmd
        self._scheduler.add_cron_job(
            run_cmd,
            second=cron_rule_list[0],
            minute=cron_rule_list[1],
            hour=cron_rule_list[2],
            day=cron_rule_list[3],
            month=cron_rule_list[4],
            day_of_week=cron_rule_list[5],
            name=name,
            jobstore='shelve',
            # args=["xx"],
            kwargs=kwargs
        )
        return True

    def start(self):
        self._scheduler.start()

    def get_jobs(self):
        jobs = []
        for job in self._scheduler.get_jobs():
            # cron_rule
            jobinfo = {}
            fields = job.trigger.fields
            cron = {}
            for field in fields:
                cron[field.name] = str(field)

            cron_rule = "{second} {minute} {hour} {day} {month} {day_of_week}".format(
                second=cron['second'],
                minute=cron['minute'],
                hour=cron['hour'],
                day=cron['day'],
                month=cron['month'],
                day_of_week=cron["day_of_week"]
            )
            jobinfo["rule"] = cron_rule
            jobinfo["nexttime"] = str(job.next_run_time)
            jobinfo["name"] = job.name
            jobinfo["cmd"] = job.kwargs["cmd"]
            jobs.append(jobinfo)
        return jobs

    def remove_job(self, name):
        matchedJobs = self.__get_jobs(name)
        self.__remove_jobs(matchedJobs)

    def __get_jobs(self, name):
        return [job for job in self._scheduler.get_jobs() if job.name == name]

    def __remove_jobs(self, matchedJobs):
        for job in matchedJobs:
            self._scheduler.unschedule_job(job)


if __name__ == "__main__":
    crontab = Crontab()
    #crontab.add_job("test_name","*/3 */4 * * *","cc")
    #crontab.add_job("test1_name","*/3 */4 * * *","cc")
    crontab.start()
    for job in crontab.get_jobs():
        print job
    crontab.remove_job("test_name")
    # cron_rule
    # while True:
    #    print "xxxxxxxxxxxxxxxxxxxxx"
    #    time.sleep(2)
