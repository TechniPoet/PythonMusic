#!/usr/bin/python

import pysynth
from pysynth_b import *
import Theory

class Generator:
	def __init__(self, seed):
		self.seed = seed;
		self.seedNote = "E"
		self.scale = makeScale(seedNote, true)

gen = Generator(123)
print gen.seed
print gen.seedNote
print gen.scale