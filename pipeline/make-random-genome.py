#! /usr/bin/env python
import random

random.seed(1)                  # make reproducible

x = ["A"] + ["G"] + ["C"] + ["T"]
x = x*100000

random.shuffle(x)
print '>genome\n%s\n' % "".join(x)
