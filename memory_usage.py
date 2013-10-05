#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2012 u3z05en
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from subprocess import Popen, PIPE
from re import split
from sys import exit, argv

def leave_now(code):
    """Exit using the code given"""
    exit(int(code))

def main():
    """Run the command and decide which exit code to use"""
    # CREATE EACH OID STRING USING THE FIRST ARGUMENT PASSED
    cmd_mem_tot = "snmpget -v 1 -c public " + argv[1] + " 1.3.6.1.4.1.2021.4.5.0"
    cmd_mem_avail = "snmpget -v 1 -c public " + argv[1] + " 1.3.6.1.4.1.2021.4.6.0"
    cmd_mem_buff = "snmpget -v 1 -c public " + argv[1] + " 1.3.6.1.4.1.2021.4.14.0"
    cmd_mem_cached = 'snmpwalk -v 1 -c public ' + argv[1] + ' 1.3.6.1.4.1.2021.4.15.0'
    # CREATE LISTS OUT OF EACH COMMAND
    clTot = cmd_mem_tot.split(' ')
    clAvail = cmd_mem_avail.split(' ')
    clBuff = cmd_mem_buff.split(' ')
    clCached = cmd_mem_cached.split(' ')
    # RETRIEVE THE DATA FROM THE TARGET SERVER
    dTot = Popen(clTot, stdout = PIPE).communicate()[0].strip()
    dAvail = Popen(clAvail, stdout = PIPE).communicate()[0].strip()
    dBuff = Popen(clBuff, stdout = PIPE).communicate()[0].strip()
    dCached = Popen(clCached, stdout = PIPE).communicate()[0].strip()
    # FILTER OUT THE RESULTS AS WELL AS DETECT ERRORS
    try:
        dTot = split(r'INTEGER: ', dTot)[1].strip(' "')
    except:
        dTot = "FAILED"
    try:
        dAvail = split(r'INTEGER: ', dAvail)[1].strip(' "')
    except:
        dAvail = "FAILED"
    try:
        dBuff = split(r'INTEGER: ', dBuff)[1].strip(' "')
    except:
        dBuff = "FAILED"
    try:
        dCached = split(r'INTEGER: ', dCached)[1].strip(' "')
    except:
        dCached = "FAILED"
    # DETERMINE CRITICALITY LEVEL CODE OR UNKNOWN
    if not dTot == "FAILED" and not dAvail == "FAILED" and not dBuff == "FAILED" and not dCached == "FAILED":
        memUsed = ((float(dTot) - float(dAvail)) - float(dBuff) - float(dCached)) / float(dTot) * 100
        print 'Memory use at ' + '{:.2%}'.format(memUsed / 100) + ' | ' + "'Memory Usage'=" + '{:.2%}'.format(memUsed / 100) + ';' + argv[2] + ';' + argv[3]
        if memUsed > int(argv[3]):
            code = 2
        elif memUsed > int(argv[2]):
            code = 1
        else:
            code = 0
    else:
        print "SNMP Retrieve Failed"
        code = 3
    leave_now(code)

if __name__ == '__main__':
    main()
