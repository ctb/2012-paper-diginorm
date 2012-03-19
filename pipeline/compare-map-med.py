import sys
from cPickle import load

print>>sys.stderr, 'loading map counts...'
map_counts = load(open(sys.argv[1]))

print>>sys.stderr, 'loading kh counts...'
med_counts = dict([ x.split()[:2] for x in open(sys.argv[2]) ])

for k in map_counts:
    try:
        c1 = map_counts[k]
        c2 = int(med_counts[k])
        print c1, c2
    except KeyError:
        pass
