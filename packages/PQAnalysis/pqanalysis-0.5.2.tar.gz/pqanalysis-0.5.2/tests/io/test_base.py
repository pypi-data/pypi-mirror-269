import pytest
import os
import sys

from PQAnalysis.io import BaseWriter, BaseReader


class TestBaseWriter:

    @pytest.mark.usefixtures("tmpdir")
    def test__init__(self):

        filename = "tmp"

        with pytest.raises(ValueError) as exception:
            BaseWriter(filename, "r")
        assert str(
            exception.value) == "Invalid mode - has to be either \'w\' or \'a\'."

        open(filename, "w")

        with pytest.raises(ValueError) as exception:
            BaseWriter(filename, "w")
        assert str(
            exception.value) == "File tmp already exists. Use mode \'a\' to append to file."

        writer = BaseWriter(filename, "a")
        assert writer.file is None
        assert writer.mode == "a"
        assert writer.filename == filename

        os.remove(filename)

        writer = BaseWriter(filename, "w")
        assert writer.file is None
        assert writer.mode == "a"
        assert writer.filename == filename

        writer = BaseWriter()
        assert writer.file == sys.stdout
        assert writer.mode == "a"
        assert writer.filename is None

    @pytest.mark.usefixtures("tmpdir")
    def test_open(self):

        filename = "tmp"

        writer = BaseWriter(filename, "a")
        assert writer.file is None

        writer.open()
        assert writer.file is not None

        os.remove(filename)

        writer = BaseWriter(filename, "w")
        assert writer.file is None

        writer.open()
        assert writer.file is not None

    @pytest.mark.usefixtures("tmpdir")
    def test_close(self):

        filename = "tmp"

        writer = BaseWriter(filename, "a")
        assert writer.file is None

        writer.open()
        assert writer.file is not None

        writer.close()
        assert writer.file is None


class TestBaseReader:
    @pytest.mark.usefixtures("tmpdir")
    def test__init__(self):
        with pytest.raises(FileNotFoundError) as exception:
            BaseReader("tmp")
        assert str(exception.value) == "File tmp not found."

        filename = "tmp"
        file = open(filename, "w")
        print("test", file=file)
        file.close()

        reader = BaseReader(filename)
        assert reader.filename == filename
        assert reader.multiple_files is False

        with pytest.raises(FileNotFoundError) as exception:
            BaseReader([filename, "tmp2"])
        assert str(
            exception.value) == "At least one of the given files does not exist. File tmp2 not found."

        filename2 = "tmp2"
        file = open(filename2, "w")
        print("test2", file=file)
        file.close()

        reader = BaseReader([filename, filename2])
        assert reader.filenames == [filename, filename2]
        assert reader.multiple_files is True
