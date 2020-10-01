# -*- encoding: utf-8 -*-

import unittest
import sys
import os

d = os.path.dirname(__file__) 
filedir = os.path.join(d, '../')
os.chdir(filedir)
sys.path.append(os.getcwd())
sys.path.insert(0, filedir)

from game import *

class TestUnit1(unittest.TestCase):
    def setUp(self):
        self.A = army.Unit(1, 1, [0,0,0])
        self.B = army.Unit(6, 2, [0,0,0])
        self.C = army.Unit(0, 2, [0,0,0])

    def test_init(self):
        self.assertEqual((self.A.type_unit, self.A.count),(1, 1),"Неверная инициализация объекта Unit(1,1)")
        self.assertEqual((self.B.type_unit, self.B.count),(2, 6),"Неверная инициализация объекта Unit(6, 2)")
        self.assertEqual((self.C.type_unit, self.C.count),(2, 0),"Неверная инициализация объекта Unit(0, 2)")

if __name__ == '__main__':
    unittest.main()

