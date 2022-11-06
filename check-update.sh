#!/bin/sh
curl -s -L https://mariadb.org/download |grep "Latest releases" |sed -e 's,.*RC),,;s,</a>.*,,;s,.*>,,' 2>/dev/null
