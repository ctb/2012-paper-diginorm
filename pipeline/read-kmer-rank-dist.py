#! /usr/bin/env python
import sys
import screed
import khmer

print 'loading counting hash', sys.argv[1]
kh = khmer.load_counting_hash(sys.argv[1])
K = kh.ksize()

for record in screed.open(sys.argv[2]):
    readname = record.name
    seq = record.sequence

    outfp = open(readname + '.ranks', 'w')

    x = []
    for i in range(len(seq) - K + 1):
        kmer = seq[i:i+K]
        x.append(kh.get(kmer))

    x.sort()

    for i in range(len(seq) - K + 1):
        print >>outfp, i, x[i]
