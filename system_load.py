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
    cmd_load_1 = "snmpget -v 1 -c public " + argv[1] + " 1.3.6.1.4.1.2021.10.1.3.1"
    cmd_load_5 = "snmpget -v 1 -c public " + argv[1] + " 1.3.6.1.4.1.2021.10.1.3.2"
    cmd_load_15 = "snmpget -v 1 -c public " + argv[1] + " 1.3.6.1.4.1.2021.10.1.3.3"
    cmd_core = 'snmpwalk -v 1 -c public ' + argv[1] + ' 1.3.6.1.2.1.25.3.2.1.2 | grep "3.1.3"'
    cl1 = cmd_load_1.split(' ')
    cl5 = cmd_load_5.split(' ')
    cl15 = cmd_load_15.split(' ')
    l1 = Popen(cl1, stdout = PIPE).communicate()[0].strip()
    l5 = Popen(cl5, stdout = PIPE).communicate()[0].strip()
    l15 = Popen(cl15, stdout = PIPE).communicate()[0].strip()
    cores = Popen([cmd_core], stdout = PIPE, shell = True).communicate()[0]
    cores = cores.count('\n')    #len(cores.splitlines(True))
    try:
        l1 = split(r'STRING:', l1)[1].strip(' "')
    except:
        l1 = "FAILED"
    try:
        l5 = split(r'STRING:', l5)[1].strip(' "')
    except:
        l5 = "FAILED"
    try:
        l15 = split(r'STRING:', l15)[1].strip(' "')
    except:
        l15 = "FAILED"
    if not l1 == "FAILED" and not l5 == "FAILED" and not l15 == "FAILED":
        l1 = float(l1)
        l5 = float(l5)
        l15 = float(l15)
        print 'System Load at   ' + str(l1) + ', ' + str(l5) + ', ' + str(l15) + '   on   ' + str(cores) + '   cores.' + ' | ' + "'System Load(1)'=" + str(l1) + ';' + str(1 * cores) + ';' + str(1.4 * cores) + " 'System Load(5)'=" + str(l5) + ';' + str(1 * cores) + ';' + str(1.4 * cores) + " 'System Load(15)'=" + str(l15) + ';' + str(1 * cores) + ';' + str(1.4 * cores)
        if l5 > (1.3 * cores):
            code = 2
        elif l5 > (1 * cores):
            code = 1
        else:
            code = 0
    else:
        print "SNMP Retrieve Failed"
        code = 3
    leave_now(code)

if __name__ == '__main__':
    main()
