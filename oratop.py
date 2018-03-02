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

try:
    import os, re, sys, operator, time, cx_Oracle, binascii, platform, getpass, argparse
    import orautility
except:
    print('Unable to import python modules')
    sys.exit(2)


sys.path.append(os.path.abspath('bin'))

##############################
##
## Functions
##
#######################################
class input_var:

    ###################
    ###
    ### Class for input variables
    ### Leave as pass and use in argument parsing
    ###
    ############################

    pass


def format_number(n, unit=1000):
    if n == None:
        return '0'

    if n == ' ':
        return ' '

    n = int(n)

    length = len(str(n))

    if length > 13:
        return str(round(n/unit/unit/unit/unit)) + 'P'
    elif length > 10:
        return str(round(n/unit/unit/unit)) + 'G'
    elif length > 7:
        return str(round(n/unit/unit)) + 'M'
    elif length > 4:
        return str(round(n/unit)) + 'K'
    else:
        return str(n)


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

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
    print('\n--------------')
    print('top + Oracle = OraTop')
    print('---------------------')



def printOraTop(top_data, session_data, system_stat, system_event, top_label, top_sum, lines):
    top_format = '{:>6}  {:<10s} {:>3} {:>5} {:>5} {:>10}  {:<26s} {:<16s} {:<10s}  {:>8} {:>8} {:>9} {:>9} {:>9} {:>9} {:>9} {:>9}  {:<50s}' 
    sys_format = '{:<60s} {:<20}'

    printLabel()

    print()
    for i in top_sum:
        print(i.replace('\n', ''))


    sorted_system_stat  = sorted(iter(system_stat.items()), key=operator.itemgetter(1))
    sorted_system_event = sorted(iter(system_event.items()), key=operator.itemgetter(1))


    if len(sorted_system_stat)-5 < 0:
        sys_start=0
    else:
        sys_start = len(sorted_system_stat)-5

    sys_stop = len(sorted_system_stat)
    for i in range(sys_start, sys_stop):
        if i == sys_start:
            print()
            print(color.BOLD + sys_format.format( 'DB        System Stats', 'Value Delta' ) + color.END) 
        stat=sorted_system_stat[i][0]
        value=sorted_system_stat[i][1]
        #print( sys_format.format(sorted_system_stat[i]) )
        print( sys_format.format(stat, value ))


    if len(sorted_system_event)-5 < 0:
        sys_start=0
    else:
        sys_start = len(sorted_system_event)-5

    sys_stop = len(sorted_system_event)
    for i in range(sys_start, sys_stop):
        if i == sys_start:
            print()
            print(color.BOLD + sys_format.format( 'DB        System Events', 'Waited Delta' ) + color.END )
        stat=sorted_system_event[i][0]
        value=sorted_system_event[i][1]
        print( sys_format.format(stat, value ))
        #print(sys_format.format( sorted_system_event[i]))

    print() 
    for i in top_label:
        print( color.BOLD + top_format.format( *i ) + color.END )

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


            print(top_format.format( top_data[i][0],  top_data[i][1], \
                                 top_data[i][7],  top_data[i][8], \
                                 top_data[i][9],  top_data[i][10],\
                                 #str(' '.join(top_data[i][11:]))[:25], \
                                 str(' '.join(top_data[i][11:])), \
                                 sql_id,          sid,            \
                                 qcsid,           blocker, \
                                 lst_call,        \
                                 format_number( blk_gts, 1024 ),         \
                                 format_number( con_gts, 1024 ),         \
                                 format_number( phy_rds, 1024 ),         \
                                 format_number( blk_chg, 1024 ),         \
                                 format_number( con_chg, 1024 ),         \
                                 event[:45] 
                               )) 
        

def getTopLabels(os_user, host):
    top_cmd = 'ssh ' + os_user + '@' + host  + ' top -b -n 1| grep PID'
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


def getTopSummary(os_user, host):
    top_cmd = 'ssh ' + os_user + '@' + host  + " top -b -n 2 | grep -v '^ *[0-9]' | grep -v PID | sed '/^$/d' | tail -5 "
    top_std_out = os.popen(top_cmd).readlines()
    r  = []
    r.append(tuple(top_std_out))
    return top_std_out


def getTopData(os_user, host ):
    #top_cmd= 'ssh ' + os_user + '@' + host  + "  top -c -b -n 1 -u oracle | grep -v '^[a-zA-Z]' 2>/dev/null | grep -v PID  2>/dev/null    | head -100"
    top_cmd= 'ssh ' + os_user + '@' + host  + "  top -c -b -n 1  | grep -v '^[a-zA-Z]' 2>/dev/null | grep -v PID  2>/dev/null    | head -100"

    top_std_out = os.popen(top_cmd).readlines()
    top_output = []
    for i in range(0, len(top_std_out)):
        top_output.append([])
        top_output[i] = top_std_out[i].split()
    
    return top_output


