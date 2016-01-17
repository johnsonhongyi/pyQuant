import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path


def main():
    ax = plt.subplot(111)
    verts = np.array([(0., 0.), (0.5, .5), (1., 0.8), (0.8, 0.)])
    codes = np.array([Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.LINETO])

    # Can this curve have zoomable width
    path = Path(verts, codes)
    patch = patches.PathPatch(path, fc='none', color='r', lw=4, zorder=3)
    ax.add_patch(patch)

    ax.plot(verts[:, 0], verts[:, 1], 'o--', lw=2, color='k', zorder=2)

    # these will be polygonal approx that will have proper zoom
    v = np.array([]).reshape((-1, 2))
    c = []
    for i in range(len(verts) - 1):
        vtmp, ctmp = line2poly(verts[[i, i + 1], :], 0.03)
        v = np.vstack((v, vtmp))
        c = np.concatenate((c, ctmp))
    path_zoom = Path(v, c)
    patch_zoom = patches.PathPatch(path_zoom, fc='r', ec='k', zorder=1, alpha=0.4)
    ax.add_patch(patch_zoom)

    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.1)
    plt.show()


def line2poly(line, width):
    dx, dy = np.hstack(np.diff(line, axis=0)).tolist()
    theta = np.arctan2(dy, dx)
    print(np.hstack(np.diff(line, axis=0)).tolist())
    print(np.degrees(theta))
    s = width / 2 * np.sin(theta)
    c = width / 2 * np.cos(theta)
    trans = np.array([(-s, c), (s, -c), (s, -c), (-s, c)])

    verts = line[[0, 0, 1, 1], :] + trans
    verts = np.vstack((verts, verts[0, :]))
    codes = np.array([Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY])
    return verts, codes


if __name__ == '__main__':
    main()
