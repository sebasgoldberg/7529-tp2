#!/usr/bin/python
# coding=utf-8

from escenario import Escenario

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


if __name__ == '__main__':
    unittest.main()
