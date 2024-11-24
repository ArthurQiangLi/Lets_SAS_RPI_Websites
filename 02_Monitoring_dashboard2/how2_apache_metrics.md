# To monitor apache:

'fetch_apache_metrics' method scrapes the apache metrics

Apache already serves the localhost/server-status so I don't think there was anything extra happening here

# To monitor latency

Modify the LogFormat directive in your apache2.conf file to include %D, which logs the request processing time in microseconds.

LogFormat "%h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\" %D" combined