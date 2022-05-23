from pylab import *
from tvb.simulator.lab import *
import threading
import numpy
import time
import sys
from matplotlib.tri import Triangulation
from matplotlib import pyplot as plt

def multiview(cortex, data, suptitle='', figsize=(15, 10), **kwds):

    cs = cortex
    vtx = cs.vertices
    tri = cs.triangles
    rm = cs.region_mapping
    x, y, z = vtx.T
    lh_tri = tri[(rm[tri] < 38).any(axis=1)]
    lh_vtx = vtx[rm < 38]
    lh_x, lh_y, lh_z = lh_vtx.T
    lh_tx, lh_ty, lh_tz = lh_vtx[lh_tri].mean(axis=1).T
    rh_tri = tri[(rm[tri] >= 38).any(axis=1)]
    rh_vtx = vtx[rm < 38]
    rh_x, rh_y, rh_z = rh_vtx.T
    rh_tx, rh_ty, rh_tz = vtx[rh_tri].mean(axis=1).T
    tx, ty, tz = vtx[tri].mean(axis=1).T

    views = {
        'lh-lateral': Triangulation(-x, z, lh_tri[argsort(lh_ty)[::-1]]),
        'lh-medial': Triangulation(x, z, lh_tri[argsort(lh_ty)]),
        'rh-medial': Triangulation(-x, z, rh_tri[argsort(rh_ty)[::-1]]),
        'rh-lateral': Triangulation(x, z, rh_tri[argsort(rh_ty)]),
        'both-superior': Triangulation(y, x, tri[argsort(tz)]),
    }

    def plotview(i, j, k, viewkey, z=None, zlim=None, zthresh=None, suptitle='', shaded=True, cmap=plt.cm.coolwarm, viewlabel=False):
        v = views[viewkey]
        ax = subplot(i, j, k)
        if z is None:
            z = rand(v.x.shape[0])
        if not viewlabel:
            axis('off')
        kwargs = {'shading': 'gouraud'} if shaded else {'edgecolors': 'k', 'linewidth': 0.1}
        if zthresh:
            z = z.copy() * (abs(z) > zthresh)
        tc = ax.tripcolor(v, z, cmap=cmap, **kwargs)
        if zlim:
            tc.set_clim(vmin=-zlim, vmax=zlim)
        ax.set_aspect('equal')
        if suptitle:
            ax.set_title(suptitle, fontsize=24)
        if viewlabel:
            xlabel(viewkey)

    figure(figsize=figsize)
    plotview(2, 3, 1, 'lh-lateral', data, **kwds)
    plotview(2, 3, 4, 'lh-medial', data, **kwds)
    plotview(2, 3, 3, 'rh-lateral', data, **kwds)
    plotview(2, 3, 6, 'rh-medial', data, **kwds)
    plotview(1, 3, 2, 'both-superior', data, suptitle=suptitle, **kwds)
    subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=1.0, wspace=0, hspace=0)
