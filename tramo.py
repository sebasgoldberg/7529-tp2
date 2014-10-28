#!/usr/bin/python
# coding=utf-8

class Tramo:

    def __init__(self, tren, ciudad_origen, ciudad_destino,
            horario_salida, horario_llegada):
        self.tren = tren
        self.ciudad_origen = ciudad_origen
        self.ciudad_destino = ciudad_destino
        self.horario_salida = horario_salida
        self.horario_llegada = horario_llegada

    def __str__(self):
        return '[Tren: %s] [Origen: %s] [Destino: %s] [Salida: %s] [Llegada: %s]' % (
                self.tren, self.ciudad_origen, self.ciudad_destino,
                self.horario_salida, self.horario_llegada)
