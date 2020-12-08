for ((i=1; i <= 16; ++i))
do
    scrapy crawl -L INFO -s CONCURRENT_REQUESTS=$i -a n=100 -a ip=$1 geni
done
