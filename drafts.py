#!/usr/bin/python

import time
import pickle

# Packages {{{ }}}
# Define params {{{ }}}

# store data in this file
dump_file = '/home/n/.todo'


def load_data(a_file):
    with open(a_file, 'rb') as data_file:
        the_data = pickle.load(data_file)
    return the_data


def save_data(a_file, all_tasks, done_tasks, failed_tasks):
    with open(a_file, 'wb') as data_file:
        the_data = [all_tasks, done_tasks, failed_tasks]
        pickle.dump(the_data, data_file)


class TaskItem:

    def __init__(self, essence, important=False):
        self.active = True
        # unique id of a class instance (=seconds since writing this code)
        self.id = int(time.time()) - 1455707700
        self.essence = essence
        if important:
            self.important = True
        else:
            self.important = False
        return self

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


def print_current(all_tasks):
    print('Don\'t forget to:')
    for task in all_tasks:
        if task.active:
            print(task)
    return


def print_past(done_tasks, failed_tasks):
    print('Completed successfully:')
    for task in done_tasks:
        print(task)
    print('Failed to complete:')
    for task in failed_tasks:
        print(task)


def main():
    """prints active tasks (if present) on starting a shell (zsh/bash/...)"""

    all_tasks = []
    done_tasks = []
    failed_tasks = []
    global dump_file
    # read the data
    [all_tasks, done_tasks, failed_tasks] = load_data(dump_file)

    # print a todo list unless it's empty
    if len(all_tasks) == len(done_tasks) + len(failed_tasks):
        # no active tasks
        return
    elif len(all_tasks) > len(done_tasks) + len(failed_tasks):
        # active tasks present
        print_current(all_tasks)
    else:
        # error
        print("memento.py is broken!")
        exit(1)


def add_task(new_task, important=False, data_file=dump_file):
    """instializes a new TaskItem instance and adds it to the data_file"""

    new_item = TaskItem(essence=new_task, important=important)
    fresh_data = load_data(data_file)
    fresh_data[0].append(new_item)
    save_data(data_file, *fresh_data)


def finish_task(target_id, failed=False, data_file=dump_file):
    data = load_data(data_file)
    for entry in data[0]:
        if entry.id == target_id:
            entry.active = False
            if failed is False:
                data[1].append(entry)
                return "task marked as complete!"
            else:
                data[2].append(entry)
                return "task marked as failed!"
            return "task found, but error happened"
        return "could'n find specified task"

