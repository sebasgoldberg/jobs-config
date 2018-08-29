import datetime

class Config:

    def __init__(self):
        self.jobs = []

    def add_job(self, job):
        self.jobs.append(job)

    def get_header(self):
        return '\t'.join([
            'JOBNAME',
            'STEP',
            'PROGRAM',
            'USER',
            'SELNAME',
            'KIND',
            'SIGN',
            'OPTION',
            'LOW',
            'HIGH',
            'START_DATE',
            'START_TIME',
            ])

    def get_line(self, job, step, screen_item):
        return '\t'.join([
            job.get_jobname(),
            str(step.stepnum),
            step.program,
            step.user,
            screen_item.selname,
            screen_item.kind,
            screen_item.sign,
            screen_item.option,
            screen_item.low,
            screen_item.high,
            job.start_date,
            job.start_time,
            ])

    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(self.get_header()+'\n')
            for job in self.jobs:
                for step in job.steps:
                    for screen_item in step.screen_items:
                        line = self.get_line(job, step, screen_item)
                        f.write(line+'\n')

class BaseExecutionInterval:

    def next_datetime(self, actual_datetime):

        raise Exception('Not Implemented')

class NoneExecutionInterval(BaseExecutionInterval):

    def next_datetime(self, actual_datetime):

        return None


class ExecutionInterval(BaseExecutionInterval):

    def __init__(self, delta):
        super(ExecutionInterval, self).__init__()
        self.delta = delta

    def next_datetime(self, actual_datetime):

        return actual_datetime + self.delta


WORKDAY_FROM = datetime.time(8)
WORKDAY_TO = datetime.time(20)

class WorkdayExecutionInterval(ExecutionInterval):
    
    def __init__(self, delta, workday_delta, workday_from=WORKDAY_FROM, workday_to=WORKDAY_TO):
        super(WorkdayExecutionInterval, self).__init__(delta)
        self.workday_delta = workday_delta
        self.workday_from = workday_from 
        self.workday_to = workday_to 

    def next_datetime(self, actual_datetime):


        start_datetime = super(WorkdayExecutionInterval, self).next_datetime()

        if self.workday_from < start_datetime.time() < self.workday_to:
            start_datetime = self.start_datetime + self.workday_delta

        return start_datetime


class MonthlyExecutionInterval(BaseExecutionInterval):

    def __init__(self):
        super(MonthlyExecutionInterval, self).__init__()

    def next_datetime(self, actual_datetime):
        day = actual_datetime.day
        dt1 = actual_datetime.replace(day=1)
        dt2 = dt1 + datetime.timedelta(days=32)
        return dt2.replace(day=day)


class Job:

    def __init__(self, jobname_prefix, start_datetime=None, jobid=1, steps=[]):
        self.jobname_prefix = jobname_prefix
        self.jobid = jobid
        self.start_datetime = start_datetime
        if start_datetime is None:
            self.start_date = ''
            self.start_time = ''
        else:
            self.start_date = self.start_datetime.strftime('%Y%m%d')
            self.start_time = self.start_datetime.strftime('%H%M%S')
        self.steps = []
        for s in steps:
            self.add_step(s)

    def add_step(self, step):
        step.stepnum = len(self.steps) + 1
        self.steps.append(step)

    def get_next_steps(self):
        return [s.next() for s in self.steps]

    def next(self, delta=NoneExecutionInterval()):

        start_datetime = delta.next_datetime(self.start_datetime)

        return Job(
            self.jobname_prefix,
            start_datetime,
            self.jobid+1,
            self.get_next_steps())

    def get_jobname(self):
        return self.jobname_prefix+'_'+str(self.jobid)

    def get_screen_item(self, name):
        return self.steps[-1].get_screen_item(name)

class Step:

    def __init__(self, program, user='', screen_items=None):
        self.program = program
        self.user = user
        self.stepnum = 1
        if screen_items is None:
            self.screen_items = []
        else:
            self.screen_items = screen_items

    def add_screen_item(self, screen_item):
        self.screen_items.append(screen_item)

    def get_next_screen_items(self):
        return [si.next() for si in self.screen_items]

    def next(self):
        return Step(
            self.program,
            self.user,
            self.get_next_screen_items())

    def get_screen_item(self, name):
        for si in reversed(self.screen_items):
            if si.selname == name:
                return si
        raise Exception('Screen item %s not found' % name)

class ScreenItem:

    def __init__(self, selname, low, kind='P', sign='', option='', high=''):
        self.selname = selname
        self.kind = kind
        self.sign = sign
        self.option = option
        self.low = low
        self.high = high

    def next(self):
        return ScreenItem(
            self.selname,
            self.low,
            self.kind,
            self.sign,
            self.option,
            self.high
            )

class ScreenItemDeltaDate(ScreenItem):

    def __init__(self, delta, *args, **kwargs):
        super(ScreenItemDeltaDate, self).__init__(*args)
        self.delta = delta

    def apply_delta(self, value):
        if value == '':
            return ''
        date = datetime.datetime.strptime(value, '%Y%m%d')
        date += self.delta
        return date.strftime('%Y%m%d')

    def next(self):
        return ScreenItemDeltaDate(
            self.delta,
            self.selname,
            self.apply_delta(self.low),
            self.kind,
            self.sign,
            self.option,
            self.apply_delta(self.high)
            )

class ScreenItemDeltaByPeriod(ScreenItem):

    def __init__(self, period_datetime, selname):
        super(ScreenItemDeltaByPeriod, self).__init__(selname, '')
        self.period_datetime = period_datetime
        self.low = self.get_value_from_period_datetime()

    def get_value_from_period_datetime(self):
        raise Exception("Abstract method")

    """
    Not use days grather than 28.
    """
    def get_next_period_datetime(self):
        dt1 = self.period_datetime.replace(day=1)
        dt2 = dt1 + datetime.timedelta(days=32)
        dt3 = dt2.replace(day=self.period_datetime.day)
        return dt3
        
    def next(self):
        return self.__class__(
            self.get_next_period_datetime(),
            self.selname
            )

class ScreenItemYearDeltaByPeriod(ScreenItemDeltaByPeriod):

    def get_value_from_period_datetime(self):
        return self.period_datetime.strftime('%Y')

class ScreenItemPeriodDeltaByPeriod(ScreenItemDeltaByPeriod):

    def get_value_from_period_datetime(self):
        return self.period_datetime.strftime('%m')

class ScreenItemYearPeriodDeltaByPeriod(ScreenItemDeltaByPeriod):

    def get_value_from_period_datetime(self):
        return self.period_datetime.strftime('%Y%m')

"""
Not use days grather than 28.
"""
class ScreenItemDateDeltaByPeriod(ScreenItemDeltaByPeriod):

    def get_value_from_period_datetime(self):
        return self.period_datetime.strftime('%Y%m%d')
