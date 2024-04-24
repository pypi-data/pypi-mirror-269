# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "02/06/2021"


from datetime import datetime

import numpy.random
from tomoscan.io import HDF5File


class MockDxFile:
    """
    Mock DXFile
    """

    def __init__(
        self,
        file_path,
        n_projection,
        n_darks,
        n_flats,
        det_height=128,
        det_width=128,
        data_path="/",
    ):
        self._file_path = file_path
        self._n_projection = n_projection
        self._n_darks = n_darks
        self._n_flats = n_flats
        self._det_height = det_height
        self._det_width = det_width
        self._n_projection = n_projection
        self.data_flat = None
        self.data_proj = None
        self.data_dark = None

        with HDF5File(file_path, mode="w") as h5f:
            root_grp = h5f.require_group(data_path)
            exchange_grp = root_grp.require_group("exchange")
            # create data
            self.data_proj = self._create_random_frames(self._n_projection)
            exchange_grp["data"] = self.data_proj
            # create data_dark
            if self._n_darks > 0:
                self.data_dark = self._create_random_frames(self._n_darks)
                exchange_grp["data_dark"] = self.data_dark
            # create data_white
            if self._n_flats > 0:
                self.data_flat = self._create_random_frames(self._n_flats)
                exchange_grp["data_white"] = self.data_flat
            root_grp["file_creation_datetime"] = str(datetime.now())
            # for now some information are not mock and used like
            # exposure_period, x_binning, roi... did not had a concrete
            # example about it

    def _create_random_frames(self, n_frames):
        data = numpy.random.random(self._det_height * self._det_width * n_frames) * 256
        data = data.astype(numpy.uint16)
        return data.reshape((n_frames, self._det_height, self._det_width))
