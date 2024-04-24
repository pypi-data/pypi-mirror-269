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
__date__ = "10/10/2020"


import datetime
import os

import numpy
from typing import Optional
from tomoscan.io import HDF5File


class MockBlissAcquisition:
    """

    :param n_sequence: number of sequence to create
    :param n_scan_per_sequence: number of scans (projection serie) per sequence
    :param n_projections_per_scan: number of projection frame in a scan
    :param n_darks: number of dark frame in the serie. Only one serie at the
                    beginning
    :param int n_flats: number of flats to create. In this case will only
                        create one serie of n flats after dark if any
    :param str output_dir: will contain the proposal file and one folder per
                           sequence.
    :param str acqui_type: acquisition type. Can be "basic", "zseries" or
                           "xrd-ct"
    :param Iterable z_values: if acqui_type is zseries then users should
                              provide the serie of values for z (one per stage)
    :param Optional[int] nb_loop: number of pcotomo loop for v1 of bliss pcotomo
    :param Optional[int] nb_tomo: number of tomo per loop for v1 of bliss pcotomo
    :param Optional[int] nb_turns: number of turns for v2 of bliss pcotomo ( <=> nb NXtomo to generate)
    :param str file_name_prefix: bliss file prefix name
    :param Optional[int] file_name_z_fill: optional z fill for the file name index. If None then file index will not be 'z filled'
    :param bool create_tomo_config: if True create the 'tomo_config' group under instrument which contains
                                    metadata describing the acquisition (which dataset to read for rotaiton, translation ...)
    """

    def __init__(
        self,
        n_sample,
        n_sequence,
        n_scan_per_sequence,
        n_darks,
        n_flats,
        output_dir,
        with_nx_detector_attr=True,
        detector_name="pcolinux",
        acqui_type="basic",
        z_values=None,
        y_rot=False,
        nb_loop=None,
        nb_tomo=None,
        nb_turns=None,
        with_rotation_motor_info=True,
        frame_data_type=numpy.uint16,
        file_name_prefix="sample",
        file_name_z_fill=None,
        create_tomo_config: bool = True,
        ebs_tomo_version: Optional[str] = None,
    ):
        self._n_darks = n_darks
        self._n_flats = n_flats
        self._n_scan_per_sequence = n_scan_per_sequence
        self.__folder = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.__proposal_file = os.path.join(self.__folder, "ihproposal_file.h5")
        if acqui_type not in ("pcotomo"):
            if nb_loop is not None or nb_tomo is not None:
                raise ValueError(
                    "nb_loop and nb_tomo are only handled by acqui_type: `pcotomo`"
                )
        else:
            if not (
                nb_turns is not None or (nb_loop is not None and nb_tomo is not None)
            ):
                raise ValueError(
                    "nb_turns should be provided or nb_loop and nb_tomo must be provided"
                )

        # create sample
        self.__samples = []
        for sample_i in range(n_sample):
            if file_name_z_fill is None:
                dir_name = f"{file_name_prefix}_{sample_i}"
            else:
                dir_name = f"{file_name_prefix}_{str(sample_i).zfill(file_name_z_fill)}"
            sample_dir = os.path.join(self.path, dir_name)
            os.mkdir(sample_dir)
            sample_file = os.path.join(sample_dir, dir_name + ".h5")
            if acqui_type == "basic":
                acqui_tomo = _BlissBasicTomo(
                    sample_dir=sample_dir,
                    sample_file=sample_file,
                    n_sequence=n_sequence,
                    n_scan_per_sequence=n_scan_per_sequence,
                    n_darks=n_darks,
                    n_flats=n_flats,
                    with_nx_detector_attr=with_nx_detector_attr,
                    detector_name=detector_name,
                    y_rot=y_rot,
                    with_rotation_motor_info=with_rotation_motor_info,
                    frame_data_type=frame_data_type,
                    create_tomo_config=create_tomo_config,
                    ebs_tomo_version=ebs_tomo_version,
                )
            elif acqui_type == "pcotomo":
                acqui_tomo = _BlissPCOTomo(
                    sample_dir=sample_dir,
                    sample_file=sample_file,
                    n_sequence=n_sequence,
                    n_scan_per_sequence=n_scan_per_sequence,
                    n_darks=n_darks,
                    n_flats=n_flats,
                    with_nx_detector_attr=with_nx_detector_attr,
                    detector_name=detector_name,
                    y_rot=y_rot,
                    with_rotation_motor_info=with_rotation_motor_info,
                    nb_loop=nb_loop,
                    nb_tomo=nb_tomo,
                    nb_turns=nb_turns,
                    frame_data_type=frame_data_type,
                    create_tomo_config=create_tomo_config,
                    ebs_tomo_version=ebs_tomo_version,
                )
            elif acqui_type == "zseries":
                if z_values is None:
                    raise ValueError("for zseries z_values should be provided")
                acqui_tomo = _BlissZseriesTomo(
                    sample_dir=sample_dir,
                    sample_file=sample_file,
                    n_sequence=n_sequence,
                    n_scan_per_sequence=n_scan_per_sequence,
                    n_darks=n_darks,
                    n_flats=n_flats,
                    with_nx_detector_attr=with_nx_detector_attr,
                    detector_name=detector_name,
                    z_values=z_values,
                    y_rot=y_rot,
                    with_rotation_motor_info=with_rotation_motor_info,
                    frame_data_type=frame_data_type,
                    create_tomo_config=create_tomo_config,
                    ebs_tomo_version=ebs_tomo_version,
                )
            elif acqui_type == "xrd-ct":
                acqui_tomo = _BlissXRD_CT(
                    sample_dir=sample_dir,
                    sample_file=sample_file,
                    n_sequence=n_sequence,
                    n_scan_per_sequence=n_scan_per_sequence,
                    n_darks=n_darks,
                    n_flats=n_flats,
                    with_nx_detector_attr=with_nx_detector_attr,
                    detector_name=detector_name,
                    y_rot=y_rot,
                    with_rotation_motor_info=with_rotation_motor_info,
                    frame_data_type=frame_data_type,
                    create_tomo_config=create_tomo_config,
                    ebs_tomo_version=ebs_tomo_version,
                )
            else:
                raise NotImplementedError("")
            self.__samples.append(acqui_tomo)

    @property
    def samples(self):
        return self.__samples

    @property
    def proposal_file(self):
        # for now a simple file
        return self.__proposal_file

    @property
    def path(self):
        return self.__folder


