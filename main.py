import unittest

def main():

  # request action [1=test, 2=hash, 3=rhash]
  action = input("Choose an action [T=test, h=hash, r=rhash]: ")

  # What action should we run?
  if ( action == "" or action.lower() == "t" ):
    # Run tests.
    print("Executing Tests.")
    test = Tests()
    test.hashTest()
    test.rhashTest()
  elif ( action.lower() == "h" ):
    # Hash.
    i = input("Specify an integer to hash [-8192..8191]: ")
    print( hash( int(i) ) )
  elif ( action.lower() == "r" ):
    # Reverse Hash.
    v = input("Specify 4 character value [00..7F]: ")
    h = int(v[:2], 16)
    l = int(v[2:], 16)
    print( rhash( h, l ) )
  else:
    # Error.
    print( "Invalid action, exiting." )
    exit()

# Convert an integer into a hash.
def hash(v):
    # Verify the integer is indeed an int, and lets make sure it is within the 14 bit range.
    if (isinstance(v, int) and v >= -8192 and v <= 8191):

        # Increase to remove negative values.
        v = v + 8192

        # Pack that value into two bytes such that the most significant bit of each is cleared
        lowByte = "%02X" % (v & 0x007F)
        highByte = "%02X" % (v >> 7)

        # Format the two bytes as a single 4-character hexadecimal string and return it.
        return (highByte + lowByte)
    else:
        return "Invalid value. An integer between -8192 and 8191 must be entered."

# Accept two bytes on input, both in the range [0x00..0x7F] and recombine
# them to return the corresponding integer between [-8192..+8191]
def rhash(highByte, lowByte):

  # Evaluate each byte to be within the valid range.
  if ( highByte >= 0x00 and highByte <= 0x7F ):

    # Convert both bytes back to integers.
    v1 = highByte << 7
    v2 = lowByte & 0x007F

    # Return combined value, reduced by 8192.
    return (v1 + v2 - 8192)
  else:
      return "Invalid byte entries. Hex values between '0x00' and '0x7F' must be entered."

class Tests(unittest.TestCase):
    def hashTest(self):
        self.assertEqual( hash( 9999 ),   "Invalid value. An integer between -8192 and 8191 must be entered." )
        self.assertEqual( hash( -8192 ),  "0000" )
        self.assertEqual( hash( 0 ),      "4000" )
        self.assertEqual( hash( 8191 ),   "7F7F" )
        self.assertEqual( hash( 2048 ),   "5000" )
        self.assertEqual( hash( -6907 ),  "0A05" )
        self.assertEqual( hash( 2688 ),   "5500" )
    
    def rhashTest(self):
        self.assertEqual( rhash( 0x40, 0x00 ), 0 )
        self.assertEqual( rhash( 0x00, 0x00 ), -8192 )
        self.assertEqual( rhash( 0x7F, 0x7F ), 8191 )
        self.assertEqual( rhash( 0x50, 0x00 ), 2048 )
        self.assertEqual( rhash( 0x0A, 0x05 ), -6907 )
        self.assertEqual( rhash( 0x55, 0x00 ), 2688 )

if __name__ == '__main__':
    main()