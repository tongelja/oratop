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


class oraTop():

    def __init__(self, os_user, db_user, db_password, host):

        self.top_label    = None
        self.top_data     = None
        self.top_sum      = None
        self.time_delta   = None
        self.system_stat  = None
        self.system_event = None
        self.session_data = None

        self.host         = host
        self.os_user      = 'oracle'
        self.db_user      = 'sys'
        self.db_password  = db_password

        self.lines        = {'top_lines' : 50, 'db_lines' : 5, 'new_lines': True }

    def snap(self, show_errors=False):

        curr_time    = 0
        prev_time    = 0

        host        = self.host
        db_user     = self.db_user
        os_user     = self.os_user
        db_host     = None
        db_password = self.db_password

        self.top_label = self.getTopLabels(os_user, host)
 
        prev_system_event = {}
        cur_system_event  = {}
        system_event      = {}
    
        prev_system_stat  = {}
        cur_system_stat   = {}
        system_stat       = {}
    
        count = 0 
        while count != 2:
    
            count        = count + 1
        
            prev_system_event = cur_system_event
            cur_system_event  = {}
            system_event      = {}
        
            prev_system_stat = cur_system_stat
            cur_system_stat  = {}
            system_stat      = {}
        
            session_data = {}
        
            db_host = hostTranslation.name[host]
        
       
            self.top_data     = self.getTopData(os_user, host)
            self.top_sum      = self.getTopSummary(os_user, host)
     
            for i in self.getLocalDbs(os_user, host):
                try:
                    connect       = i + ':' + db_host + ':' + db_user + ':' + db_password
                    db_connection = cx_Oracle.connect(user=db_user, password=db_password, dsn=db_host + '/' + i, mode=cx_Oracle.SYSDBA )
        
                    s = self.getSessionData(db_connection)
                    session_data = dict(list(s.items()) + list(session_data.items()))
        
                    s = self.getSystemStat(db_connection)
                    cur_system_stat   = dict(list(s.items()) + list(cur_system_stat.items()))
        
                    s = self.getSystemEvent(db_connection)
                    cur_system_event  = dict(list(s.items()) + list(cur_system_event.items()))
        
                except Exception as e:
                    if show_errors is True and count == 1:
                        print('Cannot connect to ' + db_user + '@' + i + '@' + db_host)
                    pass
        
            prev_time = curr_time
            curr_time=time.time()
    
            self.time_delta   = curr_time - prev_time
            self.session_data = session_data
            self.system_stat  = self.computeDelta(cur_system_stat,  prev_system_stat)
            self.system_event = self.computeDelta(cur_system_event, prev_system_event)
        
    

    def printLabel(self, host):
        print(color.BOLD + ' ----------------------' + color.END)
        print(color.BOLD + '|' + host +  color.END)
        print(color.BOLD + ' ----------------------' + color.END)
    
    
    
    def printReport(self, lines=None):


        top_data         = self.top_data
        session_data     = self.session_data
        system_stat      = self.system_stat
        system_event     = self.system_event
        top_label        = self.top_label
        top_sum          = self.top_sum
        time_delta       = self.time_delta
        host             = self.host

        if lines is None: lines = self.lines


        top_format = '{:>6}  {:<10s} {:>3} {:>5} {:>5} {:>10}  {:<20s} {:<11} {:<16s} {:<10s}  {:>8} {:>8} {:>9} {:>9} {:>9} {:>9} {:>9} {:>9}  {:<50s}' 
        sys_format = '{:<60s} {:<20}'
    
        self.printLabel(host)
    
        if lines['new_lines'] is True:  print()
        for i in top_sum:
            print(i.replace('\n', ''))
    
    
        sorted_system_stat  = sorted(iter(system_stat.items()), key=operator.itemgetter(1))
        sorted_system_event = sorted(iter(system_event.items()), key=operator.itemgetter(1))
    
    
        if len(sorted_system_stat)-lines['db_lines'] < 0:
            sys_start=0
        else:
            sys_start = len(sorted_system_stat) - lines['db_lines']
    
        sys_stop = len(sorted_system_stat)
        for i in range(sys_start, sys_stop):
            if i == sys_start:
                if lines['new_lines'] is True:  print()
                print(color.BOLD + sys_format.format( 'Instance    System Stats', 'Rate (per second)' ) + color.END) 
            stat=sorted_system_stat[i][0]
            value=format_number( sorted_system_stat[i][1] / time_delta ) + '/Sec'
            print( sys_format.format(stat, value ))
    
    
        if len(sorted_system_event)-lines['db_lines'] < 0:
            sys_start=0
        else:
            sys_start = len(sorted_system_event) - lines['db_lines']
    
        sys_stop = len(sorted_system_event)
        for i in range(sys_start, sys_stop):
            if i == sys_start:
                if lines['new_lines'] is True:  print()
                print(color.BOLD + sys_format.format( 'Instance    System Events', 'Rate (ms per second)' ) + color.END )
            stat=sorted_system_event[i][0]
            value=format_number( sorted_system_event[i][1] / time_delta ) + '/Sec'
            print( sys_format.format(stat, value ))
    
        if lines['new_lines'] is True:  print()
        for i in top_label:
            print( color.BOLD + top_format.format( *i ) + color.END )
    
        for i in range(0, lines['top_lines']):
    
            if len(top_data[i]) > 0:
                try:
                    sql_id       = session_data[top_data[i][0]]['sql_id']
                    instance     = session_data[top_data[i][0]]['instance']
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
                    instance     = ' ' 
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
                                     instance, sql_id,          sid,            \
                                     qcsid,           blocker, \
                                     lst_call,        \
                                     format_number( blk_gts, 1024 ),         \
                                     format_number( con_gts, 1024 ),         \
                                     format_number( phy_rds, 1024 ),         \
                                     format_number( blk_chg, 1024 ),         \
                                     format_number( con_chg, 1024 ),         \
                                     event[:45] 
                                   )) 

        print()    
    
    def getTopLabels(self, os_user, host):
        top_cmd = 'ssh ' + os_user + '@' + host  + ' top -b -n 1| grep PID'
        top_std_out = os.popen(top_cmd).readlines()[0].split()
        top_std_out.remove('PR')
        top_std_out.remove('NI')
        top_std_out.remove('VIRT')
        top_std_out.remove('RES')
        top_std_out.remove('SHR')
        top_std_out.append('INSTANCE')
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
    
    
    def getTopSummary(self, os_user, host):
        top_cmd = 'ssh ' + os_user + '@' + host  + " top -b -n 2 | grep -v '^ *[0-9]' | grep -v PID | sed '/^$/d' | tail -5 "
        top_std_out = os.popen(top_cmd).readlines()
        r  = []
        r.append(tuple(top_std_out))
        return top_std_out
    
    
    def getTopData(self, os_user, host ):
        #top_cmd= 'ssh ' + os_user + '@' + host  + "  top -c -b -n 1 -u oracle | grep -v '^[a-zA-Z]' 2>/dev/null | grep -v PID  2>/dev/null    | head -100"
        top_cmd= 'ssh ' + os_user + '@' + host  + "  top -c -b -n 1  | grep -v '^[a-zA-Z]' 2>/dev/null | grep -v PID  2>/dev/null    | head -100"
    
        top_std_out = os.popen(top_cmd).readlines()
        top_output = []
        for i in range(0, len(top_std_out)):
            top_output.append([])
            top_output[i] = top_std_out[i].split()
        
        return top_output
    
    
    def getSessionData(self, db_connection):
        cursor = db_connection.cursor()
        ###io.block_gets, io.consistent_gets, io.physical_reads, io.block_changes, io.consistent_changes, s.event, s.last_call_et, nvl(to_char(px.qcsid), ' '), nvl(to_char(s.blocking_session), ' ') \
        sql_stmt = "select p.spid,  \
                    decode(s.sql_id, null, '  ', s.sql_id || '/' || s.sql_child_number), s.username, decode(s.sid, null, '', s.sid || ',' ||  s.serial#), \
                    io.block_gets, io.consistent_gets, io.physical_reads, io.block_changes, io.consistent_changes,  \
                    case when s.state != 'WAITING' \
                        then 'CPU (Prev: ' || case when length(s.event) > 45 then  rpad(s.event, 45, ' ') || '...)' else s.event || ')' end \
                        else  rpad(s.event || '  (' || lower(s.wait_class) || ')' , 47, ' ') || case when length(s.event || s.wait_class ) > 45 then '...' else NULL end end as event, \
                    s.last_call_et, nvl(to_char(px.qcsid), ' '), nvl(to_char(s.blocking_session), ' '), inst.instance_name \
                    from v$session s, v$process p, v$sess_io io, v$px_session px, v$instance inst \
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
            out[rows[i][0]]['instance']     = str(rows[i][13]) 
    
        return out
    
    def getSystemStat(self, db_connection):
    
        cursor = db_connection.cursor()
        sql_stmt = "select rpad(lower(d.instance_name), 12, ' ') || s.name, value from v$sysstat s, v$instance d  \
                    where NOT regexp_like(s.name, 'session .ga .*', 'i') and s.class not in (select wait_class# from V$SYSTEM_WAIT_CLASS where wait_class = 'Idle') "
        cursor.execute(sql_stmt)
        rows = cursor.fetchall()
    
        out = {}
        for i in range(0, len(rows)):
            out[rows[i][0]] = rows[i][1]
    
        return out
    
    def getSystemEvent(self, db_connection):
    
        cursor = db_connection.cursor()
        sql_stmt = "select rpad(lower(d.instance_name), 12, ' ') || e.event, time_waited_micro from v$system_event e, v$instance d  \
                    where NOT regexp_like(e.wait_class, 'Idle', 'i') "
        cursor.execute(sql_stmt)
        rows = cursor.fetchall()
    
        out = {}
        for i in range(0, len(rows)):
            out[rows[i][0]] = rows[i][1]
    
        return out
    
    def computeDelta(self, cur_sys, prev_sys):
    
        out = {}
        for i in list(cur_sys.keys()):
            try:
                delta = cur_sys[i] - prev_sys[i]
            except:    
                delta = cur_sys[i]
    
            if delta > 0:
                out[i] = delta
    
        return out
    
    def getLocalDbs(self, os_user, host):
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
            'at12adm02vm01.dbsv.in.here.com' : 'at1202vm01-vip.dbsv.in.here.com',
            'at12adm03vm01.dbsv.in.here.com' : 'at1203vm01-vip.dbsv.in.here.com',
            'at12adm04vm01.dbsv.in.here.com' : 'at1204vm01-vip.dbsv.in.here.com',
            'at12adm05vm01.dbsv.in.here.com' : 'at1205vm01-vip.dbsv.in.here.com',
            'at12adm06vm01.dbsv.in.here.com' : 'at1206vm01-vip.dbsv.in.here.com',
            'at12adm07vm01.dbsv.in.here.com' : 'at1207vm01-vip.dbsv.in.here.com',
            'at12adm08vm01.dbsv.in.here.com' : 'at1208vm01-vip.dbsv.in.here.com',
            'at12adm01vm01'                  : 'at1201vm01-vip',
            'at12adm02vm01'                  : 'at1202vm01-vip',
            'at12adm03vm01'                  : 'at1203vm01-vip',
            'at12adm04vm01'                  : 'at1204vm01-vip',
            'at12adm05vm01'                  : 'at1205vm01-vip',
            'at12adm06vm01'                  : 'at1206vm01-vip',
            'at12adm07vm01'                  : 'at1207vm01-vip',
            'at12adm08vm01'                  : 'at1208vm01-vip',
            'at13adm01vm01.dbsv.in.here.com' : 'at1301vm01-vip.dbsv.in.here.com',
            'at13adm02vm01.dbsv.in.here.com' : 'at1302vm01-vip.dbsv.in.here.com',
            'at13adm03vm01.dbsv.in.here.com' : 'at1303vm01-vip.dbsv.in.here.com',
            'at13adm04vm01.dbsv.in.here.com' : 'at1304vm01-vip.dbsv.in.here.com',
            'at13adm05vm01.dbsv.in.here.com' : 'at1305vm01-vip.dbsv.in.here.com',
            'at13adm06vm01.dbsv.in.here.com' : 'at1306vm01-vip.dbsv.in.here.com',
            'at13adm07vm01.dbsv.in.here.com' : 'at1307vm01-vip.dbsv.in.here.com',
            'at13adm08vm01.dbsv.in.here.com' : 'at1308vm01-vip.dbsv.in.here.com',
            'at13adm01vm01'                  : 'at1301vm01-vip',
            'at13adm02vm01'                  : 'at1302vm01-vip',
            'at13adm03vm01'                  : 'at1303vm01-vip',
            'at13adm04vm01'                  : 'at1304vm01-vip',
            'at13adm05vm01'                  : 'at1305vm01-vip',
            'at13adm06vm01'                  : 'at1306vm01-vip',
            'at13adm07vm01'                  : 'at1307vm01-vip',
            'at13adm08vm01'                  : 'at1308vm01-vip',
           }