class _BlissSample:
    """
    Simple mock of a bliss sample. For now we only create the hierarchy of
    files.
    """

    def __init__(
        self,
        sample_dir,
        sample_file,
        n_sequence,
        n_scan_per_sequence,
        n_darks,
        n_flats,
        detector_name,
        with_nx_detector_attr=True,
        y_rot=False,
        with_rotation_motor_info=True,
        frame_data_type=numpy.uint16,
        create_tomo_config: bool = True,
        ebs_tomo_version: Optional[str] = None,
    ):
        self._with_nx_detector_attr = with_nx_detector_attr
        self._sample_dir = sample_dir
        self._sample_file = sample_file
        self._n_sequence = n_sequence
        self._n_scan_per_seq = n_scan_per_sequence
        self._n_darks = n_darks
        self._n_flats = n_flats
        self._scan_folders = []
        self._index = 1
        self._detector_name = detector_name
        self._det_width = 64
        self._det_height = 64
        self._tomo_n = 10
        self._energy = 19.0
        self._distance = 1.0
        self._pixel_size = (0.0065, 0.0066)
        self._y_rot = y_rot
        self._with_rotation_motor_info = with_rotation_motor_info
        self._frame_data_type = frame_data_type
        self._create_tomo_config = create_tomo_config
        self._ebs_tomo_version = ebs_tomo_version
        for _ in range(n_sequence):
            self.add_sequence()

    @property
    def frame_data_type(self):
        return self._frame_data_type

    def get_next_free_index(self):
        idx = self._index
        self._index += 1
        return idx

    def get_main_entry_title(self):
        raise NotImplementedError("Base class")

    @staticmethod
    def get_title(scan_type):
        if scan_type == "dark":
            return "dark images"
        elif scan_type == "flat":
            return "reference images 1"
        elif scan_type == "projection":
            return "projections 1 - 2000"
        else:
            raise ValueError("Not implemented")

    def create_entry_and_technique(self, seq_ini_index):
        # add sequence init information
        with HDF5File(self.sample_file, mode="a") as h5f:
            seq_node = h5f.require_group(str(seq_ini_index) + ".1")
            seq_node.attrs["NX_class"] = "NXentry"
            seq_node["title"] = self.get_main_entry_title()
            seq_node.require_group("instrument/positioners")
            # write energy
            seq_node["technique/scan/energy"] = self._energy
            seq_node["technique/scan/tomo_n"] = self._tomo_n * self._n_scan_per_seq
            seq_node["technique/scan/sample_detector_distance"] = self._distance
            seq_node["technique/detector/pixel_size"] = numpy.asarray(self._pixel_size)
            if self._y_rot:
                seq_node["instrument/positioners/yrot"] = 0.13
            seq_node["start_time"] = str(datetime.datetime.now())
            seq_node["end_time"] = str(
                datetime.datetime.now() + datetime.timedelta(minutes=10)
            )

    def register_scan_in_parent_seq(self, parent_index, scan_index):
        with HDF5File(self.sample_file, mode="a") as h5f:
            # write scan numbers
            seq_node = h5f.require_group(str(parent_index) + ".1")
            scan_number_node = seq_node.require_group("measurement/scan_numbers")
            if "data" in scan_number_node:
                res = list(scan_number_node["data"][()])
                del scan_number_node["data"]
            else:
                res = []
            res.append(scan_index)
            scan_number_node["data"] = res

    @staticmethod
    def get_next_group_name(seq_ini_index, scan_idx):
        return str(scan_idx) + ".1"

    def add_scan(
        self,
        scan_type,
        seq_ini_index,
        z_value,
        skip_title=False,
        nb_loop=None,
        nb_tomo=None,
        nb_turns=1,
    ):
        """
        :param int nb_loop: number of loop in pcotomo use case. Else must be 1
        :param int nb_tomo: number of tomography done in pcotomo 'per iteration' use case. Else must be 1
        """
        scan_idx = self.get_next_free_index()
        scan_name = str(scan_idx).zfill(4)
        scan_path = os.path.join(self.path, scan_name)
        self._scan_folders.append(_BlissScan(folder=scan_path, scan_type=scan_type))
        self.register_scan_in_parent_seq(
            parent_index=seq_ini_index, scan_index=scan_idx
        )
        if nb_turns is not None:
            nb_nxtomo = nb_turns
            if nb_tomo is not None or nb_loop is not None:
                raise ValueError(
                    "nb_tomo and nb_loop should be provided or nb_turns. Not both"
                )
        elif nb_loop is not None and nb_tomo is not None:
            nb_nxtomo = nb_loop * nb_tomo
            if nb_turns is not None:
                raise ValueError(
                    "nb_tomo and nb_loop should be provided or nb_turns. Not both"
                )
        else:
            raise ValueError(
                "nb_tomo and nb_loop should be provided or nb_turns. None provided"
            )
        # register the scan information
        with HDF5File(self.sample_file, mode="a") as h5f:
            seq_node = h5f.require_group(str(scan_idx) + ".1")
            # write title
            title = self.get_title(scan_type=scan_type)
            if not skip_title:
                seq_node["title"] = title
            # write data
            data = (
                numpy.random.random(
                    self._det_height * self._det_width * self._tomo_n * nb_nxtomo
                )
                * 256
            )
            n_frames = self._tomo_n * nb_nxtomo
            data = data.reshape(n_frames, self._det_height, self._det_width)
            data = data.astype(self.frame_data_type)
            det_path_1 = "/".join(("instrument", self._detector_name))
            det_grp = seq_node.require_group(det_path_1)
            det_grp["data"] = data
            if self._with_nx_detector_attr:
                det_grp.attrs["NX_class"] = "NXdetector"
            acq_grp = det_grp.require_group("acq_parameters")
            acq_grp["acq_expo_time"] = 4
            det_path_2 = "/".join(("technique", "scan", self._detector_name))
            seq_node[det_path_2] = data
            seq_node.attrs["NX_class"] = "NXentry"

            # write rotation angle value and translations
            instrument_group = seq_node.require_group("instrument")
            positioners_grp = instrument_group.require_group("positioners")
            positioners_grp["hrsrot"] = numpy.linspace(
                start=0.0, stop=360, num=n_frames
            )
            positioners_grp["sx"] = numpy.array(numpy.random.random(size=n_frames))
            positioners_grp["sy"] = numpy.random.random(size=n_frames)
            positioners_grp["sz"] = numpy.asarray([z_value] * n_frames)
            if self._with_rotation_motor_info:
                scan_node = seq_node.require_group("technique/scan")
                scan_node["motor"] = ("rotation", "hrsrot", "srot")

            if self._create_tomo_config:
                technique_group = seq_node.require_group("technique")
                tomo_config_group = technique_group.require_group("tomo_config")
                tomo_config_group["rotation"] = "hrsrot"
                tomo_config_group["detector"] = self._detector_name
                tomo_config_group["translation_x"] = "sx"
                tomo_config_group["translation_y"] = "sy"
                tomo_config_group["translation_z"] = "sz"

            if self._ebs_tomo_version is not None:
                technique_group = seq_node.require_group("technique")
                technique_group.attrs["tomo_version"] = self._ebs_tomo_version

    def add_sequence(self):
        """Add a sequence to the bliss file"""
        raise NotImplementedError("Base class")

    @property
    def path(self):
        return self._sample_dir

    @property
    def sample_directory(self):
        return self._sample_dir

    @property
    def sample_file(self):
        return self._sample_file

    def scans_folders(self):
        return self._scan_folders

    @property
    def n_darks(self):
        return self._n_darks

    @property
    def with_rotation_motor_info(self):
        return self._with_rotation_motor_info


