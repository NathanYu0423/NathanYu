fname = input ('Enter File: ')
if len(fname) < 1 : fname = 'cown.txt'
hand = open(fname)

di = dict ()
for lin in hand:
    lin = lin.rstrip()
    wds = lin.split()
    for w in wds:
        di[w] = di.get(w,0) + 1

largest = -1
theword = None
for k,v in di.items() :
    print (k,v)
    if v > largest :
        largest = v
        theword = w

print('Done',theword, largest)
