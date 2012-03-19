#! /usr/bin/env python
import screed
import sys
import pygr.sequence
import random

random.seed(1)                  # make this reproducible, please.

COVERAGE=200
READLEN=100
ERROR_RATE=100

record = iter(screed.open(sys.argv[1])).next()
genome = record.sequence
len_genome = len(genome)

n_reads = int(len_genome*COVERAGE / float(READLEN))
reads_mut = 0
total_mut = 0

for i in range(n_reads):
    start = random.randint(0, len_genome - READLEN)
    read = genome[start:start + READLEN].upper()

    # reverse complement?
    if random.choice([0, 1]) == 0:
        read = str(-pygr.sequence.Sequence(read, ""))

    # error?
    was_mut = False
    for _ in range(READLEN):
        while random.randint(1, ERROR_RATE) == 1:
           pos = random.randint(1, READLEN) - 1
           read = read[:pos] + random.choice(['a', 'c', 'g', 't']) + read[pos+1:]
           was_mut = True
           total_mut += 1

    if was_mut:
        reads_mut += 1
    
    print '>read%d\n%s' % (i, read)

print >>sys.stderr, "%d of %d reads mutated; %d total mutations" % \
    (reads_mut, n_reads, total_mut)