class _BlissScan:
    """
    mock of a bliss scan
    """

    def __init__(self, folder, scan_type: str):
        assert scan_type in ("dark", "flat", "projection")
        self.__path = folder

    def path(self):
        return self.__path


class _BlissBasicTomo(_BlissSample):
    def get_main_entry_title(self):
        return "tomo:fullturn"

    def add_sequence(self):
        # reserve the index for the 'initialization' sequence. No scan folder
        # will be created for this one.
        seq_ini_index = self.get_next_free_index()

        self.create_entry_and_technique(seq_ini_index=seq_ini_index)

        if self.n_darks > 0:
            self.add_scan(scan_type="dark", seq_ini_index=seq_ini_index, z_value=1)

        if self._n_flats > 0:
            self.add_scan(scan_type="flat", seq_ini_index=seq_ini_index, z_value=1)

        for _ in range(self._n_scan_per_seq):
            self.add_scan(
                scan_type="projection", seq_ini_index=seq_ini_index, z_value=1
            )


class _BlissPCOTomo(_BlissSample):
    def __init__(
        self,
        sample_dir,
        sample_file,
        n_sequence,
        n_scan_per_sequence,
        n_darks,
        n_flats,
        detector_name,
        with_nx_detector_attr=True,
        y_rot=False,
        with_rotation_motor_info=True,
        nb_loop=None,
        nb_tomo=None,
        nb_turns=1,
        frame_data_type=numpy.uint16,
        create_tomo_config: bool = True,
        ebs_tomo_version=None,
    ):
        self.nb_loop = nb_loop
        self.nb_tomo = nb_tomo
        self.nb_turns = nb_turns
        super().__init__(
            sample_dir,
            sample_file,
            n_sequence,
            n_scan_per_sequence,
            n_darks,
            n_flats,
            detector_name,
            with_nx_detector_attr,
            y_rot,
            with_rotation_motor_info=with_rotation_motor_info,
            frame_data_type=frame_data_type,
            create_tomo_config=create_tomo_config,
            ebs_tomo_version=ebs_tomo_version,
        )
        if nb_loop is not None and nb_tomo is not None:
            if nb_turns is not None:
                raise ValueError(
                    "All of nb_loop, nb_tomo and nb_turns provided. Unable to deduce the pcotomo version"
                )
            pcotomo_version = 1
        elif nb_turns is not None:
            pcotomo_version = 2
        else:
            pcotomo_version = None
        if pcotomo_version is not None:
            # write Bliss version in attrs
            with HDF5File(self.sample_file, mode="a") as h5f:
                if "creator_version" not in h5f.attrs:
                    if pcotomo_version == 1:
                        h5f.attrs["creator_version"] = "1.2.3"
                    if pcotomo_version == 2:
                        h5f.attrs["creator_version"] = "1.10.0"

    def get_main_entry_title(self):
        return "tomo:pcotomo"

    def add_sequence(self):
        # reserve the index for the 'initialization' sequence. No scan folder
        # will be created for this one.
        seq_ini_index = self.get_next_free_index()

        self.create_entry_and_technique(seq_ini_index=seq_ini_index)

        # start dark
        if self.n_darks > 0:
            self.add_scan(scan_type="dark", seq_ini_index=seq_ini_index, z_value=1)

        # start flat
        if self._n_flats > 0:
            self.add_scan(scan_type="flat", seq_ini_index=seq_ini_index, z_value=1)

        for _ in range(self._n_scan_per_seq):
            self.add_scan(
                scan_type="projection",
                seq_ini_index=seq_ini_index,
                z_value=1,
                nb_loop=self.nb_loop,
                nb_tomo=self.nb_tomo,
                nb_turns=self.nb_turns,
            )

        # end flat
        if self._n_flats > 0:
            self.add_scan(scan_type="flat", seq_ini_index=seq_ini_index, z_value=1)

    def add_scan(
        self,
        scan_type,
        seq_ini_index,
        z_value,
        skip_title=False,
        nb_loop=None,
        nb_tomo=None,
        nb_turns=1,
    ):
        super().add_scan(
            scan_type, seq_ini_index, z_value, skip_title, nb_loop, nb_tomo, nb_turns
        )
        if scan_type == "projection":
            # register pcotomo specific informations (only for projections)
            with HDF5File(self.sample_file, mode="a") as h5f:
                seq_node = h5f.require_group(str(self._index - 1) + ".1")

                scan_grp = seq_node.require_group("technique/proj")
                if nb_loop is not None and "nb_loop" not in scan_grp:
                    scan_grp["nb_loop"] = nb_loop
                if nb_tomo is not None and "nb_tomo" not in scan_grp:
                    scan_grp["nb_tomo"] = nb_tomo
                if nb_turns is not None and "nb_turns" not in scan_grp:
                    scan_grp["nb_turns"] = nb_turns
                if "tomo_n" not in scan_grp:
                    scan_grp["tomo_n"] = self._tomo_n


