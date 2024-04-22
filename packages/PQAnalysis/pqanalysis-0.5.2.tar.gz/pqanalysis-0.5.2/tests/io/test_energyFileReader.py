import pytest
import numpy as np

from collections import defaultdict

from PQAnalysis.io import EnergyFileReader, InfoFileReader
from PQAnalysis.traj import MDEngineFormat
from PQAnalysis.traj.exceptions import MDEngineFormatError


class TestEnergyReader:
    @pytest.mark.parametrize("example_dir", ["readEnergyFile"], indirect=False)
    def test__init__(self, test_with_data_dir):
        with pytest.raises(FileNotFoundError) as exception:
            EnergyFileReader("tmp")
        assert str(exception.value) == "File tmp not found."

        reader = EnergyFileReader("md-01.en")
        assert reader.filename == "md-01.en"
        assert reader.info_filename == "md-01.info"
        assert reader.withInfoFile == True
        assert reader.format == MDEngineFormat.PIMD_QMCF

        reader = EnergyFileReader("md-01.en", use_info_file=False)
        assert reader.filename == "md-01.en"
        assert reader.info_filename == None
        assert reader.withInfoFile == False
        assert reader.format == MDEngineFormat.PIMD_QMCF

        reader = EnergyFileReader("md-01_noinfo.en")
        assert reader.filename == "md-01_noinfo.en"
        assert reader.info_filename == None
        assert reader.withInfoFile == False
        assert reader.format == MDEngineFormat.PIMD_QMCF

        with pytest.raises(FileNotFoundError) as exception:
            EnergyFileReader(
                "md-01_noinfo.en", info_filename="md-01_noinfo.info", use_info_file=True)
        assert str(
            exception.value) == "Info File md-01_noinfo.info not found."

        reader = EnergyFileReader(
            "md-01_noinfo.en", info_filename="md-01.info")
        assert reader.filename == "md-01_noinfo.en"
        assert reader.info_filename == "md-01.info"
        assert reader.withInfoFile == True
        assert reader.format == MDEngineFormat.PIMD_QMCF

        reader = EnergyFileReader("md-01.en", format="qmcfc")
        assert reader.filename == "md-01.en"
        assert reader.info_filename == "md-01.info"
        assert reader.withInfoFile == True
        assert reader.format == MDEngineFormat.QMCFC

        with pytest.raises(MDEngineFormatError) as exception:
            EnergyFileReader("md-01.en", format="tmp")
        assert str(
            exception.value) == f"""
'tmp' is not a valid MDEngineFormat.
Possible values are: {MDEngineFormat.member_repr()}
or their case insensitive string representation: {MDEngineFormat.value_repr()}"""

    @pytest.mark.parametrize("example_dir", ["readEnergyFile"], indirect=False)
    def test__info_file_found__(self, test_with_data_dir):
        reader = EnergyFileReader("md-01.en")
        assert reader.__info_file_found__() == True

        reader = EnergyFileReader("md-01_noinfo.en")
        assert reader.__info_file_found__() == False

        reader = EnergyFileReader(
            "md-01_noinfo.en", info_filename="md-01.info")
        assert reader.__info_file_found__() == True

        with pytest.raises(FileNotFoundError) as exception:
            EnergyFileReader(
                "md-01_noinfo.en", info_filename="md-01_noinfo.info", use_info_file=True)
        assert str(exception.value) == "Info File md-01_noinfo.info not found."

    @pytest.mark.parametrize("example_dir", ["readEnergyFile"], indirect=False)
    def test_read(self, test_with_data_dir):
        data_ref = np.array([[1.00000000e+00,  2.00000000e+00],
                             [2.98066020e+02,  2.98442926e+02],
                             [2.32566666e+04,  2.39839997e+04],
                             [-1.85898221e+05, -
                              1.85719252e+05],
                             [-1.85903822e+05, -
                              1.86024132e+05],
                             [0.00000000e+00,  0.00000000e+00],
                             [5.60049937e+00,  3.04879280e+02],
                             [0.00000000e+00,  0.00000000e+00],
                             [3.72913867e+03,  3.72146189e+03],
                             [8.34545285e-01,  8.34545285e-01],
                             [1.12687000e-16,  5.63381000e-17],
                             [1.07571000e+00,  9.97330000e-01]])

        infoFileReader = InfoFileReader("md-01.info")
        info, units = infoFileReader.read()

        reader = EnergyFileReader("md-01.en")
        energy = reader.read()

        assert energy.data.shape == (12, 2)
        assert np.allclose(energy.data, data_ref)
        assert energy.info == info
        assert energy.units == units
        assert energy.info_given == True
        assert energy.units_given == True

        reader = EnergyFileReader("md-01_noinfo.en")
        energy = reader.read()
        assert np.allclose(energy.data, data_ref)
        assert energy.info == defaultdict(lambda: None)
        assert energy.units == defaultdict(lambda: None)
        assert energy.info_given == False
        assert energy.units_given == False
