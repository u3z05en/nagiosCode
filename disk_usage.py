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
    cmd_used_space = "snmpget -v 1 -c public " + argv[1] + " .1.3.6.1.4.1.2021.9.1.9.1"
    cmd_used_space = cmd_used_space.split(' ')
    used_space = Popen(cmd_used_space, stdout = PIPE).communicate()[0].strip()
    try:
        used_space = split(r'INTEGER:', used_space)[1].strip()
    except:
        used_space = "FAILED"
    if not used_space == "FAILED":
        used_space = int(used_space)
        print "Disk Use at " + str(used_space) + '%' + ' | ' + "'Disk Use'=" + str(used_space) + '%;' + argv[2] + ';' + argv[3]
        if used_space > int(argv[3].strip('%')):
            code = 2
        elif used_space > int(argv[2].strip('%')):
            code = 1
        else:
            code = 0
    else:
        print "SNMP Retrieve Failed"
        code = 3
    leave_now(code)

if __name__ == '__main__':
    main()
