#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      joe
#
# Created:     13/11/2017
# Copyright:   (c) joe 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    first = 0b100
    second = 0b101
    res = (first<<3) | (second)
    print bin(res)

if __name__ == '__main__':
    main()
