# SPDX-FileCopyrightText: Copyright 2022, Siavash Ameli <sameli@berkeley.edu>
# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileType: SOURCE
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the license found in the LICENSE.txt file in the root directory
# of this source tree.


# =======
# Imports
# =======

import numpy
import scipy

__all__ = ['sy_logdet']


# =========
# sy logdet
# =========

def sy_logdet(
        A,
        sym_pos=False,
        overwrite_A=False):
    """
    Implementation of `logdet` function using scipy.
    """

    if sym_pos:
        L = scipy.linalg.cholesky(A, lower=True, overwrite_a=overwrite_A,
                                  check_finite=False)
        diag_L = numpy.diag(L).astype(numpy.complex128)
        logdet_L = numpy.real(numpy.sum(numpy.log(diag_L)))
        ld = 2.0*logdet_L
        sign = 1

    else:
        lu, piv = scipy.linalg.lu_factor(A, overwrite_a=overwrite_A,
                                         check_finite=False)
        diag_lu = numpy.diag(lu)
        ld = numpy.sum(numpy.log(numpy.abs(diag_lu)))
        sign = numpy.prod(numpy.sign(diag_lu))

    return ld, sign
