# coding: utf-8

from fabkit import task, parallel
from fablib.fluentd import Fluentd


@task
@parallel
def setup():
    fluentd = Fluentd()
    fluentd.setup()
