#!/usr/bin/python
# coding=utf-8

from tramo import Tramo

def normalizar_horario(x):
    x = x.replace(':','')
    return int(x[0:2])*60+int(x[2:4])

class Escenario:

    def __init__(self, f):

        self.ciudades = []
        self.id_por_ciudad = {}
        self.tramos_por_ciudad_destino = []

        cantidad_ciudades = int(f.readline().strip())
        for i in xrange(cantidad_ciudades):
            ciudad = f.readline().strip()
            self.id_por_ciudad[ciudad] = len(self.ciudades)
            self.ciudades.append(ciudad)
            self.tramos_por_ciudad_destino.append([])

        cantidad_trenes = int(f.readline().strip())
        for tren in xrange(cantidad_trenes):
            cantidad_ciudades_tren = int(f.readline().strip())
            horario_salida, ciudad_origen = f.readline().strip().split(' ', 1)
            horario_salida = normalizar_horario(horario_salida)
            ciudad_origen = self.id_por_ciudad[ciudad_origen]
            for i in xrange(cantidad_ciudades_tren-1):
                horario_llegada, ciudad_destino = f.readline().strip().split(' ', 1)
                horario_llegada = normalizar_horario(horario_llegada)
                ciudad_destino = self.id_por_ciudad[ciudad_destino]
                self.tramos_por_ciudad_destino[ciudad_destino].append(
                        Tramo(tren,ciudad_origen, ciudad_destino,
                            horario_salida, horario_llegada))
                horario_salida, ciudad_origen = horario_llegada, ciudad_destino

        self.horario_inicial = normalizar_horario(f.readline().strip())
        self.ciudad_origen = self.id_por_ciudad[f.readline().strip()]
        self.ciudad_destino = self.id_por_ciudad[f.readline().strip()]

    def get_id_ciudad(self, ciudad):
        return self.id_por_ciudad[ciudad]

    def get_tramos_a_ciudad(self, id_ciudad_destino):
        return self.tramos_por_ciudad_destino[id_ciudad_destino]