class _BlissZseriesTomo(_BlissSample):
    def __init__(
        self,
        sample_dir,
        sample_file,
        n_sequence,
        n_scan_per_sequence,
        n_darks,
        n_flats,
        detector_name,
        z_values,
        with_nx_detector_attr=True,
        y_rot=False,
        with_rotation_motor_info=True,
        frame_data_type=numpy.uint16,
        create_tomo_config: bool = True,
        ebs_tomo_version=None,
    ):
        self._z_values = z_values
        super().__init__(
            sample_dir=sample_dir,
            sample_file=sample_file,
            n_sequence=n_sequence,
            n_scan_per_sequence=n_scan_per_sequence,
            n_darks=n_darks,
            n_flats=n_flats,
            detector_name=detector_name,
            with_nx_detector_attr=with_nx_detector_attr,
            y_rot=y_rot,
            with_rotation_motor_info=with_rotation_motor_info,
            frame_data_type=frame_data_type,
            create_tomo_config=create_tomo_config,
            ebs_tomo_version=ebs_tomo_version,
        )

    def get_main_entry_title(self):
        return "tomo:zseries"

    def add_sequence(self):
        # reserve the index for the 'initialization' sequence. No scan folder
        # will be created for this one.
        seq_ini_index = self.get_next_free_index()

        self.create_entry_and_technique(seq_ini_index=seq_ini_index)

        for z_value in self._z_values:
            if self.n_darks > 0:
                self.add_scan(
                    scan_type="dark", seq_ini_index=seq_ini_index, z_value=z_value
                )

            if self._n_flats > 0:
                self.add_scan(
                    scan_type="flat", seq_ini_index=seq_ini_index, z_value=z_value
                )

            for i_proj_seq in range(self._n_scan_per_seq):
                self.add_scan(
                    scan_type="projection", seq_ini_index=seq_ini_index, z_value=z_value
                )


