# coding: utf-8

from fabkit import *  # noqa
from fablib.base import SimpleBase


class Fluentd(SimpleBase):
    def __init__(self):
        self.data_key = 'fluentd'
        self.data = {
            'etcd_cluster_nodes': [],
        }

        self.packages = {
            'CentOS .*': [
                'wget',
                'td-agent',
            ]
        }

        self.services = {
            'CentOS .*': [
                'td-agent',
            ]
        }

    def init_after(self):
        pass

    def setup(self):
        data = self.init()

        sudo('setenforce 0')
        filer.Editor('/etc/selinux/config').s('SELINUX=enforcing', 'SELINUX=disable')

        Service('firewalld').stop().disable()

        filer.template('/etc/yum.repos.d/treasuredata.repo')

        self.install_packages()

        if filer.template('/etc/td-agent/td-agent.conf', data=data):
            self.handlers['restart_td-agent'] = True

        self.start_services().enable_services()
        self.exec_handlers()
