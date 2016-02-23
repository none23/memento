#!/usr/bin/python

import sys
import time
import pickle
import argparse

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

    def __init__(self, essence, id, important=False):
        self.active = True
        self.id = id
        self.essence = essence
        if important:
            self.important = True
        else:
            self.important = False

    def __str__(self):
        if self.important:
            str_to_print = "  [!]   "
        else:
            str_to_print = "  [_]   "
        str_to_print += str(self.essence) + "     " + str(self.id)
        return str_to_print


def print_current(all_tasks):
    print('Don\'t forget to:')
    for task in all_tasks:
        if task.active:
            print(task)
    return


def display_past(dump_file=dump_file):
    """print past tasks (completed and failed)"""

    [all_tasks, done_tasks, failed_tasks] = load_data(dump_file)

    print('Completed successfully:')
    for task in done_tasks:
        print(task)
    print('Failed to complete:')
    for task in failed_tasks:
        print(task)


def display_active(dump_file=dump_file):
    """prints active tasks (if present) on starting a shell (zsh/bash/...)"""

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
        print("memento data is invalid!")
        exit(1)


def add_task(new_task, important=False, data_file=dump_file):
    """instializes a new TaskItem instance and adds it to the data_file"""

    data = load_data(data_file)
    new_item = TaskItem(essence=new_task, important=important,
                        id=len(data[0])+1)
    data[0].append(new_item)
    save_data(data_file, *data)


def finish_task(target_id, failed, data_file=dump_file):
    """mark active task as done/failed"""

    data = load_data(data_file)
    for entry in data[0]:
        if entry.id == target_id:
            # prevent finishing a task multiple times
            if entry.active:
                entry.active = False
                if failed is False:
                    data[1].append(entry.essence)
                else:
                    data[2].append(entry.essence)
    save_data(data_file, *data)


if __name__ == "__main__":
    all_tasks = []
    done_tasks = []
    failed_tasks = []
    # parse arguments
    parser = argparse.ArgumentParser()
    parse_gr = parser.add_mutually_exclusive_group()
    parse_subgr = parse_gr.add_mutually_exclusive_group()
    parse_subgr.add_argument("-n", "--new", type=str, nargs="+",
                             help="add new task")
    parse_subgr.add_argument("-i", "--important", action="store_true",
                             help="mark new task as important")
    parse_gr.add_argument("-d", "--done", type=int,
                          help="mark task as done")
    parse_gr.add_argument("-f", "--failed", type=int,
                          help="mark task as failed")
    parse_pr = parser.add_mutually_exclusive_group()
    parse_pr.add_argument("-s", "--show", action="store_true",
                          help="display active tasks")
    parse_pr.add_argument("--hist", action="store_true",
                          help="display active tasks")
    args = parser.parse_args()

    if args.new:
        description = " ".join(args.new)
        add_task(description, args.important)
    elif args.done:
        print(args.done)
        finish_task(args.done, failed=False)
    elif args.failed:
        finish_task(args.done, failed=True)
    elif args.hist:
        display_past()
    else:
        display_active()
    sys.exit(0)
