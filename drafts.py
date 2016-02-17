#!/usr/bin/python

import time
import pickle

# Packages {{{ }}}
# Define params {{{ }}}
dump_file = '/home/n/.todo'


def load_data():
    with open(dump_file, 'rb') as data_file:
        all_tasks, done_tasks, failed_tasks = pickle.load(data_file)


def save_data():
    global all_tasks
    global done_tasks
    global failed_tasks
    with open(dump_file, 'wb') as data_file:
        the_data = [all_tasks, done_tasks, failed_tasks]
        pickle.dump(the_data, data_file)


class TaskItem:

    def __init__(self, essence, important=False):
        self.active = True
        # seconds since writing this (an arbitrary value that never repeats)
        self.id = int(time.time()) - 1455707700
        self.essence = essence
        if important:
            self.important = True
        else:
            self.important = False

    def __print__(self):

        print('\t[' + '!' * self.important + '_' * (1 - self.important) + '] ',
              end=' ')
        print(self.essence, end='\t')
        print(self.id, end='\n')

    def cross_off(self, completed=True):
        self.active = False
        if completed:
            self.important = True
        else:
            self.important = False


def print_current(all_tasks=all_tasks):
    for task in all_tasks:
        if task.active:
            print(task)


def print_past(done_tasks=done_tasks, failed_tasks=failed_tasks):
    print('Completed successfully:')
    for task in done_tasks:
        print(task)
    print('Failed to complete:')
    for task in failed_tasks:
        print(task)


# +----------------+
# | TODO: argparse |
# +----------------+
