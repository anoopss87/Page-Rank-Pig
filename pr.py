# pagerank.py
from org.apache.pig.scripting import *
P = Pig.compile("""
previous_pagerank = load '$docs_in' as (url:chararray, pagerank:float,
                      links:{link:(url:chararray)});
outbound_pagerank = foreach previous_pagerank generate
                      pagerank / COUNT(links) as pagerank,
                      flatten(links) as to_url;
cogrpd            = cogroup outbound_pagerank by to_url,
                      previous_pagerank by url;
new_pagerank      = foreach cogrpd generate group as url,
                      (1 - $d) + $d * SUM (outbound_pagerank.pagerank)
                      as pagerank,
                      flatten(previous_pagerank.links) as links,
                      flatten(previous_pagerank.pagerank) AS previous_pagerank;
store new_pagerank into '$docs_out';
nonulls           = filter new_pagerank by previous_pagerank is not null and
                        pagerank is not null;
pagerank_diff     = foreach nonulls generate ABS (previous_pagerank - pagerank);
grpall            = group pagerank_diff all;
max_diff          = foreach grpall generate MAX (pagerank_diff);
store max_diff into '$max_diff';
""")

d = 0.5
docs_in = 'pr_input/part-r-00000'

for i in range(10):
    docs_out = "pagerank_data_" + str(i + 1)
    max_diff = "max_diff_" + str(i + 1)
    Pig.fs("rmr " + docs_out)
    Pig.fs("rmr " + max_diff)
    bound = P.bind()
    stats = bound.runSingle()
    if not stats.isSuccessful():
        raise 'failed'
    mdv = float(str(stats.result("max_diff").iterator().next().get(0)))
    print "max_diff_value = " + str(mdv)
    if mdv < 0.01:
        print "done at iteration " + str(i)
        break
    docs_in = docs_out