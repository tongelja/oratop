#!/bin/python

#/tools/python/virtual/dba/bin/python

##########################
##
##
##
##
##################################


###########################
##
## Import
###
#####################################

import os, re, sys, getopt, operator, time, cx_Oracle, binascii, platform, getpass
sys.path.append(os.path.abspath('bin'))
import orautility


##############################
##
## Functions
##
#######################################

##
## usage
##
def usageExit(message):
    print message
    print "Usage:"
    print os.path.abspath( __file__ ),  '-p <PASSWORD> -d <DB> -u <USER> [ -l <LINES> ] \n '

    sys.exit(2)



def format_number(n, unit=1000):
    if n == None:
        return '0'

    if n == ' ':
        return ' '

    n = int(n)

    length = len(str(n))

    if length > 13:
        return str(n/unit/unit/unit/unit) + 'P'
    elif length > 10:
        return str(n/unit/unit/unit) + 'G'
    elif length > 7:
        return str(n/unit/unit) + 'M'
    elif length > 4:
        return str(n/unit) + 'K'
    else:
        return str(n)


def getTerminalSize():
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (env['LINES'], env['COLUMNS'])
        except:
            cr = (25, 80)
    return int(cr[1]), int(cr[0])


def printLabel():
    print '\n--------------'
    print 'top + Oracle = OraTop'
    print '---------------------'



def printOraTop(top_data, session_data, system_stat, system_event, top_label, top_sum, lines):
    #top_format = '%8s %-8s %3s %3s %8s %-8s %-8s %3s %-8s %-8s %-12s %-30s %-18s %-10s %10s %10s %10s %10s %10s' 
    top_format = '%6s  %-10s %3s %5s %5s %10s  %-26s %-16s %-10s  %8s %8s %9s %9s %9s %9s %9s %9s  %-50s' 
    sys_format = '%-50s %-20s'

    printLabel()

    print
    for i in top_sum:
        print  i.replace('\n', '')


    sorted_system_stat  = sorted(system_stat.iteritems(), key=operator.itemgetter(1))
    sorted_system_event = sorted(system_event.iteritems(), key=operator.itemgetter(1))


    if len(sorted_system_stat)-5 < 0:
        sys_start=0
    else:
        sys_start = len(sorted_system_stat)-5

    sys_stop = len(sorted_system_stat)
    for i in range(sys_start, sys_stop):
        if i == sys_start:
            print
            print sys_format % ( 'DB        System Stats', 'Value Delta' ) 
        print sys_format %  sorted_system_stat[i]


    if len(sorted_system_event)-5 < 0:
        sys_start=0
    else:
        sys_start = len(sorted_system_event)-5

    sys_stop = len(sorted_system_event)
    for i in range(sys_start, sys_stop):
        if i == sys_start:
            print
            print sys_format % ( 'DB        System Events', 'Waited Delta' )
        print sys_format %  sorted_system_event[i]

    print 
    for i in top_label:
        print top_format %  ( i )

    ##lines=len(top_data)

    for i in range(0, lines):

        if len(top_data[i]) > 0:
            try:
                sql_id       = session_data[top_data[i][0]]['sql_id']
                sid          = session_data[top_data[i][0]]['sid']
                blk_gts      = session_data[top_data[i][0]]['block_gets']
                con_gts      = session_data[top_data[i][0]]['cons_gets']
                phy_rds      = session_data[top_data[i][0]]['phy_reads']
                blk_chg      = session_data[top_data[i][0]]['block_chgs']
                con_chg      = session_data[top_data[i][0]]['cons_chgs']
                event        = session_data[top_data[i][0]]['event']
                lst_call     = session_data[top_data[i][0]]['last_call_et']
                qcsid        = session_data[top_data[i][0]]['qcsid']
                blocker      = session_data[top_data[i][0]]['blocker']
            except:
                sql_id       = ' '
                sid          = ' ' 
                blk_gts      = ' '
                con_gts      = ' '
                phy_rds      = ' '
                blk_chg      = ' '
                con_chg      = ' '
                event        = ' '
                lst_call     = ' '
                qcsid        = ' '
                blocker      = ' '

            print top_format % ( top_data[i][0],  top_data[i][1], \
                                 top_data[i][7],  top_data[i][8], \
                                 top_data[i][9],  top_data[i][10],\
                                 str(' '.join(top_data[i][11:]))[:25], \
                                 sql_id,          sid,            \
                                 qcsid,           blocker, \
                                 lst_call,        \
                                 format_number( blk_gts, 1024 ),         \
                                 format_number( con_gts, 1024 ),         \
                                 format_number( phy_rds, 1024 ),         \
                                 format_number( blk_chg, 1024 ),         \
                                 format_number( con_chg, 1024 ),         \
                                 event[:45] 
                               ) 
        

