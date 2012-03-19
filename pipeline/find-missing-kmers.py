#! /usr/bin/env python
import sys
import screed
import khmer

print 'loading'
kh = khmer.load_counting_hash(sys.argv[1])
K = kh.ksize()
print 'done - K is', K

outfp = open(sys.argv[3], 'w')

poslist = [0]*200000
poscount = [0]*200000

for n, record in enumerate(screed.open(sys.argv[2])):
    if n % 100 == 0:
        print '...', n
    seq = record.sequence
    seqlen = len(record.sequence) - K + 1

    for pos in range(len(seq) - K + 1):
        kmer = seq[pos:pos+K]
        cnt = kh.get(kmer)

        if pos > seqlen / 2:
            pos = seqlen - pos - 1

        poscount[pos] += 1
        if not kh.get(kmer):
            poslist[pos] += 1

for pos, (count, total) in enumerate(zip(poslist, poscount)):
    frac = 0.
    if total:
        frac = float(count) / float(total)
    print >>outfp, pos, count, frac, total
