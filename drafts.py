#!/usr/bin/python

# Packages {{{ }}}
# Define params {{{ }}}


all_tasks = []     # TODO
done_tasks = []    # TODO
failed_tasks = []  # TODO


def new_id():
    ...
    # TODO (current time, maybe?)


class TaskItem:

    def __init__(self, task, important=False):
        self.active = True
        self.id = new_id()
        self.task = task
        if important:
            self.important = True
        else:
            self.important = False

    def cross_off(self, completed=True):
        self.active = False
        if completed:
            self.important = True
        else:
            self.important = False

