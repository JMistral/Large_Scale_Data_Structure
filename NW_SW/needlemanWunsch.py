#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#==============================================================================
# Needleman-Wunsch
#==============================================================================
import numpy as np
import sys
import random

class Sequence(object):
    def __init__(self,read=None):
        self.read = read
        
    def generate(self,length):
        self.read = []
        for i in range(length):
            rn = random.random()
            if rn<=0.25:
                self.read.append("A")
            elif rn>0.25 and rn<=0.5:
                self.read.append("C")
            elif rn>0.5 and rn<=0.75:
                self.read.append("G")
            else:
                self.read.append("T")
  

def radix(seq):
    value = 0
    if seq == "A":
        value =1
    elif seq == "C":
        value = 2
    elif seq == "G":
        value = 3
    elif seq == "T":
        value = 4
    else:
        value = 0
    return value

class Score(object):
        def __init__(self,pair,neighbors=[[],[],[]]):
            self.pair = [radix(pair[0]),radix(pair[1])]
            self.neighbors=neighbors
        def match(self,matrix):
            Mij=matrix[self.pair[0]][self.pair[1]]
            Gapi = matrix[self.pair[0]][0]
            Gapj = matrix[0][self.pair[1]]
            Dmatch = self.neighbors[0]+Mij
            Dgapi = self.neighbors[1]+Gapi #introduce a gap vertically
            Dgapj = self.neighbors[2]+Gapj #introduce a gap horizontally
            self.score = np.amax(np.array([Dmatch,Dgapi,Dgapj]))
            self.pointer = np.argmax(np.array([Dmatch,Dgapi,Dgapj]))
        def row_ini(self,matrix):
            Gapj = matrix[0][self.pair[1]]
            Dgapj = self.neighbors[2]+Gapj
            self.score = Dgapj
            self.pointer = 2
        def col_ini(self,matrix):
            Gapi = matrix[self.pair[0]][0]
            Dgapi = self.neighbors[1]+Gapi
            self.score = Dgapi
            self.pointer = 1
        def zero_ini(self,matrix):
            self.score = 0
            self.pointer = 3 # when pointer = 3, it point to nothing....
        
matrix = [[0,-3,-3,-3,-3],[-3,2,-1,-1,-1],[-3,-1,2,-1,-1],[-3,-1,-1,2,-1],[-3,-1,-1,-1,2]]
#subject = ['','G','A','T','C','T','C','A','T','T','A']
for j in range(1000):
    s = Sequence()
    s.generate(100)
    subject = ['']
    for i in range(100):
        subject.append(s.read[i])
    query = ['','G','C','T','G','A','T','T','C']
    scores = np.empty([len(query), len(subject)], dtype=Score)
    Rows = len(query)
    Cols = len(subject)
    # scores matrix initialization
    scores[0,0] = Score(pair=['',''])
    scores[0,0].zero_ini(matrix)
    for c in range(Cols-1):
        scores[0,c+1] = Score(pair=[query[0],subject[c+1]])
        scores[0,c+1].neighbors = [[],[],scores[0,c].score]
        scores[0,c+1].row_ini(matrix)
        
    for r in range(Rows-1):
        scores[r+1,0] = Score(pair=[query[r+1],subject[0]])
        scores[r+1,0].neighbors = [[],scores[r,0].score,[]]
        scores[r+1,0].col_ini(matrix)
        
    for c in range(Cols-1):
        for r in range(Rows-1):
            scores[r+1,c+1] = Score(pair=[query[r+1],subject[c+1]])
            scores[r+1,c+1].neighbors = [scores[r,c].score,scores[r,c+1].score,scores[r+1,c].score]
            scores[r+1,c+1].match(matrix)
            
def trace_back(query,subject,scores):
    r = len(query)-1
    c = len(subject)-1
    l = max(r,c)
    new_query = np.empty(l, dtype=str)
    matching_info = np.empty(l, dtype=str)
    new_subject = np.empty(l, dtype=str)
    counter = l-1
    while(scores[r,c].pointer < 3):
        pointer = scores[r,c].pointer      
        if pointer == 0:
            new_query[counter] = query[r]
            new_subject[counter] = subject[c]
            if new_query[counter] == new_subject[counter]:
                matching_info[counter] = '|'
            else:
                matching_info[counter] = 'x'
            counter = counter-1
            r = r-1
            c = c-1
        elif pointer == 1:
            new_subject[counter] = ' '
            new_query[counter] = query[r]
            matching_info[counter] = ' '
            counter = counter-1
            r = r-1
        else:
            new_subject[counter] = subject[c]
            new_query[counter] = ' '
            matching_info[counter] = ' '
            counter = counter-1
            c = c-1
        
        
    return new_query,new_subject,matching_info

[new_query,new_subject,matching_info] = trace_back(query,subject,scores)
n = len(new_query)
for i in range(n):
    sys.stdout.write(new_subject[i])
    
print('')
for i in range(n):
    sys.stdout.write(matching_info[i])

print('')

for i in range(n):
    sys.stdout.write(new_query[i])   