def getTopLabels():
    top_cmd = " top -b -n 1| grep PID"
    top_std_out = os.popen(top_cmd).readlines()[0].split()
    top_std_out.remove('PR')
    top_std_out.remove('NI')
    top_std_out.remove('VIRT')
    top_std_out.remove('RES')
    top_std_out.remove('SHR')
    top_std_out.append('SQL_ID/CHILD')
    top_std_out.append('SID,SERIAL')
    top_std_out.append('QCSID')
    top_std_out.append('BLOCKER')
    top_std_out.append('LAST_CALL')
    top_std_out.append('BLK_GTS')
    top_std_out.append('CON_GTS')
    top_std_out.append('PHY_RDS')
    top_std_out.append('BLK_CHG')
    top_std_out.append('CON_CHG')
    top_std_out.append('EVENT')

    r  = []

    r.append(tuple(top_std_out))

    return r


def getTopSummary():
    #top_cmd = " top -b -n 1| head -5 "
    top_cmd = " top -b -n 2 | grep -v '^ *[0-9]' | grep -v PID | sed '/^$/d' | tail -5 "
    top_std_out = os.popen(top_cmd).readlines()
    r  = []
    r.append(tuple(top_std_out))
    return top_std_out


def getTopData(db_search):
    if db_search == '.*':
        #top_cmd="top -c -b -n 1 -u oracle | grep -v '^[a-Z]' 2>/dev/null | grep -v PID  2>/dev/null    | sort  -k 8,9 2>/dev/null  | head -40"
        top_cmd="top -c -b -n 1 -u oracle | grep -v '^[a-Z]' 2>/dev/null | grep -v PID  2>/dev/null    | head -100"
    else:
        top_cmd="top -c -b -n 1 -u oracle | grep -v '^[a-Z]' 2>/dev/null | grep -v PID 2>/dev/null | grep " + db_search + " 2>/dev/null  | head -100"
        #top_cmd="top -c -b -n 1 -u oracle | grep oracle 2>/dev/null | sort   -k 8,9 2>/dev/null | grep " + db_search + " 2>/dev/null  | head -40"

    top_std_out = os.popen(top_cmd).readlines()
    top_output = []
    for i in range(0, len(top_std_out)):
        top_output.append([])
        top_output[i] = top_std_out[i].split()
    
    return top_output


def getSessionData(db_connection):
    cursor = db_connection.cursor()
    ###io.block_gets, io.consistent_gets, io.physical_reads, io.block_changes, io.consistent_changes, s.event, s.last_call_et, nvl(to_char(px.qcsid), ' '), nvl(to_char(s.blocking_session), ' ') \
    sql_stmt = "select p.spid, decode(s.sql_id, null, '', s.sql_id || '/' || s.sql_child_number), s.username, decode(s.sid, null, '', s.sid || ',' ||  s.serial#), \
                io.block_gets, io.consistent_gets, io.physical_reads, io.block_changes, io.consistent_changes,  \
                case when s.state != 'WAITING' \
                    then 'CPU (Prev: ' || case when length(s.event) > 45 then  rpad(s.event, 45, ' ') || '...)' else s.event || ')' end \
                    else  rpad(s.event || '  (' || lower(s.wait_class) || ')' , 47, ' ') || case when length(s.event || s.wait_class ) > 45 then '...' else NULL end end as event, \
                s.last_call_et, nvl(to_char(px.qcsid), ' '), nvl(to_char(s.blocking_session), ' ') \
                from v$session s, v$process p, v$sess_io io, v$px_session px \
                where s.sid = px.sid(+) and s.sid = io.sid and s.paddr = p.addr  and s.sql_id is not null"
    cursor.execute(sql_stmt)
    rows = cursor.fetchall()
  
    out = {}
    for i in range(0, len(rows)):
        out[rows[i][0]] = {}
        out[rows[i][0]]['sql_id']       = str(rows[i][1]) 
        out[rows[i][0]]['username']     = str(rows[i][2]) 
        out[rows[i][0]]['sid']          = str(rows[i][3]) 
        out[rows[i][0]]['block_gets']   = str(rows[i][4]) 
        out[rows[i][0]]['cons_gets']    = str(rows[i][5]) 
        out[rows[i][0]]['phy_reads']    = str(rows[i][6]) 
        out[rows[i][0]]['block_chgs']   = str(rows[i][7]) 
        out[rows[i][0]]['cons_chgs']    = str(rows[i][8]) 
        out[rows[i][0]]['event']        = str(rows[i][9]) 
        out[rows[i][0]]['last_call_et'] = str(rows[i][10]) 
        out[rows[i][0]]['qcsid']        = str(rows[i][11]) 
        out[rows[i][0]]['blocker']      = str(rows[i][12]) 

    return out

