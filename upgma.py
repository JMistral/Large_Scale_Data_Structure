#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import sys


f = open('HW7_distance1.csv')
csv_f = csv.reader(f)
names = []
dist = []
for row in csv_f:
  names.append(row[0])
  d = []
  for n in row[1:]:
      if n != '':
          d.append(int(n))
  dist.append(d)


#print(names)
#print(dist)

class cluster:
    pass

def make_clusters(species):
    clusters = {}
    id = 1
    for s in species:
        c = cluster()
        c.id = id
        c.data = s
        c.size = 1
        c.height = 0
        clusters[c.id] = c
        id = id + 1
    return clusters

def find_min(clu, d):
    mini = None
    i_mini = 0
    j_mini = 0
    for i in clu:
        for j in clu:
            if j>i:
                tmp = d[j -1 ][i -1 ]
                if not mini:
                    mini = tmp
                if tmp <= mini:
                    i_mini = i
                    j_mini = j
                    mini = tmp
    return (i_mini, j_mini, mini)

def regroup(clusters, dist):
    i, j, dij = find_min(clusters, dist)
    ci = clusters[i]
    cj = clusters[j]
    # create new cluster
    k = cluster()
    k.id = max(clusters) + 1
    k.data = (ci, cj)
    k.size = ci.size + cj.size
    k.height = dij / 2. # to be modified in NHJ
    # remove clusters
    del clusters[i]
    del clusters[j]
    # compute new distance values and insert them
    dist.append([])
    for l in range(0, k.id -1):
        dist[k.id-1].append(0)
    for l in clusters:
        dil = dist[max(i, l) -1][min(i, l) -1]
        djl = dist[max(j, l) -1][min(j, l) -1]
        dkl = (dil * ci.size + djl * cj.size) / float (ci.size + cj.size)
        #print('i:',ci.size,'j' ,cj.size)
        dist[k.id -1][l-1] = dkl
    # insert the new cluster
    clusters[k.id] = k

    if len(clusters) == 1:
        # we're through !
        l = list(clusters.values())
        return l[0]
    else:
        return regroup(clusters, dist)

def pprint(tree, len):
    if tree.size > 1:
        # it's an internal node
        sys.stdout.write("(")
        #print("(",end = " ")
        pprint(tree.data[0], tree.height)
        sys.stdout.write(",")
        #print (",",end = " ")
        pprint(tree.data[1], tree.height)
        sys.stdout.write("):%2.2f" % (len - tree.height))
        #print ("):%2.2f" % (len - tree.height)),
    else :
        # it's a leaf
        sys.stdout.write("%s:%2.2f" % (tree.data, len))
        #print ("%s:%2.2f" % (tree.data, len)),

clu = make_clusters(names)
tree = regroup(clu, dist)
pprint(tree, tree.height)
