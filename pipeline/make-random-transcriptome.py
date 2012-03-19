#! /usr/bin/env python
import random

random.seed(1)                  # make random transcriptome

N_TRANSCRIPTS=100
TRANSCRIPT_LENGTH=500
POWER_RANGE=3

def generate_transcript(length):
    x = ["A"] + ["G"] + ["C"] + ["T"]
    x = x*(length/4)

    random.shuffle(x)
    return "".join(x)

for i in range(N_TRANSCRIPTS):
    transcript = generate_transcript(TRANSCRIPT_LENGTH)
    power = random.choice(range(1, POWER_RANGE + 1))
    print '>%d %d\n%s' % (i, power, transcript)
