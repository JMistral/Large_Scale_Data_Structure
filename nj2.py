#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 14:11:10 2017

@author: jessie
"""

import numpy
import csv


f = open('HW7_distance1.csv')
csv_f = csv.reader(f)
names = []
dist = []
for row in csv_f:
  names.append(row[0])
  d = []
  for n in row[1:]:
      if n != '':
          d.append(float(n))
      else:
          d.append(0)
  d.append(0)
    
  dist.append(d)
  
mat = numpy.array(dist)
  
def calcDist(distMat, i, j):


   if i < j:
      i, j = j, i
   return distMat[i][j]

def calcDistSum(distMat, i):

   sum = 0

   for k in range(len(distMat)):
      sum += distMat[i][k]

   for k in range(len(distMat)):
      sum += distMat[k][i]

   return sum

def calcM(distMat, i, j):

   return (len(distMat)-2)*calcDist(distMat, i, j) - \
           calcDistSum(distMat, i) - \
           calcDistSum(distMat, j)

def calcMMat(distMat):


   M = numpy.zeros((len(distMat),len(distMat)), int)

   for i in range(1, len(distMat)):
      for j in range(i):
         M[i][j] = calcM(distMat, i, j)

   return M

def calcDistOldNew(distMat, i, j):

   #diu = (.5)*(calcDist(distMat, i, j))
   return (.5)*(calcDist(distMat, i, j)) + ((1./(2*(len(distMat)-2))) * \
          (calcDistSum(distMat,i) - calcDistSum(distMat, j)))

def calcDistNewOther(distMat, m, i, j):

   return (.5)*(calcDist(distMat,i,m) - calcDistOldNew(distMat, i, j)) + \
          (.5)*(calcDist(distMat,j,m) - calcDistOldNew(distMat, j, i))
   
def minMVal(M):

   iMin = 0
   jMin = 0
   MMin = 0

   for i in range(len(M)):
      for j in range(len(M)):
         if min(MMin, M[i][j]) == M[i][j]:
            MMin = M[i][j]
            iMin = i
            jMin = j

   if i > j:
      i, j = j, i

   return MMin, iMin, jMin

def doNeigJoin(mat, species,debug=0):

   if len(mat) == 1:
       s = str(species).replace(' ', '').replace('[','(').replace(']',')').replace('\'','').replace(',','').replace('!',',')
       #s.replace('\'','').replace(',','').replace('!',',')
       return s

   M = calcMMat(mat)

   minM, idA, idB = minMVal(M)

   # initialize new distance matrix
   newMat = numpy.zeros((len(mat)-1, len(mat)-1), float)

   oldspecies = species[:]
   oldspecies.remove(species[idA])
   oldspecies.remove(species[idB])
   if debug:
       print(idA,':',calcDistOldNew(mat, idA, idB))
       
   if len(mat) == 2:
       newspecies = [species[idA],':',mat[1][0]/2,\
                   species[idB],':',mat[1][0]/2] \
                   + oldspecies
   else:
       newspecies = [[species[idA],':',calcDistOldNew(mat, idA, idB),'!',\
                   species[idB],':',calcDistOldNew(mat, idB, idA)]]\
                   + oldspecies

   # calculate new distance matrix for new U
   for i in range(1, len(newMat)):
      oldI = species.index(newspecies[i])
      newMat[i][0] = calcDistNewOther(mat, oldI, idB, idA)

   for i in range(2, len(newMat)):
      for j in range(1, len(newMat)-1):
         oldI = species.index(newspecies[i])
         oldJ = species.index(newspecies[j])
         newMat[i][j] = mat[oldI][oldJ]

   return doNeigJoin(newMat, newspecies)

def main():
    print(mat)
    print(doNeigJoin(mat, names))
    
main()



