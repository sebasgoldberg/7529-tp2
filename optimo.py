#!/usr/bin/python
# coding=utf-8

class Optimo:

    def __init__(self, tramo, tiempo_total, optimoAnterior=None):
        self.tramo = tramo
        self.tiempo_total = tiempo_total
        self.optimoAnterior = None

    def __cmp__(self, other):
        if self.tramo.horario_llegada > other.tramo.horario_llegada:
            return 1
        if self.tramo.horario_llegada < other.tramo.horario_llegada:
            return -1
        return 0
