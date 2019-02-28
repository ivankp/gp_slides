#!/usr/bin/env python

import math, sys, json
from gaussian_process import *
import numpy as np
from scipy import special

# https://apps.automeris.io/wpd/
with open('data.json') as f:
    data = json.load(f)
xs = data[sys.argv[1]]['x']
ys = data[sys.argv[1]]['y']
ts = np.linspace(*data[sys.argv[1]]['t']).tolist()

h = [ float(x) for x in sys.argv[3:] ]
us = [ h[0]**2 for x in xs ]

def kernel_se(a, b):
    return h[1]**2 * math.exp(-0.5*(((a-b)/h[2])**2))

def kernel_rq(a, b):
    return h[1]**2 * math.pow(1+(((a-b)/h[2])**2)/(2*h[3]), -h[3])

def kernel_mat(a, b):
    nu = h[3]
    r = math.sqrt(2*nu) * abs(a-b) / h[2]
    return h[1]**2 * ( math.pow(2,1-nu)/math.gamma(nu) ) \
         * math.pow(r,nu) * special.kn(nu,r)

kernels = {
    'se': kernel_se,
    'rq': kernel_rq,
    'mat': kernel_mat
}
hnames = {
    'se': [r'\ell'],
    'rq': [r'\ell',r'\alpha'],
    'mat': [r'\ell',r'\nu']
}
ker = sys.argv[2]
gp = gaussian_process(xs,ys,us,ts,kernels[ker])

print 'regression complete'

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.figure(num=None, figsize=(6.5, 4), dpi=200)
ax = plt.gca()
ax.fill_between(
    ts,
    [ m-u for m,u in gp ],
    [ m+u for m,u in gp ],
    color="#7777ff"
)
plt.plot(xs, ys, 'r.', ms=10)
plt.plot(ts, [ m for m,u in gp ], 'k-', lw=2)
# plt.axis([105,160,0,40])
plt.margins(x=0)

for i,x in enumerate(zip([r'\sigma_n',r'\sigma_s']+hnames[ker],h)):
    plt.text(0.03,0.92-0.08*i,'${} = ${:g}'.format(*x),
             transform = ax.transAxes, fontsize=16)

plt.savefig(
    '{}_{}.pdf'.format(
        '_'.join(sys.argv[1:3]),
        '_'.join(format(x,'g') for x in h)
    ),
    bbox_inches='tight'
)

