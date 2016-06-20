
from __future__ import division
import os, re
import cx_Oracle, getpass

def getOraHome(search='.*'):
    if os.path.isfile('/oracle/oratab'):
        oratab_file = '/oracle/oratab'
    elif os.path.isfile('/etc/oratab'):
        oratab_file = '/etc/oratab'
    else:
        print 'No oratab found.'
        sys.exit(2)

    oratab = os.popen("grep -v '^#'  " + oratab_file + "  | grep -v agent | grep -v cluster | grep -v grid | grep -v ASM ").readlines()
    homes = []
    for i in oratab:
        if re.search(search, i):
            homes.append(i.split(':', 3)[1])
    return homes[0]

def getLocalDbs(search='.*'):
    if os.path.isfile('/oracle/oratab'):
        oratab_file = '/oracle/oratab'
    elif os.path.isfile('/etc/oratab'):
        oratab_file = '/etc/oratab'
    else:
        print 'No oratab found.'
        sys.exit(2)

    oratab = os.popen("grep -v '^#'  " + oratab_file + " | grep -v agent | grep -v cluster | grep -v grid | grep -v ASM ").readlines()
    dbs = []
    for i in oratab:
        if re.search(search, i):
            dbs.append(i.split(':', 1)[0])
    return dbs

def createOraConnection(connect):
 
    if connect is None:
        try:
            conn = cx_Oracle.Connection(mode = cx_Oracle.SYSDBA)

        except:
            print 'Error connecting to database using connection string: ' + connect
            sys.exit(2)

    elif len(connect.split(':')) == 1:

        c = []
        c = connect.split(':')

        service      = c[0]

        try:
            os.environ['ORACLE_SID']      = service
            os.environ['ORACLE_HOME']     = getOraHome(service)
            os.environ['LD_LIBRARY_PATH'] = getOraHome(service) + '/lib:/lib'
            os.environ['PATH']            = getOraHome(service) + '/lib:' + getOraHome(service) + '/bin:' + os.environ['PATH']

            conn = cx_Oracle.Connection(mode=cx_Oracle.SYSDBA )
        except Exception as e:
            print 'Error connecting to database using connection string: ' + service + ' /  as sysdba'
            print e
            pass

    else:
        c = []
        c = connect.split(':')

        service      = c[0]
        hostname     = c[1]
        ##hostname     = c[1].replace('hq\.navteq\.com', '')
        try:
            user     = c[2]
        except:
            user     = 'sys'
        try:
            port     = c[4]
        except:
            port     = 1521
        try:
            password = c[3]
        except:
            print '\nEnter password for ' + user + '@' + hostname + ':' + str(port) + '/' + service
            password = getpass.getpass()


        dsn_tns = hostname + ':' + str(port) + '/' + service
        #dsn_tns = '(DESCRIPTION_LIST=' + cx_Oracle.makedsn(hostname, port, service).replace('SID','SERVICE_NAME') + \
        #                                 cx_Oracle.makedsn(hostname, port, service + '_' + hostname).replace('SID','SERVICE_NAME') + \
        #                                 cx_Oracle.makedsn(hostname, port, service) + \
        #                                 ')'

        if user != 'sys':
            try:
                ###                    connect = 'username/password@connection_string'
                conn = cx_Oracle.connect( user=user, password=password, dsn=dsn_tns )
            except Exception as e:
                print 'Error connecting to database using connection string: ' + connect + '  @' + dsn_tns
                print e
                pass

        else:
            try:
                ###                    connect = 'username/password@connection_string'
                conn = cx_Oracle.connect( user=user, password=password, dsn=dsn_tns, mode=cx_Oracle.SYSDBA )
            except Exception as e:
                print 'Error connecting to database using connection string: ' + connect + '  @' + dsn_tns
                print e
                pass

    return conn




def selectFoo(ora_connect):
    cursor = ora_connect.cursor()
    sql_stmt = "select instance_name from v$instance"
    cursor.execute(sql_stmt)
    rows = cursor.fetchall()
    print rows[0][0]


def format_number(n, unit=1000):
    if n == None:
        return ' '

    length = len(str(n))
    n = int(n)

    if length > 12:
        return "{0:.1f}".format(n/unit/unit/unit/unit) + 'T'
    elif length > 9:
        return "{0:.1f}".format(n/unit/unit/unit) + 'G'
    elif length > 6:
        return "{0:.1f}".format(n/unit/unit) + 'M'
    elif length > 3:
        return "{0:.1f}".format(n/unit) + 'K'
    else:
        return str(n)


