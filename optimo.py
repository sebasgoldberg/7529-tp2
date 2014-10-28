#!/usr/bin/python
# coding=utf-8

class Optimo:

    def __init__(self, horario_llegada, tramo, tiempo_total, optimoAnterior=None):
        self.horario_llegada = horario_llegada
        self.tramo = tramo
        self.tiempo_total = tiempo_total
        self.optimoAnterior = None

    def __cmp__(self, other):
        if self.horario_llegada > other.horario_llegada:
            return 1
        if self.horario_llegada < other.horario_llegada:
            return -1
        return 0
