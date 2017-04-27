import random
import string

class Sequence(object):
    def __init__(self,read=None):
        self.read = read
        
    def generate(self,length):
        self.read = ""
        for i in range(length):
            rn = random.random()
            if rn<=0.25:
                self.read += "A"
            elif rn>0.25 and rn<=0.5:
                self.read += "C"
            elif rn>0.5 and rn<=0.75:
                self.read += "G"
            else:
                self.read += "T"
    
    def radix(self):
        value = 0
        N = len(self.read)
        for i in range(N):
            if self.read[i] is "A":
                value += 0*(4**(N-i))
            elif self.read[i] is "C":
                value += 1*(4**(N-i))
            elif self.read[i] is "G":
                value += 2*(4**(N-i))
            else:
                value += 3*(4**(N-i))
        return value
        
    

class HashTable(object):
    def __init__(self,size):
        self.size = size
        self.slot = []
        for i in range(size):
            self.slot.append([])
            
    def add(self,seq):
        value = seq.radix()
        HashSlot = self.slot[value%self.size]
        for i in range(len(HashSlot)):
            if HashSlot[i][0] == value:
                HashSlot[i] = (value,seq)
                break
        HashSlot.append((value,seq))
        
    def check(self,seq):
        value = seq.radix()
        HashSlot = self.slot[value%self.size]
        for e in HashSlot:
            if e[0] == value:
                return True,value%self.size
        return False,None
        
        


sequences = []
for j in range(100000):
    s = Sequence()
    s.generate(16)
    sequences.append(s)
 
h = HashTable(50000)   
for seq in sequences:
    #print(seq.read)
    h.add(seq)

(boo,slot) = h.check(sequences[555])
if boo:
    print ("read # 555 is in slot ",slot)
#
#v = s.radix()
#print v

#using build-in dictionary structure to implement
keys = list(map(hash,sequences))

i = 0
d = {}
for k in keys:
    d[k] = sequences[i]
    i += 1
    
print (keys[:5])
print (d[keys[555]].read)

#comparing two methods of hash table
r555 = h.slot[slot]
for rr in range(len(r555)):
    print (r555[rr])

    
        