def getSystemStat(db_connection):

    cursor = db_connection.cursor()
    sql_stmt = "select rpad(lower(d.name), 10, ' ') || s.name, value from v$sysstat s, v$database d  \
                where NOT regexp_like(s.name, 'session .ga .*', 'i') and s.class not in (select wait_class# from V$SYSTEM_WAIT_CLASS where wait_class = 'Idle') "
    cursor.execute(sql_stmt)
    rows = cursor.fetchall()

    out = {}
    for i in range(0, len(rows)):
        out[rows[i][0]] = rows[i][1]

    return out

def getSystemEvent(db_connection):

    cursor = db_connection.cursor()
    sql_stmt = "select rpad(lower(d.name), 10, ' ') || e.event, time_waited from v$system_event e, v$database d  \
                where NOT regexp_like(e.wait_class, 'Idle', 'i') "
    cursor.execute(sql_stmt)
    rows = cursor.fetchall()

    out = {}
    for i in range(0, len(rows)):
        out[rows[i][0]] = rows[i][1]

    return out

def computeDelta(cur_sys, prev_sys):

    out = {}
    for i in cur_sys.keys():
        try:
            delta = cur_sys[i] - prev_sys[i]
        except:    
            delta = cur_sys[i]

        if delta > 0:
            out[i] = delta

    return out

def selectFoo(db_connection):
    cursor = db_connection.cursor()
    sql_stmt = "select 'foo' from dual"
    cursor.execute(sql_stmt)
    rows = cursor.fetchall()
    print rows[0][0]


##
## main
##
def main():

    password     = None
    sleep_time   = 4
    host         = str(platform.node())
    user         = 'sys'
    db_search    = '.*'
    lines        = 30 

    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:p:d:l:")
    except getopt.GetoptError, err:
        print str(err)
        usageExit('getopt error:')

    for o, a in opts:
        if o in ('-p'):
            password = a
        elif o in ('-l'):
            lines    = int(a)
        elif o in ('-d'):
            db_search = a
        elif o in ('-u'):
            user     = a
        else:
            assert False, "Invalid option "


    if password is None:
        print '#############################'
        print '##'
        print '## Enter ' + user + ' password for DBs'
        print '##'
        print '#############################'
        password   = getpass.getpass()
 
    top_label = getTopLabels()

    prev_system_event = {}
    cur_system_event  = {}
    system_event      = {}

    prev_system_stat  = {}
    cur_system_stat   = {}
    system_stat       = {}

    while 1 == 1:

        top_data     = getTopData(db_search)
        top_sum      = getTopSummary()

        prev_system_event = cur_system_event
        cur_system_event  = {}
        system_event      = {}

        prev_system_stat = cur_system_stat
        cur_system_stat  = {}
        system_stat      = {}

        session_data = {}

        for i in orautility.getLocalDbs(db_search):
            try:
                connect       = i + ':' + str(host) + ':' + user + ':' + password
                db_connection = orautility.createOraConnection(connect)

                s            = getSessionData(db_connection)
                session_data = dict(s.items() + session_data.items())

                s                 = getSystemStat(db_connection)
                cur_system_stat   = dict(s.items() + cur_system_stat.items())

                s                 = getSystemEvent(db_connection)
                cur_system_event  = dict(s.items() + cur_system_event.items())

            except Exception as e:
                print e
                pass

        system_stat  = computeDelta(cur_system_stat,  prev_system_stat)
        system_event = computeDelta(cur_system_event, prev_system_event)

        os.system('clear')

        printOraTop(top_data, session_data, system_stat, system_event, top_label, top_sum, lines)

        time.sleep(sleep_time)



#########################
##
## main()
##
##############################
if __name__ == '__main__':
    main()


