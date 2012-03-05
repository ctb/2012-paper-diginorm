#! /usr/bin/env python
import re, sys, urllib
import time

def retrieve_pubmed_cites(data):
    pattern = re.compile("pubmed(\d+)")
    return pattern.findall(data)

data = open(sys.argv[1]).read()
pmids = retrieve_pubmed_cites(data)

x = []
for z in pmids:
    if z in x:
        continue
    x.append(z)
pmids = x

search_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
search_args = dict(email="titus@caltech.edu",
                   db="pubmed",
                   retmax="150000",
                   usehistory="y")

search_terms = " ".join(pmids)
search_args['term'] = search_terms

r = urllib.urlopen(search_url, urllib.urlencode(search_args))
o = r.read()

def retrieve_values(name, data):
    pattern = re.compile("<%s>([^<]+)</%s>" % (name, name,))
    return pattern.findall(data)

def retrieve_value(name, data):
    v = retrieve_values(name, data)
    assert len(v) <= 1
    return v[0]

query_key = retrieve_value("QueryKey", o)
web_env = retrieve_value("WebEnv", o)

fetch_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

fetch_args = dict(email="titus@caltech.edu",
                  db="pubmed",
                  retmod="text",
                  rettype="medline",   # or medline
                  WebEnv=web_env,
                  query_key=query_key)

time.sleep(2)

r = urllib.urlopen(fetch_url, urllib.urlencode(fetch_args))
o = r.read()

def get_medline_fields(record, fieldname, max_ret=None):
    assert len(fieldname) <= 4

    fieldsearch = '%-4s-' % (fieldname.upper(),)
    cont = '     '

    results = []

    lines = record.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.find(fieldsearch) == 0:
            match = [line[6:].strip()]
            i += 1

            line = lines[i]
            while i < len(lines) and line.find(cont) == 0:
                match.append(line.strip())
                i += 1
                line = lines[i]

            results.append(" ".join(match))
        else:
            i += 1
        
    if max_ret:
        assert len(results) <= max_ret

    return results

def medline_to_bibtex(content):
    start = content.find('PMID- ')
    next = content.find('PMID- ', start + 1)

    bibrecs = []

    n = 1
    while start > -1:
        n += 1

        record = content[start:next]

        author_fields = get_medline_fields(record, 'AU')
        new_author_fields = []
        for author in author_fields:
            x = author.split()
            y = [x[-1], ]
            y.extend(x[:-1])
            author = " ".join(y)
            new_author_fields.append(author)

        authors = " and ".join(new_author_fields)
        pmid = get_medline_fields(record, 'PMID', 1)[0]
        title = get_medline_fields(record, 'TI', 1)[0]
        try:
            pages = get_medline_fields(record, 'PG', 1)[0]
        except:
            pages = ""
        journal_abbr = get_medline_fields(record, 'TA', 1)[0]
        year = get_medline_fields(record, "DP", 1)[0].split()[0]
        try:
            volume = get_medline_fields(record, 'VI', 1)[0]
        except:
            volume = ""
        try:
            issue = get_medline_fields(record, 'IP', 1)[0]
        except:
            issue = ""

        bibrecs.append("""\

@Article{pubmed%(pmid)s,
   author = "%(authors)s",
   title = "%(title)s",
   journal = "%(journal_abbr)s",
   year = "%(year)s",
   volume = "%(volume)s",
   number = "%(issue)s",
   pages = "%(pages)s"
}
""" % locals())
        
        start = next
        next = content.find('PMID- ', start + 1)

    return "".join(bibrecs)

print medline_to_bibtex(o)

