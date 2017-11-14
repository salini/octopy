

### functions from: https://wiki.python.org/moin/BitManipulation
def testBit(int_type, offset):
    mask = 1 << offset
    return (int_type & mask)

def setBit(int_type, offset):
    mask = 1 << offset
    return (int_type | mask)

def clearBit(int_type, offset):
    mask = ~(1 << offset)
    return (int_type & mask)

