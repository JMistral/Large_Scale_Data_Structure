#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 23:38:17 2017

@author: jessie
"""

import numpy as np
import pickle
import sys
import random
    
pickle_in = open('index_seeds_Dengue.pickle','rb')
hash_all_seeds = pickle.load(pickle_in)

pickle_in2 = open('reads_50mers.pickle',"rb")
reads_50mers = pickle.load(pickle_in2)

f = open("sequence.fasta.txt","r")
file = f.readlines()

genome = []
seq = ""
for f in file:
    if not f.startswith('>'):
        f = f.replace(" ","")
        f = f.replace("\n","")
        seq = seq + f
    else:
        genome.append(seq)
        seq = ""
genome.append(seq)
genome = genome[1:]

#%%
r = open("test_reads.txt","r")
file2 = r.readlines()
test_reads = []
seq = ""
for r in file2:
    if not r.startswith('>'):
        r = r.replace(" ","")
        r = r.replace("\n","")
        seq = seq + r
    else:
        test_reads.append(seq)
        seq = ""
test_reads.append(seq)
test_reads = test_reads[1:]
#%%
#==============================================================================
# BLAST using SW. seed length = 11
#==============================================================================
def radix(seq):
    value = 0
    N = len(seq)
    for i in range(N):
        if seq[i] == "A":
            value += 0*(4**(N-i))
        elif seq[i] == "C":
            value += 1*(4**(N-i))
        elif seq[i] == "G":
            value += 2*(4**(N-i))
        else:
            value += 3*(4**(N-i))
    return value

def generate_seg(sequence,n,l,error_rate,rd):
    length = len(sequence)
    # rd <--- randomly generate fragment or find all the seeds
    if rd:
        start_point = np.random.randint(low = 0,high=length-l,size=n)
    else:
        start_point = range(length-l+1)
    segments = []
    for i in start_point:
        origin = sequence[i:i+l]
        mutated = []
        # generate a bernoulli rand
        oops = np.random.binomial(n=1,p=error_rate,size=l)
        for o in range(l):
            if oops[o] == 1:
                alphabets = ['A','C','G','T']
                alphabets.remove(origin[o])
                sub = np.random.randint(low=0,high=2)
                err = alphabets[sub]
                mutated+=err
            else:
                mutated+=origin[o]
        segments.append(mutated)
    return np.asarray(segments)
# copy paste my Smith Waterman......
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
                
def Char2Num(char):
    value = 0
    if char == "A":
        value =1
    elif char == "C":
        value = 2
    elif char == "G":
        value = 3
    elif char == "T":
        value = 4
    else:
        value = 0
    return value

class Score(object):
        def __init__(self,pair,neighbors=[[],[],[]]):
            self.pair = [Char2Num(pair[0]),Char2Num(pair[1])]
            self.neighbors=neighbors
        def match(self,matrix):
            Mij=matrix[self.pair[0]][self.pair[1]]
            Gapi = matrix[self.pair[0]][0]
            Gapj = matrix[0][self.pair[1]]
            Dmatch = self.neighbors[0]+Mij
            Dgapi = self.neighbors[1]+Gapi #introduce a gap vertically
            Dgapj = self.neighbors[2]+Gapj #introduce a gap horizontally
            D = np.array([Dmatch,Dgapi,Dgapj,0]) 
            self.score = np.amax(D)
            self.pointer = np.argmax(D)
        def row_ini(self,matrix):
            self.score = 0
            self.pointer = 3
        def col_ini(self,matrix):
            self.score = 0
            self.pointer = 3
        def zero_ini(self,matrix):
            self.score = 0
            self.pointer = 3 # when pointer = 3, it point to nothing....

def trace_back(query,subject,scores,trace_location):
    r = trace_location[0]
    c = trace_location[1]
    new_query = []
    matching_info = []
    new_subject = []
    while(scores[r,c].pointer < 3):
        pointer = scores[r,c].pointer      
        if pointer == 0:
            new_query.append(query[r])
            new_subject.append(subject[c])
            if query[r] == subject[c]:
                matching_info.append('|')
            else:
                matching_info.append('x')
        
            r = r-1
            c = c-1
        elif pointer == 1:
            new_subject.append(' ')
            new_query.append(query[r])
            matching_info.append(' ')
            
            r = r-1
        else:
            new_subject.append(subject[c])
            new_query.append(' ')
            matching_info.append(' ')
            
            c = c-1
    new_query.reverse()
    new_subject.reverse()
    matching_info.reverse()
    return new_query,new_subject,matching_info
#%%            
matrix = [[0,-3,-3,-3,-3],[-3,2,-1,-1,-1],[-3,-1,2,-1,-1],[-3,-1,-1,2,-1],[-3,-1,-1,-1,2]]

#for read in reads_50mers[0:10]:
for read in test_reads:
    # dissemble reads
    read_seeds = generate_seg(read,40,11,0,False)
    # look for seed-match
    for i in range(len(read_seeds)):
        vi = radix(read_seeds[i])
        for j in range(len(hash_all_seeds)):
            vj = hash_all_seeds[j]
            # if seed-match is found, extend it
            if vj == vi:
                left_edge = max([j-i,0])
                right_edge = min([j+(50-i),len(hash_all_seeds)-1])
                subject = ['']
                query = ['']
                for ii in range(len(read)):
                    query.append(read[ii])
                for jj in range(left_edge,right_edge):
                    subject.append(genome[0][jj])
                scores = np.empty([len(query), len(subject)], dtype=Score)
                trace_score = 0
                trace_location = [0,0]
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
                        if scores[r+1,c+1].score > trace_score:
                            trace_score = scores[r+1,c+1].score
                        trace_location = [r+1,c+1]
                [new_query,new_subject,matching_info] = trace_back(query,subject,scores,trace_location)
#    text_file = open('TestResult.txt','w')
#    text_file.write()
    n = len(new_query)
    print('')
    for ns in range(n):
        sys.stdout.write(new_subject[ns])
        
    print('')
    for m in range(n):
        sys.stdout.write(matching_info[m])
    
    print('')
    
    for nq in range(n):
        sys.stdout.write(new_query[nq])
    print('')