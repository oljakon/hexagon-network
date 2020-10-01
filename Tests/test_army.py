# -*- encoding: utf-8 -*-

'''
Протестированы 2 метода: __init__, merge
'''

import unittest
import sys
import os
import cocos
from cocos.director import director

d = os.path.dirname(__file__) 
filedir = os.path.join(d, '../')
os.chdir(filedir)
sys.path.append(os.getcwd())
sys.path.insert(0, filedir)


from hexagon import *

class TestUnit1(unittest.TestCase):
    def setUp(self):
        window_w, window_h = 1300, 800
        cocos.director.director.init(width=window_w, height=window_h)
        game_session = session.Session(4, ["Player 1","Player 2","Player 3","Player 4"])

        self.A_Unit = army.Unit(6, 1,[0,0,0])
        self.A = army.Army(self.A_Unit, 0, 0)

        self.B_Unit1 = army.Unit(1,2,[0,0,0])
        self.B_Unit2 = army.Unit(4,2,[0,0,0])
        self.B = army.Army(self.B_Unit1,0, 0)
        self.B.merge_unit(self.B_Unit2)

        self.C_Unit1 = army.Unit(1,1,[0,0,0])
        self.C_Unit2 = army.Unit(4,2,[0,0,0])
        self.C_Unit3 = army.Unit(6,3,[0,0,0])
        self.C = army.Army(self.C_Unit1,0,0)
        self.C.merge_unit(self.C_Unit2)
        self.C.merge_unit(self.C_Unit3)

        
    def test_init(self):
        self.assertEqual((self.A.army[0],self.A.type_army_global),(self.A_Unit,self.A_Unit.type_unit),"Wrong army initialization")

    def test_merge(self):
        self.assertEqual(len(self.B.army),1,"Wrong merge. Wrong length of army array")
        self.assertEqual(self.B.type_army_global,self.B_Unit1.type_unit,"Wrong merge. Wrong type of army")
        self.assertEqual(len(self.C.army),3,"Wrong merge. Wrong length of army array")
        self.assertEqual(self.C.type_army_global,self.C_Unit3.type_unit,"Wrong merge. Wrong type of army")                   
    

if __name__ == '__main__':
    unittest.main()
