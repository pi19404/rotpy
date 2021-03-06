""" 
pyrotate.angles
===============

Rotations defined by Euler angles.

There should be a python interface to a more optimized C version of this

Euler angles are intuitive because they are the first rotation representation
introduced to many people. They have several deficiencies, but they are here
to stay. Try not to use Euler angles for internal representation of rotations. 
Feel free to use them for communicating and plotting, but be sure to document
the convention you use!

"""

import numpy as np

_axes_string_to_tuple = {
    'xyz': (1,2,3), 'ijk': (1,2,3),
    'zyx': (3,2,1), 'kji': (3,2,1),
}

# default should be SNAME HPR order
# use intrinsic/extrinsic flag to differentiate body/fixed axes
def to_matrix(angles, axes = (3, 2, 1), intrinsic=True,):
    if intrinsic:
        return _to_matrix_intrinsic(angles, axes) 
        # this allows me to avoid evaluating the if statement (speedup?)
# XXX if you are really looking for the speedup, you should use the c library
    else:
        raise NotImplementedError

    
def _to_matrix_intrinsic(angles, axes = (3, 2, 1)):
    
    Rlist = [_to_matrix_about_elemental_axis(*aa) 
             for aa in reversed(zip(angles, axes))]
#    Rlist.reverse() #XXX need to reverse the Rlist to apply in correct order
    return reduce(np.dot, Rlist)


#TODO better terminology than elemental_axis
def _to_matrix_about_elemental_axis(angle, axis):
    #TODO pythonic implementation below
    if axis in [1, 'i', 'x']: return _to_matrix_about_i(angle)
    elif axis in [2, 'j', 'y']: return _to_matrix_about_j(angle)
    elif axis in [3, 'k', 'z']: return _to_matrix_about_k(angle)
    else: print 'axis ', axis, 'unknown'
        #TODO raise an error


def _to_matrix_about_i(angle):
    s, c = np.sin(angle), np.cos(angle)
    return np.array([[1, 0, 0],[0, c, s],[0, -s, c]]) # e.g. roll


def _to_matrix_about_j(angle):
    s, c = np.sin(angle), np.cos(angle)
    return np.array([[c, 0, -s],[0, 1, 0],[s, 0, c]]) # e.g. pitch


def _to_matrix_about_k(angle):
    s, c = np.sin(angle), np.cos(angle)
    return np.array([[c, s, 0],[-s, c, 0],[0, 0, 1]]) # e.g. heading


def to_axis_angle(angles, order='xyz', intrinsic=True, ):
    raise NotImplementedError


def to_quaternion(angles, order='xyz', intrinsic=True,):
    raise NotImplementedError


