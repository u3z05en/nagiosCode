#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2012 u3z05en
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from subprocess import Popen, PIPE
from re import split, search, findall
from sys import exit, argv

def leave_now(code):
    """Exit using the code given"""
    exit(int(code))

def main():
    """Run the command and decide which exit code to use"""
    # CREATE EACH OID STRING USING THE FIRST ARGUMENT PASSED
    cmd_uptime = "snmpget -v 1 -c public " + argv[1] + " 1.3.6.1.2.1.1.3.0"
    # CREATE LISTS OUT OF EACH COMMAND
    clUptime = cmd_uptime.split(' ')
    # RETRIEVE THE DATA FROM THE TARGET SERVER
    dUptime = Popen(clUptime, stdout = PIPE).communicate()[0].strip()
    # FILTER OUT THE RESULTS AS WELL AS DETECT ERRORS
    try:
        dTotal = findall(r'\(.*\)', dUptime)[0].strip('()')
    except:
        dTotal = 'FAILED'
    try:
        dUptime = split(r'Timeticks: \(.*\) ', dUptime)[1].strip(' ')
    except:
        dUptime = 'FAILED'
    # DETERMINE CRITICALITY LEVEL CODE OR UNKNOWN
    if not dUptime == 'FAILED':
        print 'System Uptime at ' + dUptime + ' | ' + "'System Uptime'=" + dTotal
        if search(r'days', dUptime) == None:
            code = 1
        else:
            code = 0
    else:
        print 'SNMP Retrieve Failed'
        code = 3
    leave_now(code)

if __name__ == '__main__':
    main()
