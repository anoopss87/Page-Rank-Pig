crawl = load 'data/webcrawl' as (url:chararray, num:double, pageid:bag{t:(p:chararray)});

id = foreach crawl generate url, flatten(pageid) as pid;

id_f1 = filter id by pid is not null;
id_f2 = filter id_f1 by (pid matches '.*http.*');
byurl = group id_f2 by url;
burl = foreach byurl {
	uniq_pid = DISTINCT id_f2.pid;	
	generate group, uniq_pid;
};
out = foreach burl generate group, 1.0 as double, uniq_pid.pid;
store out into 'pr_input';