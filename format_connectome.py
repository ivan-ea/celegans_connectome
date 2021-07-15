# -*- coding: utf-8 -*-


# Connectome data in 2 JSON files: chem.json and gap.json
# Polarity data in emask.npy
# source https://github.com/shlizee/C-elegans-Neural-Interactome

# Output = 2 adjacency matrices in .csv format
# For chem synapses: with directionality, and sign (representing polarity)
# For gap junctions: symetric

# labels.csv = Name of the neurons in order of their index

import json
import numpy as np

N = 279

with open ('data/chem.json') as chem_file:
    chem_dic = json.load(chem_file)

with open ('data/gap.json') as gap_file:
    gap_dic = json.load(gap_file)

Chem_mat = np.zeros((N,N))
Gap_mat = np.zeros((N,N))

# GAP JUNCTION CONNECTIONS
gap_links = gap_dic['links']

# Find if all gap junctions are bidirectional
i = 0
done = False
non_sym_sources = []
non_sym_targets = []
for d in gap_links:
    s = d['source']
    t = d['target']
    for e in gap_links:
        if (not done) and s == e['target'] and t == e['source']:
            i += 1
            done = True
            if d['value'] != e['value']:
                print("differnet value! for:") # none have different weight!
    if not done:
        #print(' no bidirectional for:', d) # 15 are not bidirectional
        non_sym_sources.append(s)
        non_sym_targets.append(t)
    else :
        done = False


print("bidirectional gap junctions:",i, "out of", len(gap_links))
# bidirectional gap junctions: 1050 out of 1065

# Solution 1: force all gap junctions bidirectional
for g in gap_links:
    s = g['source']
    t = g['target']
    v = g['value']
    Gap_mat[s,t] = v
    Gap_mat[t,s] = v

name_gap = 'results/Gap_headless.csv'
np.savetxt(name_gap, Gap_mat, fmt='%1.2f', delimiter=',')
print('Gap junctions matrix written in file:', name_gap,'(',
      np.count_nonzero(Gap_mat),'non-zero elements)')
#gap_test = np.loadtxt('Gap.csv', delimiter=',') # how to load the data

#Solution 2: remove non symetrical gap junctions
Gap_mat_no15 = Gap_mat
for i, j in zip(non_sym_sources, non_sym_targets):
    Gap_mat_no15[i,j] = 0
    Gap_mat_no15[j,i] = 0

name_gap2 = 'results/GapNo15_headless.csv'
np.savetxt(name_gap2, Gap_mat_no15, fmt='%1.2f', delimiter=',')
print('Gap junctions matrix  (without 15) written in file:', name_gap2,'(',
      np.count_nonzero(Gap_mat_no15),'non-zero elements)')

# CHEMICAL SYNAPSES

E = np.load('data/emask.npy')
E = E[:,0] #array of 279 elements. 1 = inhibitory synapse
# source index in E => GABAegic neuron => inhibitory (hypothesis)
# but AVL(124) and DVB(252) should be excitatory acording to Wormbook

chem_synapses = chem_dic['links']

for c in chem_synapses:
    s = c['source']
    t = c['target']
    v = c['value']
    if E[s] == 1:
        Chem_mat[s,t] = -v
    else:
        Chem_mat[s,t] = v


name_chem = 'results/Chem_headless.csv'
np.savetxt(name_chem, Chem_mat, fmt='%1.2f', delimiter=',')
print('Chemical synapses matrix written in file:', name_chem,
      '(',np.count_nonzero(Chem_mat),'non-zero elements)')
#chem_test = np.loadtxt('Chem.csv', delimiter=',') # how to load the data

# NEURON NAMES

labels = []
for node in chem_dic['nodes']:
    labels.append(node['name'])

labels_file = 'results/labels.csv'
file = open(labels_file,'w')
for l in labels:
    file.write(l+'\n')

file.close()

print('Neuron labels written in file:', labels_file)

readfile = open(labels_file,'r')
label_test = readfile.readlines()

readfile.close()

#2d positions in interactome
# xs = []
# ys = []
# for node in chem_dic['nodes']:
#     xs.append(node['x'])
#     ys.append(node['y'])

# neurons = [80, 131, 157, 57, 153, 134, 266, 121, 113, 1]

# for n in neurons:
#     inst = chem_dic['nodes'][n]
#     print(inst['x'], ',',inst['y'], '#',inst['name'])
