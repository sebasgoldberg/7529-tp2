#!/usr/bin/python
# coding=utf-8

from tramo import Tramo
from lista_ordenada import ListaOrdenada, ElementoNoEncontrado
from optimo import Optimo
from horario import *

class OptimoNoEncontrado(Exception):
    pass


class ItemItinerario:

    def __init__(self, hora, ciudad):
        """
        O(1)
        """
        self.hora = hora
        self.ciudad = ciudad

class ItemListadoCiudades:

    def __init__(self, nombre, id):
        """
        O(1)
        """
        self.nombre = nombre
        self.id = id

    def __cmp__(self, other):
        """
        O(1)
        """
        if self.nombre < other.nombre:
            return -1
        if self.nombre > other.nombre:
            return 1
        return 0

class Escenario:

    def __init__(self, f):
        """
        O(max(n,m+r)*log(n))
        n: Cantidad de ciudades
        m: Cantidad de trenes
        ri: Cantidad de ciudades que visita el tren i
        r: Cantidad de ciudades visitadas por los m trenes
        """

        self.ciudades = [] # O(1)
        self.id_por_ciudad = ListaOrdenada() # O(1)
        self.tramos_por_ciudad_destino = [] # O(1)

        cantidad_ciudades = int(f.readline().strip()) # O(1)
        # O(n*log(n))
        for i in xrange(cantidad_ciudades): # n
            ciudad = f.readline().strip() # O(1)
            self.id_por_ciudad.insert(ItemListadoCiudades(ciudad, len(self.ciudades))) # O(log(n))
            self.ciudades.append(ciudad) # O(1)
            self.tramos_por_ciudad_destino.append([]) # O(1)

        cantidad_trenes = int(f.readline().strip()) # O(1)

        # O(m*log(n) + sum(ri*log(n))) = O(m*log(n)+r*log(n)) = O((m+r)*log(n))
        for tren in xrange(cantidad_trenes): # m
            cantidad_ciudades_tren = int(f.readline().strip()) # O(1)
            horario_salida, ciudad_origen = f.readline().strip().split(' ', 1) # O(1)
            horario_salida = normalizar_horario(horario_salida) # O(1)
            ciudad_origen = self.get_id_ciudad(ciudad_origen) # O(log(n))
            for i in xrange(cantidad_ciudades_tren-1): # ri
                horario_llegada, ciudad_destino = f.readline().strip().split(' ', 1) # O(1)
                horario_llegada = normalizar_horario(horario_llegada) # O(1)
                ciudad_destino = self.get_id_ciudad(ciudad_destino) # O(log(n))
                self.tramos_por_ciudad_destino[ciudad_destino].append(
                        Tramo(tren,ciudad_origen, ciudad_destino,
                            horario_salida, horario_llegada)) # O(1)
                horario_salida, ciudad_origen = horario_llegada, ciudad_destino # O(1)

        self.horario_inicial = normalizar_horario(f.readline().strip()) # O(1)
        self.ciudad_origen = self.get_id_ciudad(f.readline().strip()) # O(log(n))
        self.ciudad_destino = self.get_id_ciudad(f.readline().strip()) # O(log(n))

    def get_id_ciudad(self, ciudad):
        """
        O(log(n))
        """
        return self.id_por_ciudad.get_item(ItemListadoCiudades(ciudad,None)).id

    def get_tramos_a_ciudad(self, id_ciudad_destino):
        """
        O(1)
        """
        return self.tramos_por_ciudad_destino[id_ciudad_destino]

    def resolver(self):
        """
        O(max(n*p*log(p) + p**2, n**2))
        self.solucion es una matriz donde la primer componente es la cantidad
        máxima de tramos necesarios para llegar a una ciudad, la segunda
        componente es la ciudad destino, y la tercera es la solucion optima
        para un determinado horario de llegada.
        """

        self.solucion = [] # O(1)

        # O(n**2)
        for k in xrange(len(self.ciudades)): # n
            self.solucion.append([]) # O(1)
            for ciudad in xrange(len(self.ciudades)): # n
                self.solucion[k].append(ListaOrdenada()) # O(1)

        # O(1)
        self.solucion[0][self.ciudad_origen].insert(Optimo(
            self.horario_inicial, Tramo(None, self.ciudad_origen,
                self.ciudad_origen, self.horario_inicial,
                self.horario_inicial), 0))


        # O(sum(p*log(p)) + sum(pj*p)) = O(n*p*log(p) + p**2)
        for k in xrange(1,len(self.ciudades)): # n-1
            # O(sum(pj*log(pj)) + sum(sum(pi))) = O(p*log(p)+ pj*p)
            for ciudad in xrange(len(self.ciudades)): # n
                # O(pj*(log(pj) + sum(log(pi))), donde pi son los tramos que llegan a cada ciudad i que llega a j.
                for tramo in self.get_tramos_a_ciudad(ciudad): # pj (los tramos que llegan a la ciudad j)
                    try:
                        """
                        O(log(si)) (si cantidad de soluciones para la ciudad i en k-1 tramos,
                        si <= pi ya que habra como máximo tantas soluciones hacia i como tramos
                        lleguen a i (ver insert más abajo))
                        Se obtiene la solucion más cercana al horario de salida desde la
                        ciudad origen a la destino en k-1 tramos.
                        """
                        optimoAnterior = self.solucion[k-1][tramo.ciudad_origen].get_anterior_mas_cercano(
                                Optimo(tramo.horario_salida, None, None)) 
                    except ElementoNoEncontrado:
                        continue
                    tiempo_total = optimoAnterior.tiempo_total + (tramo.horario_llegada - 
                            optimoAnterior.tramo.horario_llegada) # O(1)
                    self.solucion[k][ciudad].insert(
                            Optimo(tramo.horario_llegada,
                                tramo, tiempo_total, optimoAnterior)) # O(log(sj)) = O(log(pj))

        self.optimos = [] # O(1)
        tiempo_total_optimo = None # O(1)
        # O(sum(pj)) = O(p)
        for k in xrange(len(self.ciudades)): # n
            for solucion in self.solucion[k][self.ciudad_destino].iteritems(): # sj = pj
                if tiempo_total_optimo is None: # O(1)
                    self.optimos = [solucion] # O(1)
                    tiempo_total_optimo = solucion.tiempo_total # O(1)
                elif solucion.tiempo_total == tiempo_total_optimo: # O(1)
                    self.optimos.append(solucion) # O(1)
                elif solucion.tiempo_total < tiempo_total_optimo: # O(1)
                    self.optimos = [solucion] # O(1)
                    tiempo_total_optimo = solucion.tiempo_total # O(1)

    def get_itinerarios_optimos(self):
        """
        O(p*n)
        """
        itinerarios = [] # O(1)
        if len(self.optimos) == 0: # O(1)
            return itinerarios # O(1)
        # O(p*n)
        for optimo in self.optimos: # p
            itinerario = [] # O(1)
            solucion = [] # O(1)
            while optimo.optimoAnterior is not None: # n
                solucion.insert(0,optimo) # O(1)
                optimo = optimo.optimoAnterior # O(1)
            itinerario.append(ItemItinerario(
                    format_horario(solucion[0].tramo.horario_salida),
                    self.ciudades[solucion[0].tramo.ciudad_origen])) # O(1)
            for optimo in solucion[:-1]: # n
                itinerario.append(ItemItinerario(
                        format_horario(optimo.tramo.horario_llegada),
                        self.ciudades[optimo.tramo.ciudad_destino])) # O(1)
            itinerario.append(ItemItinerario(
                    format_horario(solucion[-1].tramo.horario_llegada),
                    self.ciudades[solucion[-1].tramo.ciudad_destino])) # O(1)
            itinerarios.append(itinerario) # O(1)
        return itinerarios # O(1)


    def imprimir_solucion(self):
        """
        O(p*n)
        """
        itinerarios = self.get_itinerarios_optimos() # O(p*n)
        if len(itinerarios) == 0:
            print 'Sin combinaciones posibles'
            return
        for itinerario in itinerarios:
            print 'Salida %s %s' % (
                    itinerario[0].hora, itinerario[0].ciudad)
            for item in itinerario[1:-1]:
                print 'Trasbordo %s %s' % (
                    item.hora, item.ciudad)
            print 'Arribo %s %s' % (
                    itinerario[-1].hora, itinerario[-1].ciudad)
