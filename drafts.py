#!/usr/bin/python

import time
import pickle

# Packages {{{ }}}
# Define params {{{ }}}

# Get existing data
with open('~/.todo') as data_file:
    all_tasks, done_tasks, failed_tasks = pickle.load(data_file)


class TaskItem:

    def __init__(self, task, important=False):
        self.active = True
        # seconds since writing this (an arbitrary value that never repeats)
        self.id = int(time.time()) - 1455707700
        self.task = task
        if important:
            self.important = True
        else:
            self.important = False

    def __print__(self):
        print('[' +
              self.important * '!' + (1 - self.important) * '_' '] ' + str(self.task ) +


    def cross_off(self, completed=True):
        self.active = False
        if completed:
            self.important = True
        else:
            self.important = False

