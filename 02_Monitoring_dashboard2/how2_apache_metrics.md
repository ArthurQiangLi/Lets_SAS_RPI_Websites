# To monitor latency:

Modify the LogFormat directive in your apache2.conf file to include %D, which logs the request processing time in microseconds.

LogFormat "%h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\" %D" combined

