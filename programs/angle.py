#!/usr/bin/env python
from builtins import input
import sys
import numpy


import pmagpy.pmag as pmag


def main():
    """
    NAME
        angle.py

    DESCRIPTION
      calculates angle between two input directions D1,D2

    INPUT (COMMAND LINE ENTRY)
           D1_dec D1_inc D1_dec D2_inc
    OUTPUT
           angle

    SYNTAX
        angle.py [-h][-i] [command line options] [< filename]

    OPTIONS
        -h prints help and quits
        -i for interactive data entry
        -f FILE input filename
        -F FILE output filename (required if -F set)
        Standard I/O
    """
    out = ""
    if '-h' in sys.argv:
        print(main.__doc__)
        sys.exit()
    if '-F' in sys.argv:
        ind = sys.argv.index('-F')
        o = sys.argv[ind + 1]
        out = open(o, 'w')
    if '-i' in sys.argv:
        cont = 1
        while cont == 1:
            dir1, dir2 = [], []
            try:
                ans = input('Declination 1: [ctrl-D  to quit] ')
                dir1.append(float(ans))
                ans = input('Inclination 1: ')
                dir1.append(float(ans))
                ans = input('Declination 2: ')
                dir2.append(float(ans))
                ans = input('Inclination 2: ')
                dir2.append(float(ans))
            except:
                print("\nGood bye\n")
                sys.exit()

            # send dirs  to angle and spit out result
            ang = pmag.angle(dir1, dir2)
            print('%7.1f ' % (ang))
    elif '-f' in sys.argv:
        ind = sys.argv.index('-f')
        file = sys.argv[ind + 1]
        file_input = numpy.loadtxt(file)
    else:
        # read from standard input
        file_input = numpy.loadtxt(sys.stdin.readlines(), dtype=numpy.float)
    if len(file_input.shape) > 1:  # list of directions
        dir1, dir2 = file_input[:, 0:2], file_input[:, 2:]
    else:
        dir1, dir2 = file_input[0:2], file_input[2:]
    angs = pmag.angle(dir1, dir2)
    for ang in angs:   # read in the data (as string variable), line by line
        print('%7.1f' % (ang))
        if out != "":
            out.write('%7.1f \n' % (ang))
    if out:
        out.close()


if __name__ == "__main__":
    main()
