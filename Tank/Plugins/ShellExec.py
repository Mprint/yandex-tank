'''
Contains shellexec plugin
'''
from Tank.Core import AbstractPlugin
from Tank.Utils import CommonUtils
import logging

'''
ShellExec plugin
allows executing shell scripts before/after test
'''
class ShellExecPlugin(AbstractPlugin):
    SECTION = 'shellexec'
    
    def __init__(self, core):
        AbstractPlugin.__init__(self, core)
        self.end = None
        self.poll = None
        self.prepare = None
        self.start = None
        self.postprocess = None

    @staticmethod
    def get_key():
        return __file__
    
    def configure(self):
        self.prepare = self.get_option("prepare", '')
        self.start = self.get_option("start", '')
        self.end = self.get_option("end", '')
        self.poll = self.get_option("poll", '')
        self.postprocess = self.get_option("post_process", '')

    def prepare_test(self):
        if self.prepare:
            self.execute(self.prepare)
            
            
    def start_test(self):
        if self.start:
            self.execute(self.start)

    def is_test_finished(self):
        if self.poll:
            self.execute(self.poll)
            
    def end_test(self, retcode):
        if self.end:
            self.execute(self.end)
        return retcode

    def post_process(self, rc):
        if self.postprocess:
            self.execute(self.postprocess)
        return rc

    def execute(self, cmd):
        self.log.debug("Executing: %s", cmd)
        retcode = CommonUtils.execute(cmd, shell=True, poll_period=0.1)
        if retcode:
            raise RuntimeError("Subprocess returned %s",)    