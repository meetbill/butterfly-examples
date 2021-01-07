# coding=utf8
import os
import re
import time
import datetime
import subprocess
import logging

from xlib.apscheduler import scheduler
from xlib.apscheduler.jobstores import shelve_store
from xlib.apscheduler import triggers

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
    if "rm" in cmd:
        return False

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
    def __init__(self, db="./data/cron.db"):
        self._db_path = db
        self._scheduler = scheduler.Scheduler()
        self._init_crontab()

    def _init_crontab(self):
        dir = os.path.dirname(self._db_path)
        if not os.path.isdir(dir):
            os.makedirs(dir)

        self._scheduler.add_jobstore(shelve_store.ShelveJobStore(self._db_path), 'shelve')

    def add_cron_job(self, name, cmd, rule):
        """
        创建 cron 任务
        Args:
            name: job name
            cmd : job cmd
            rule: "* * * * * *"
        """
        cron_rule_list = rule.split(' ')
        if len(cron_rule_list) != 6:
            return False

        # 删除同名 job
        self.remove_job(name)

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
            kwargs=kwargs
        )
        return True

    def add_interval_job(self, name, cmd, rule):
        """
        添加间隔任务
        Args:
            name: job name
            cmd : job cmd
            rule: Xs/Xm/Xh/Xd
        """
        interval_cron_dict = {}
        interval_cron_dict["days"] = 0
        interval_cron_dict["hours"] = 0
        interval_cron_dict["minutes"] = 0
        interval_cron_dict["seconds"] = 0

        rule_list = re.findall(r"[0-9]+|[a-z]+", rule)
        if len(rule_list) != 2:
            return False

        if rule_list[1] not in ["s", "m", "h", "d"]:
            return False

        if rule_list[1] == "s":
            interval_cron_dict["seconds"] = int(rule_list[0])
        elif rule_list[1] == "m":
            interval_cron_dict["minutes"] = int(rule_list[0])
        elif rule_list[1] == "h":
            interval_cron_dict["hours"] = int(rule_list[0])
        elif rule_list[1] == "d":
            interval_cron_dict["days"] = int(rule_list[0])

        # 删除同名 job
        self.remove_job(name)

        kwargs = {}
        kwargs["cmd"] = cmd
        self._scheduler.add_interval_job(
            run_cmd,
            days=interval_cron_dict["days"],
            hours=interval_cron_dict["hours"],
            minutes=interval_cron_dict["minutes"],
            seconds=interval_cron_dict["seconds"],
            name=name,
            jobstore='shelve',
            kwargs=kwargs
        )
        return True


    def add_date_job(self, name, cmd, rule):
        """
        添加一次任务
        Args:
            name: job name
            cmd : job cmd
            rule: "2020-12-16 18:03:17"/"2020-12-16 18:05:17.682862"
        """
        # 删除同名 job
        self.remove_job(name)

        kwargs = {}
        kwargs["cmd"] = cmd
        self._scheduler.add_date_job(
            run_cmd,
            date=rule,
            name=name,
            jobstore='shelve',
            kwargs=kwargs
        )

    def start(self):
        """
        启动 scheduler
        """
        self._scheduler.start()

    def get_jobs(self):
        """
        获取所有任务

        job.__dict__
        {
            'runs': 0,
            'args': [],
            'name': u'test_name',
            'misfire_grace_time': 1,
            'instances': 0,
            '_lock': <thread.lock object at 0x10241c5d0>,
            'next_run_time': datetime.datetime(2020, 12, 15, 19, 48),
            'max_instances': 1,
            'max_runs': None,
            'coalesce': True,
            'trigger': <CronTrigger (month='*', day='*', day_of_week='*', hour='*', minute='*/4', second='*/3')>,
            'func': <function run_cmd at 0x102676140>,
            'kwargs': {'cmd': 'cc'},
            'id': '512965'
        }
        """
        jobs = []
        for job in self._scheduler.get_jobs():
            # cron_rule
            jobinfo = {}

            rule = ""
            trigger = ""
            if isinstance(job.trigger, triggers.CronTrigger):
                trigger = "cron"
                fields = job.trigger.fields
                cron = {}
                for field in fields:
                    cron[field.name] = str(field)
                rule = "{second} {minute} {hour} {day} {month} {day_of_week}".format(
                    second=cron['second'],
                    minute=cron['minute'],
                    hour=cron['hour'],
                    day=cron['day'],
                    month=cron['month'],
                    day_of_week=cron["day_of_week"]
                )

            if isinstance(job.trigger, triggers.IntervalTrigger):
                trigger = "interval"
                rule = str(job.trigger.interval_length) + "s"

            if isinstance(job.trigger, triggers.SimpleTrigger):
                trigger = "date"
                rule = str(job.trigger.run_date)

            jobinfo["id"] = job.id
            jobinfo["rule"] = rule
            jobinfo["nexttime"] = str(job.next_run_time)
            jobinfo["name"] = job.name
            jobinfo["cmd"] = job.kwargs["cmd"]
            jobinfo["trigger"] = trigger
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

    crontab.add_cron_job("test_cron1","cc", "*/3 */4 * * * *")
    crontab.add_cron_job("test_cron2","cc", "*/3 */4 * * * *")
    crontab.add_cron_job("test_cron3","cc", "*/3 */4 * * * *")
    crontab.add_interval_job("test_interval1","cc", "10s")
    #crontab.add_date_job("test_date1","cc", "2020-12-16 21:40:00")

    # start
    crontab.start()

    for job in crontab.get_jobs():
        print job

    #crontab.remove_job("test_name")

    #while True:
    #    time.sleep(2)
