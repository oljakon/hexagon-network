import sys
import os
import pyglet

d = os.path.dirname(__file__)
folder = os.path.join(d, '../resources')

pyglet.resource.path = [folder]
pyglet.resource.reindex()


from game import chart
from game import city
from game import army
from game import menu
from game import session
