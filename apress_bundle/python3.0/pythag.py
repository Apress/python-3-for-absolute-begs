#! /usr/bin/env python

"""Work out the note values in Hz for a pythagorean scale"""

base_pitch = 432
a = base_pitch
a_1 = base_pitch * 2

def collect_args(b, e, a = 432, c = 512, *args, **kwargs):
     print((a, b, c, e))
     print(args)
     print(kwargs)

def calcsh5(pitch):
	pitch = pitch * 1.5
	if pitch > a_1:
		pitch = pitch / 2
	return int(pitch)

def calcsh4(pitch):
	pitch = pitch / 1.5
	if pitch < a:
		pitch = pitch * 2
	return int(pitch)

e = calcsh5(a)
b = calcsh5(e)
fsh = calcsh5(b)
csh = calcsh5(fsh)
gsh = calcsh5(csh)
d = calcsh4(a)
g = calcsh4(d)
c = calcsh4(g)
f = calcsh4(c)

collect_args(b, e, a, c, d, f, g, sharp1 = fsh, sharp2 = csh, sharp3 = gsh)

collect_args(486, 648, 432, 512, 576, 682, 768, first = 729, second = 546, third = 819)
