#!/usr/bin/env python3

from .courses import *

def total_duration():
    return sum(course.duration for course in courses)