class _BlissXRD_CT(_BlissSample):
    def __init__(
        self,
        sample_dir,
        sample_file,
        n_sequence,
        n_scan_per_sequence,
        n_darks,
        n_flats,
        detector_name,
        with_nx_detector_attr=True,
        y_rot=False,
        with_rotation_motor_info=True,
        frame_data_type=numpy.uint16,
        create_tomo_config: bool = True,
        ebs_tomo_version=None,
    ):
        """XRD-CT are scan with only projection. Projections are store in
        the init group. Data can be store under 1.1 but also 1.2..."""
        super().__init__(
            sample_dir=sample_dir,
            sample_file=sample_file,
            n_sequence=n_sequence,
            n_scan_per_sequence=n_scan_per_sequence,
            n_darks=n_darks,
            n_flats=n_flats,
            detector_name=detector_name,
            with_nx_detector_attr=with_nx_detector_attr,
            y_rot=y_rot,
            with_rotation_motor_info=with_rotation_motor_info,
            frame_data_type=frame_data_type,
            create_tomo_config=create_tomo_config,
            ebs_tomo_version=ebs_tomo_version,
        )

    def get_main_entry_title(self):
        return "aeroystepscan hrrz hry"

    def add_sequence(self):
        # reserve the index for the 'initialization' sequence. No scan folder
        # will be created for this one.
        seq_ini_index = self.get_next_free_index()
        self.create_entry_and_technique(seq_ini_index=seq_ini_index)

    def create_entry_and_technique(self, seq_ini_index):
        super().create_entry_and_technique(seq_ini_index=seq_ini_index)
        self._index = 1
        self.add_scan(
            scan_type="projection",
            seq_ini_index=seq_ini_index,
            z_value=1,
            skip_title=True,
        )
        self.add_diode(
            seq_ini_index=seq_ini_index,
        )

    def register_scan_in_parent_seq(self, parent_index, scan_index):
        pass

    def add_diode(self, seq_ini_index):
        scan_idx = str(seq_ini_index) + ".2"
        scan_name = str(scan_idx)

        with HDF5File(self.sample_file, mode="a") as h5f:
            scan_node = h5f.require_group(scan_name)
            scan_node.attrs["NX_class"] = "NXentry"

            measrurement_node = h5f.require_group("/".join((scan_name, "measurement")))
            data = numpy.random.random(self._tomo_n) * 256.2
            measrurement_node["fpico3"] = data
            h5f.require_group(scan_name)["title"] = self.get_main_entry_title()
            instrument_node = h5f.require_group("/".join((scan_name, "instrument")))
            fpico3_node = instrument_node.require_group("fpico3")
            fpico3_node.attrs["NX_class"] = "NXdetector"
            fpico3_node["data"] = data

    @staticmethod
    def get_next_group_name(seq_ini_index, scan_idx):
        return f"{seq_ini_index}.{scan_idx}"
