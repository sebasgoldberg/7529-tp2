#!/usr/bin/python
# coding=utf-8

from escenario import Escenario
import sys

class TP2:

    def __init__(self, filepath):
        self.escenarios = []
        with open(filepath) as f:
            cantidad_escenarios = int(f.readline().strip())
            for i in xrange(cantidad_escenarios):
                self.escenarios.append(Escenario(f))

    def resolver(self):
        for escenario in self.escenarios:
            escenario.resolver()

    def imprimir_solucion(self):
        for i in xrange(len(self.escenarios)):
            escenario = self.escenarios[i]
            print 'Escenario %s' % (i+1)
            escenario.imprimir_solucion()
            print


import unittest

class TP2TestCase(unittest.TestCase):

    def test_init(self):
        tp2 = TP2('ejemplo.txt')
        self.assertEqual(len(tp2.escenarios),2)
        escenario1 = tp2.escenarios[0]
        self.assertEqual(len(escenario1.ciudades),3)
        self.assertEqual(len(escenario1.get_tramos_a_ciudad(
            escenario1.get_id_ciudad('Jujuy'))),0)
        self.assertEqual(len(escenario1.get_tramos_a_ciudad(
            escenario1.get_id_ciudad('Tucumán'))),2)
        self.assertEqual(len(escenario1.get_tramos_a_ciudad(
            escenario1.get_id_ciudad('Buenos Aires'))),3)

        escenario2 = tp2.escenarios[1]
        self.assertEqual(len(escenario2.ciudades),2)
        self.assertEqual(len(escenario2.get_tramos_a_ciudad(
            escenario2.get_id_ciudad('Córdoba'))),0)
        self.assertEqual(len(escenario2.get_tramos_a_ciudad(
            escenario2.get_id_ciudad('La Plata'))),1)

    def test_resolucion_ejemplo(self):

        tp2 = TP2('ejemplo.txt')
        tp2.resolver()

        itinerarios = tp2.escenarios[0].get_itinerarios_optimos()
        itinerario = itinerarios[0]
        self.assertEqual(itinerario[0].hora, '1000')
        self.assertEqual(itinerario[0].ciudad, 'Jujuy')
        self.assertEqual(itinerario[1].hora, '1200')
        self.assertEqual(itinerario[1].ciudad, 'Tucumán')
        self.assertEqual(itinerario[2].hora, '1411')
        self.assertEqual(itinerario[2].ciudad, 'Buenos Aires')

        itinerarios = tp2.escenarios[1].get_itinerarios_optimos()
        self.assertEqual(itinerarios, [])


def reporte_tp2():
    for filepath in sys.argv[1:]:
        tp2 = TP2(filepath)
        tp2.resolver()
        tp2.imprimir_solucion()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        unittest.main()
    else:
        reporte_tp2()


