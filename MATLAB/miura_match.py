#This is the matching procedure described by Miura et al. in their paper.
#A small difference is that this matching function calculates the match 
#ratio instead of the mismatch ratio.

#Parameters:
# I  - Input image
# R  - Registered template image
# cw - Maximum search displacement in x-direction
# ch - Maximum search displacement in y-direction

#Returns:
# score - Value between 0 and 0.5, larger value is better match

#Reference:
#Feature extraction of finger vein patterns based on iterative line 
#   tracking and its application to personal identification
#N. Miura, A. Nagasaka, and T. Miyatake
#Syst. Comput. Japan 35 (7 June 2004), pp. 61--71
#doi: 10.1002/scj.v35:7

#Author:  Bram Ton <b.t.ton@alumnus.utwente.nl>
#Date:    20th December 2011
#License: Simplified BSD License

import numpy as np
import scipy

def miura_match(I, R, cw, ch):

    [h, w] = R.shape #Get height and width of registered data

    #Determine value of match, just cross-correlation
    crop_R = R[ch:h-ch, cw:w-cw]
    Nm = scipy.signal.fftconvolve(I, np.rot90(crop_R, k=2), 'valid')

    # #Maximum value of match
    # [Nmm,mi] = max(Nm(:)); #(what about multiple maximum values ?)
    # [t0,s0] = ind2sub(size(Nm),mi);
    t0, s0 = np.unravel_index(Nm.argmax(), Nm.shape)
    Nmm = Nm[t0,s0]

    # Normalize
    score = Nmm/(sum(sum(crop_R)) + sum(sum(I[t0:t0+h-2*ch-1, s0:s0+w-2*cw-1])))
            # Nmm/(sum(sum(crop_R)) + sum(sum(I[t0:t0+h-2*ch-1, s0:s0+w-2*cw-1])))
            # Nmm/(crop_R.sum() + I[t0:t0+h-2*ch, s0:s0+w-2*cw].sum())
    return score
    


