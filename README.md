# OraTop

OraTop is an interface that takes data from top and Oracle databases on a host.  The utility combines the data to OS data and session data.  It allows the viewer to see how multiple databases are interatcting with the host and identify high CPU consumers, memory consumers, and IO consumers.



## Getting Started

To get started, clone the repo:

```
https://github.com/tongelja/oratop.git
```



### Prerequisites

You will need to have cx_Oracle installed.


## Running OraTop


Run the oratop utility from the command line by giving it the hostname and the SYS passwords for the databases on the server.  I am assuming that the SYS database is the same across all databases.
 
```
python3 oratop.py --host myserver01 --db_password MyPassword
```

Your output will refresh every few seconds and look like this:

```
|myserver01
 ----------------------

top - 19:10:16 up 114 days,  1:27,  1 user,  load average: 9.95, 8.08, 6.49
Tasks: 4425 total,   6 running, 4419 sleeping,   0 stopped,   0 zombie
Cpu(s):  8.0%us,  4.1%sy,  0.2%ni, 86.9%id,  0.0%wa,  0.0%hi,  0.5%si,  0.3%st
Mem:  742619864k total, 671473940k used, 71145924k free,  1673708k buffers
Swap: 16777212k total,     6048k used, 16771164k free, 99278684k cached

Instance    System Stats                                     Rate (per second)
mydb0015   cell physical IO bytes eligible for predicate offload 106M/Sec
mydb0015   physical read bytes                              106M/Sec
mydb0015   cell IO uncompressed bytes                       106M/Sec
mydb0015   physical read total bytes optimized              106M/Sec
mydb0015   physical read total bytes                        106M/Sec

Instance    System Events                                    Rate (ms per second)
mydb0016   log file sync                                    255K/Sec
mydb0017   Data Guard server operation completion           269K/Sec
mydb0018   Data Guard server operation completion           275K/Sec
mydb0019   Data Guard server operation completion           491K/Sec
mydb0020   Data Guard server operation completion           1115K/Sec

   PID  USER         S  %CPU  %MEM      TIME+  COMMAND              INSTANCE    SQL_ID/CHILD     SID,SERIAL     QCSID  BLOCKER LAST_CALL   BLK_GTS   CON_GTS   PHY_RDS   BLK_CHG   CON_CHG  EVENT
 12319  grid         S  19.0   0.1    1824:15  /u01/app/12.2.0.1/
 72746  oracle       R  19.0   0.0    0:00.19  top -c -b -n 1
 47493  oracle       R  11.1   0.0   60:48.09  ora_pr08_mydb0020    mydb0020                    494,19920                       1142379         0         0     4253K         0         0  parallel recovery slave next change  (idle)
 47378  oracle       S   9.5   0.0   62:22.77  ora_pr02_mydb0020    mydb0020                    72,6040                         1142379         0         0     4210K         0         0  parallel recovery slave next change  (idle)
 47718  oracle       S   9.5   0.0   65:04.95  ora_pr0l_mydb0020    mydb0020                    1404,22314                      1142379         0         0     4050K         0         0  parallel recovery slave next change  (idle)
 47471  oracle       S   7.9   0.0   63:12.65  ora_pr07_mydb0020    mydb0020                    423,62823                       1142379         0         0     4367K         0         0  parallel recovery slave next change  (idle)
 19657  oracle       R   6.3   0.0  372:23.99  ora_lck0_mydb0020    mydb0020                    1263,24212                      1142588         0         0         0         0         0  rdbms ipc message  (idle)
 46397  oracle       S   6.3   0.0  667:48.18  ora_pr00_mydb0020    mydb0020                    1472,32080                      1142385         0         0      490K         0         0  CPU (Prev: log file sequential read)
 47549  oracle       S   6.3   0.0   67:40.02  ora_pr0b_mydb0020    mydb0020                    704,60706                       1142379         0         0     4272K         0         0  parallel recovery slave next change  (idle)
 47603  oracle       S   6.3   0.0   60:22.27  ora_pr0e_mydb0020    mydb0020                    915,31767                       1142379         0         0     4175K         0         0  parallel recovery slave next change  (idle)
177765  oracle       S   6.3   0.0    2:45.12  ora_dia0_mydb0021    mydb0021                    981,11128                         27935         0         0         0         0         0  DIAG idle wait  (idle)
 18335  oracle       S   4.7   0.0  257:33.09  ora_vktm_mydb0020    mydb0020                    281,8123                        1142595         0         0         0         0         0  VKTM Logical Idle Wait  (idle)
 18429  oracle       S   4.7   0.0  256:38.34  ora_vktm_mydb0018    mydb0018                    281,1515                        1142597         0         0         0         0         0  VKTM Logical Idle Wait  (idle)
 36440  oracle       S   4.7   0.0  748:06.79  ora_pr00_mydb0022    mydb0022                    983,52752                       1142510         0         0      240K         0         0  CPU (Prev: log file sequential read)
 51842  oracle       R   4.7   0.0  213:32.65  oraclemydb0020 (L    mydb0020                    74,42191                              0         0         0         0         0         0  SQL*Net vector message from client  (idle)
170266  oracle       S   4.7   0.0  226:38.27  ora_lck0_mydb0023    mydb0023                    18,5317                          443341         0         0         0         0         0  rdbms ipc message  (idle)
176775  oracle       S   4.7   0.0  327:37.01  ora_pr00_mydb0023    mydb0023                    33,24798                         443244         0         0      102K         0         0  enq: WL - contention  (other)
185023  oracle       S   4.7   0.0    9:39.61  ora_vktm_mydb0024    mydb0024                    2,29825                           42147         0         0         0         0         0  VKTM Logical Idle Wait  (idle)
```




## Authors

* **John Tongelidis** - *Initial work* - [tongelja](https://github.com/tongelja)


