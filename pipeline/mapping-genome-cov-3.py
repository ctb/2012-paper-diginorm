import sys
import screed
import gzip

# arg 1 -- sequence file
# arg 2 -- bowtie map file
# arg 3 -- output dist file

refs = [ (r.name, len(r.sequence)) for r in screed.open(sys.argv[1]) ]

if sys.argv[2].endswith('.gz'):
   infp = gzip.open(sys.argv[2])
else:
   infp = open(sys.argv[2])
outfp = open(sys.argv[3], 'w')

refcov = {}
for name, length in refs:
   counts = [0]*length
   refcov[name] = counts

for n, line in enumerate(infp):
   if n % 10000 == 0:
      print '...', n
   _, orient, refname, pos, read = line.split('\t')[:5]
   pos = int(pos)
   readlen = len(read)

   cov = refcov[refname]
   for i in range(readlen):
      cov[pos + i] += 1

dist = {}
for name in refcov:
   for count in refcov[name]:
      dist[count] = dist.get(count, 0) + 1

for i in range(0, max(dist.keys()) + 1):
   print >>outfp, i, dist.get(i, 0)


totalcov = 0
totalsize = 0
for k in refcov:
   totalcov += sum(refcov[k])
   totalsize += len(refcov[k])

print 'average coverage:', totalcov / float(totalsize)

print 'done', sys.argv[1:]
