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
 ----------------------
|myserver01
 ----------------------

top - 20:52:23 up 134 days, 15:53,  4 users,  load average: 24.34, 23.21, 22.86
Tasks: 3054 total,  26 running, 3028 sleeping,   0 stopped,   0 zombie
Cpu(s): 68.9%us,  9.1%sy,  0.0%ni, 16.7%id,  1.6%wa,  0.0%hi,  3.4%si,  0.2%st
Mem:  742619864k total, 647719048k used, 94900816k free,  1042588k buffers
Swap: 16777212k total,   255056k used, 16522156k free, 72276680k cached

Instance    System Stats                                     Rate (per second)
my1db0021   physical read total bytes                        1234M/Sec
my1db0021   logical read bytes from cache                    2213M/Sec
my1db0021   logical read bytes from cache                    2303M/Sec
my1db0021   logical read bytes from cache                    2481M/Sec
ncm10cpr1   logical read bytes from cache                    3822M/Sec

Instance    System Events                                    Rate (ms per second)
my1db0021   cell list of blocks physical read                1025K/Sec
my1db0021   resmgr:cpu quantum                               1611K/Sec
my1db0021   cell single block physical read                  2507K/Sec
my1db0021   cell list of blocks physical read                2518K/Sec
my1db0021   cell single block physical read                  3987K/Sec

   PID  USER         S  %CPU  %MEM      TIME+  COMMAND              INSTANCE    SQL_ID/CHILD     SID,SERIAL     QCSID  BLOCKER LAST_CALL   BLK_GTS   CON_GTS   PHY_RDS   BLK_CHG   CON_CHG  EVENT
245513  oracle       R  88.4   0.0   27:32.14  oraclencm10cpr1 (L   ncm10cpr1   7wbw114ckgadd/0  52,34118                           1719     2184K       56M      946K     3714K     2312K  CPU (Prev: resmgr:cpu quantum)
239707  oracle       R  83.9   0.2    1131:53  oraclemy1db0021 (L   my1db0021   6xr13yjmzspu0/0  470,56459                         79713      362K      891M       21M      4562      7336  CPU (Prev: resmgr:cpu quantum)
398624  oracle       R  78.0   0.0    3:17.38  oraclencm10cpr1 (L   ncm10cpr1   b2cv0gq12gs42/0  341,2636                            338       11M     2165K     1277K       11M     1024K  CPU (Prev: latch: cache buffers chains)
 21443  oracle       R  76.6   0.0    1:20.61  oraclemy1db0021 (L   my1db0021   d26kddnrwfzpk/0  1254,53436                          125      3934     2129K      505K      5875      4142  CPU (Prev: cell single block physical read)
180246  oracle       R  76.6   0.1    1063:32  oraclemy1db0021 (L   my1db0021   0pbzn3j9fnzdp/0  455,62530                         74675      156K      445M       14M      1899      1721  CPU (Prev: resmgr:cpu quantum)
349252  oracle       R  76.6   0.2   11:04.81  oraclemy1db0021 (L   my1db0021   2cfzca0kkbvbh/0  470,34103                           959     1633K       43M       29M     2470K     1809K  CPU (Prev: resmgr:cpu quantum)
 29826  oracle       R  73.6   0.0  119:27.66  oraclemy1db0021 (L   my1db0021   dp76nnpnk5x12/2  857,43792                          8520      2612      214M       37K      4979      2497  CPU (Prev: resmgr:cpu quantum)
 26041  oracle       R  66.3   0.0    0:06.72  oraclemy1db0021 (L   my1db0021   6zjpp3151vxds/   1187,31621                            4       14K     3502K     3414K       13K       322  SQL*Net message from client  (idle)
398596  oracle       R  61.8   0.0    3:23.61  oraclencm10cpr1 (L   ncm10cpr1   crk42uh5tqsww/0  900,46663                           354     6633K     2306K     1615K     7069K     1215K  CPU (Prev: gc current block 2-way)
 14626  oracle       R  53.0   0.0    0:51.32  oraclemy1db0021 (L   my1db0021   d6s8ckcvn1rj2/2  1235,36261                          185       30K     8995K      616K       48K       32K  cell list of blocks read request  (user i/o)
 27561  oracle       R  50.1   0.0    0:02.60  oraclemy1db0021 (L   my1db0021   d4626g6akh1p6/0  30,53579                              0      2675      765K      100K      4196      2612  SQL*Net message from client  (idle)
 35720  oracle       S  47.1   0.3  135:34.81  oraclemy1db0021 (L   my1db0021   96xk2j91hvb4m/3  843,7783                          31824     2865K     1934M       64M     4369K       41M  CPU (Prev: cell list of blocks physical read)
 27972  oracle       S  44.2   0.0    0:00.65  oraclemy1db0021 (L
366131  oracle       R  39.8   0.0    0:16.79  oraclencm10cpr1 (L   ncm10cpr1                    618,3601                              0        61     3831K      2716        29         1  SQL*Net message from client  (idle)
383484  oracle       R  35.3   0.0    2:28.24  oraclemy1db0021 (L
 28271  oracle       S  28.0   0.0    0:00.38  oraclemy1db0021 (L   my1db0021   0uj4d205y94jf/2  1210,40528                           12      1939      120K       65K      3301      1823  cell single block read request  (user i/o)
353818  oracle       S  26.5   0.0    3:31.56  oraclemy1db0021 (L   my1db0021   8w1n5vfkxzmfa/4  473,3595                              0      168K       42M     1514K      256K      176K  cell single block read request  (user i/o)
398093  oracle       S  26.5   0.0    1:59.06  oraclemy1db0021 (L   my1db0021   3m79ft28u33p6/2  604,57521                           395       60K       24M     1085K       95K       61K  CPU (Prev: cell list of blocks physical read)
 17218  oracle       S  25.0   0.0    0:59.66  oraclemy1db0021 (L   my1db0021   5u2v8ah38ymmy/27 424,14860                             3       60K       13M      415K       92K       62K  cell list of blocks read request  (user i/o)
 13554  oracle       S  23.6   0.0    0:53.70  oraclemy1db0021 (L   my1db0021   5u2v8ah38ymmy/14 1187,43962                            9       33K     6577K      635K       51K       34K  CPU (Prev: cell list of blocks physical read)
 28398  oracle       R  22.1   0.0    0:00.15  oraclemy1db0021 (L
394083  root         S  20.6   0.0  456:01.19  /u01/app/12.2.0.1/
399493  oracle       S  20.6   0.0    1:55.83  oraclemy1db0021 (L   my1db0021   8pqxc5jmfxmzb/2  616,14423                           372       47K       21M     1201K       72K       49K  cell single block read request  (user i/o)
 23371  oracle       S  19.1   0.0    0:10.91  oraclemy1db0021 (L

```




## Authors

* **John Tongelidis** - *Initial work* - [tongelja](https://github.com/tongelja)