def getSessionData(db_connection):
    cursor = db_connection.cursor()
    ###io.block_gets, io.consistent_gets, io.physical_reads, io.block_changes, io.consistent_changes, s.event, s.last_call_et, nvl(to_char(px.qcsid), ' '), nvl(to_char(s.blocking_session), ' ') \
    sql_stmt = "select p.spid, decode(s.sql_id, null, '  ', s.sql_id || '/' || s.sql_child_number), s.username, decode(s.sid, null, '', s.sid || ',' ||  s.serial#), \
                io.block_gets, io.consistent_gets, io.physical_reads, io.block_changes, io.consistent_changes,  \
                case when s.state != 'WAITING' \
                    then 'CPU (Prev: ' || case when length(s.event) > 45 then  rpad(s.event, 45, ' ') || '...)' else s.event || ')' end \
                    else  rpad(s.event || '  (' || lower(s.wait_class) || ')' , 47, ' ') || case when length(s.event || s.wait_class ) > 45 then '...' else NULL end end as event, \
                s.last_call_et, nvl(to_char(px.qcsid), ' '), nvl(to_char(s.blocking_session), ' ') \
                from v$session s, v$process p, v$sess_io io, v$px_session px \
                where s.sid = px.sid(+) and s.sid = io.sid and s.paddr = p.addr  "
                ##where s.sid = px.sid(+) and s.sid = io.sid and s.paddr = p.addr  and s.sql_id is not null"
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
    for i in list(cur_sys.keys()):
        try:
            delta = cur_sys[i] - prev_sys[i]
        except:    
            delta = cur_sys[i]

        if delta > 0:
            out[i] = delta

    return out

def getLocalDbs(os_user, host):
    db_list = []

    cmd =  'ssh ' + os_user + '@' + host  + " cat /etc/oratab | grep -v '^#' | grep -v ^$ | awk -F: '{print $1}' "
     
    std_output = os.popen(cmd).readlines()
    for i in std_output:
        db_list.append( i.replace('\n', '') )
    
    return db_list

 
class hostTranslation:

    ###################
    ###
    ### Host transation
    ### Names in DAR need translation if scan addresses are used
    ###
    ############################

    name = {'at12adm01vm01.dbsv.in.here.com' : 'at1201vm01-vip.dbsv.in.here.com',
            'at12adm01vm01'                  : 'at1201vm01-vip',
            'at13adm05vm01.dbsv.in.here.com' : 'at1305vm01-vip.dbsv.in.here.com',
            'at13adm05vm01'                  : 'at1305vm01-vip',
            'at12adm05vm01.dbsv.in.here.com' : 'at1205vm01-vip.dbsv.in.here.com',
            'at12adm05vm01'                  : 'at1205vm01-vip',
           }


##
## main
##
def main():

    db_password  = None
    sleep_time   = 4
    host         = None
    os_user      = 'oracle'
    db_user      = 'sys'
    db_search    = '.*'
    lines        = 40 


    parser = argparse.ArgumentParser()
    parser.add_argument('--db_password',          help='SysPassword')
    parser.add_argument('--lines',                help='Lines')
    parser.add_argument('--host',                 help='host')

    args = parser.parse_args(namespace=input_var)

    if input_var.db_password is not None:    db_password = input_var.db_password
    if input_var.lines is not None:          lines = input_var.lines
    if input_var.host is not None:           host = input_var.host


    if db_password is None:
        print('#############################')
        print('##')
        print('## Enter ' + db_user + ' password for DBs')
        print('##')
        print('#############################')
        db_password   = getpass.getpass()

    if os_user is None:
        print('OS User not specified')
        sys.exit(2)
      
    if host is None:
        print('Host not specified')
        sys.exit(2)

 
   
    top_label = getTopLabels(os_user, host)

    prev_system_event = {}
    cur_system_event  = {}
    system_event      = {}

    prev_system_stat  = {}
    cur_system_stat   = {}
    system_stat       = {}

    count = 0 
    while 1 == 1:

        count        = count + 1
        top_data     = getTopData(os_user, host)

        top_sum      = getTopSummary(os_user, host)

        prev_system_event = cur_system_event
        cur_system_event  = {}
        system_event      = {}

        prev_system_stat = cur_system_stat
        cur_system_stat  = {}
        system_stat      = {}

        session_data = {}

        db_host = hostTranslation.name[host]
 
        for i in getLocalDbs(os_user, host):
            try:
                connect       = i + ':' + db_host + ':' + db_user + ':' + db_password
                #db_connection = orautility.createOraConnection(connect)
                db_connection = cx_Oracle.connect(user=db_user, password=db_password, dsn=db_host + '/' + i, mode=cx_Oracle.SYSDBA )

                s            = getSessionData(db_connection)
                session_data = dict(list(s.items()) + list(session_data.items()))

                s                 = getSystemStat(db_connection)
                cur_system_stat   = dict(list(s.items()) + list(cur_system_stat.items()))

                s                 = getSystemEvent(db_connection)
                cur_system_event  = dict(list(s.items()) + list(cur_system_event.items()))

            except Exception as e:
                if count > 1:
                    print('Cannot connect to ' + i)
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


