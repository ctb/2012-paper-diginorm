import numpy, math, itertools

LIMIT=10000

def load_cmp_file(filename):
    x = numpy.loadtxt(filename)
    print 'loaded %d lines from %s ' % (len(x), filename)
    return x

def f():
    lines = [ line.split() for (line, _) in itertools.izip(open(filename), range(LIMIT)) ]
    lines = [ (float(a[0]), float(a[1])) for a in lines ]

    print 'loaded %d lines from %s ' % (len(lines), filename)
    return numpy.array(lines)

def filter_kmer_counts(counts, max_count):
    counts = [ (a,b) for (a,b) in counts if b < max_count ]
    return numpy.array(counts)

def log_kmer_counts(counts):
    counts = numpy.array([ (math.log(a), math.log(b)) for (a,b) in counts \
                              if a and b ])
    return counts

if 1:
    counts = load_cmp_file('genome-reads.fa.counts.cmp')
    c = numpy.corrcoef(counts[:,0], counts[:,1])[0,1]
    print 'simulated genome r^2', c**2
    print ''

if 1:
    counts = load_cmp_file('ecoli_ref-5m.fastq.counts.cmp')
    c = numpy.corrcoef(counts[:,0], counts[:,1])[0,1]
    print 'E. coli genome r^2', c**2

    counts = filter_kmer_counts(counts, 8000)
    c = numpy.corrcoef(counts[:,0], counts[:,1])[0,1]
    print 'FILTERED E. coli genome r^2', c**2
    print ''

###

if 1:
    counts = load_cmp_file('transcript-reads.fa.counts.cmp')
    c = numpy.corrcoef(counts[:,0], counts[:,1])[0,1]
    print 'simulated transcriptome r^2', c**2

    log_counts = log_kmer_counts(counts)
    c = numpy.corrcoef(log_counts[:,0], log_counts[:,1])[0,1]
    print 'LOG simulated transcriptome r^2', c**2

    print ''


if 1:
    counts = load_cmp_file('mouse-5m.fq.counts.cmp')
    c = numpy.corrcoef(counts[:,0], counts[:,1])[0,1]
    print 'mouse transcriptome r^2', c**2

    counts = filter_kmer_counts(counts, 20000)
    c = numpy.corrcoef(counts[:,0], counts[:,1])[0,1]
    print 'FILTERED mouse transcriptome r^2', c**2

    log_counts = log_kmer_counts(counts)
    c = numpy.corrcoef(log_counts[:,0], log_counts[:,1])[0,1]
    print 'LOG / FILTERED mouse transcriptome r^2', c**2

    print ''

