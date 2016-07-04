"""
 Naam:         testconverters.py
 Omschrijving: Tests for specifieke conversies
 Auteurs:      Just van den Broecke
"""

from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import sensorconverters
import sensordefs

# Nodig om output naar console/file van strings goed te krijgen
# http://www.saltycrane.com/blog/2008/11/python-unicodeencodeerror-ascii-codec-cant-encode-character/
# anders bijv. deze fout: 'ascii' codec can't encode character u'\xbf' in position 42: ordinal not in range(128)
# reload(sys)
# sys.setdefaultencoding( "utf-8" )

def main():
    """

    """
    print('hello')

if __name__ == "__main__":
    main()
