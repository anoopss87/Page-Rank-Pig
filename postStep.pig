A = LOAD 'pagerank_data_5/part-r-00000' AS ( url: chararray, pagerank: float, links:{ link: ( url: chararray ) } );
B = filter A by pagerank is not null;
C = foreach B generate url, pagerank;
store C into 'Q7';