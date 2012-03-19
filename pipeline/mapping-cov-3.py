import sys
from cPickle import dump
import screed

# arg 1 -- reference fasta
# arg 2 -- sam file
# arg 3 -- output pickled dict

refs = [ (r.name, len(r.sequence)) for r in screed.open(sys.argv[1]) ]
infp = open(sys.argv[2])
outfp = open(sys.argv[3], 'w')

refcov = {}
for name, length in refs:
   counts = [0]*length
   refcov[name] = counts

for n, line in enumerate(infp):
   if n % 10000 == 0:
      print '...', n

   _, orient, refname, pos, read = line.split()[:5]
   pos = int(pos)
   readlen = len(read)

   cov = refcov[refname]
   for i in range(readlen):
      cov[pos + i] += 1

counts_d = {}

for n, line in enumerate(open(sys.argv[2])):
   if n % 10000 == 0:
      print '...2', n

   rname, orient, refname, pos, read = line.split()[:5]
   pos = int(pos)
   readlen = len(read)

   cov = refcov[refname]
   counts = cov[pos:pos+i]

   avg = sum(counts) / float(len(counts))
   counts_d[rname] = avg

print len(counts_d)

dump(counts_d, outfp)
