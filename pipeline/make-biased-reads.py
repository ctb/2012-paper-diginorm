#! /usr/bin/env python
import screed
import sys
import pygr.sequence
import random
import math

random.seed(1)                  # make this reproducible, please.

N_READS = int(1e6)
READLEN=100
ERROR_RATE=100


indices = []
seqs = []
powers = {}

index = 0
for r in screed.open(sys.argv[1]):
    power = int(r.description)
    count = int(math.pow(10, power))
    indices += [index] * count
    seqs.append(r.sequence)
    powers[index] = power

    index += 1

n_reads = N_READS
reads_mut = 0
total_mut = 0

z = []
for i in range(n_reads):
    index = random.choice(indices)
    sequence = seqs[index]

    start = random.randint(0, len(sequence) - READLEN)
    read = sequence[start:start + READLEN].upper()

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
    z.append(index)

y = []
for i in set(z):
    y.append((z.count(i), i))
y.sort()
print >>sys.stderr, y

print >>sys.stderr, "%d of %d reads mutated; %d total mutations" % \
    (reads_mut, n_reads, total_mut)
