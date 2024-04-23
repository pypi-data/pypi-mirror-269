This library is forked from https://github.com/mlagace/upcdb, but updated to the new api definition. It also uses requests instead of urllib2

upcdb
=====

upcdb is a Python library that allows you to use the http://www.upcdatabase.org API to get UPC details

HowTo
=====

from upcdb import UPCDB

upcdb   = UPCDB('API KEY')

upc     = upcdb.get('UPC')

print upc.name

print upc.description

print upc.valid

print upc.price

print upc.description

print upc.ratingsup

print upc.ratingsdown

print upc.reason

print upc.todict()