##
## main
##
def main():

    db_password  = None
    sleep_time   = 0
    host         = None
    os_user      = 'oracle'
    db_user      = 'sys'
    db_search    = '.*'

    parser = argparse.ArgumentParser()
    parser.add_argument('--db_password',          help='SysPassword')
    parser.add_argument('--lines',                help='Lines')
    parser.add_argument('--host',                 help='host')

    args = parser.parse_args(namespace=input_var)

    if input_var.db_password is not None:    db_password = input_var.db_password
    if input_var.lines is not None:          lines = input_var.lines
    if input_var.host is not None:           host_list = input_var.host


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
      
    if host_list is None:
        print('Host not specified')
        sys.exit(2)

    count = 0 
    while 1 == 1:

        count = count + 1

        if len(host_list.split(',')) == 2:
            lines = {'top_lines' : 15, 'db_lines' : 3 } 
        
        my_snaps = [] 
        for host in host_list.split(','):
            i = oraTop(os_user, db_user, db_password, host)
            if count == 1:
                i.snap(True)
            else:
                i.snap()

            my_snaps.append(i) 

        os.system('clear')
        host_count = len(my_snaps)
        if host_count == 1:
            lines        = {'top_lines' : 50, 'db_lines' : 5, 'new_lines': True }
        elif host_count == 2:
            lines        = {'top_lines' : 15, 'db_lines' : 3, 'new_lines': True }
        elif host_count == 3:
            lines        = {'top_lines' : 10, 'db_lines' : 2, 'new_lines': False }
        elif host_count >= 4:
            lines        = {'top_lines' : 5, 'db_lines' : 2, 'new_lines': False }

        for i in my_snaps:
            i.printReport(lines)


        time.sleep(sleep_time)



#########################
##
## main()
##
##############################
if __name__ == '__main__':
    main()


