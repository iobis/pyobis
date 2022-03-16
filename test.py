from pyobis import occurrences
print(occurrences.search(scientificname = 'Mola mola'))
# occurrences.search(scientificname = 'Mola mola', offset=0, limit=10)
#occurrences.search(geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', limit=20)
#occurrences.search( year="2013", limit=20)