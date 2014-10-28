#!/usr/bin/python
# coding=utf-8

from datetime import time


def normalizar_horario(x):
    x = x.replace(':','')
    return int(x[0:2])*60+int(x[2:4])


def format_horario(x):
    return time(x/60,x % 60).isoformat().replace(':','')[0:4]
