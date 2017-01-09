# !/usr/bin/python
# -*- coding: utf8 -*-

import os
from app.graphic_editor import GraphicEditor, CreateMatrix, CleanMatrix, PrintPixel, PrintOnVertical, \
    PrintOnHorizontal, PrintRectangle, PrintOnRegion, WriteToFile


class TestGraphicEditor:
    graphic_editor = None

    def setup(self):
        """
        Test setup method
        :return:
        """
        self.graphic_editor = GraphicEditor()
        CreateMatrix.execute(self.graphic_editor, 10, 9)

    def test_create_matrix(self):
        """
        Tests logic of CreateMatrix command
        :return:
        """
        CreateMatrix.execute(self.graphic_editor, 5, 4)

        # Validates matrix size
        assert len(self.graphic_editor) == 4
        assert len(self.graphic_editor.matrix[0]) == 5

        # Validates a demonstration value as zero
        assert self.graphic_editor[0][0] == 0

    def test_clean_matrix(self):
        """
        Tests logic of CleanMatrix command
        :return:
        """
        CleanMatrix.execute(self.graphic_editor)

        # Same size as before
        assert len(self.graphic_editor) == 9
        assert len(self.graphic_editor.matrix[0]) == 10

        # Validates all values as zero
        for row in range(len(self.graphic_editor)):
            for column in range(len(self.graphic_editor.matrix[0])):
                if self.graphic_editor[row][column] != 0:
                    assert False

    def test_print_pixel(self):
        """
        Tests logic of PrintPixel command
        :return:
        """
        PrintPixel.execute(self.graphic_editor, 3, 3, "X")

        assert self.graphic_editor[2][2] == "X"

    def test_print_on_vertical(self):
        """
        Tests logic of PrintOnVertical command
        :return:
        """
        PrintOnVertical.execute(self.graphic_editor, 10, 2, 8, "Y")

        for row in range(len(self.graphic_editor)):
            # Row out of range
            if row not in range(1, 8):
                assert self.graphic_editor[row] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                continue

            # Last column is printed
            assert self.graphic_editor[row] == [0, 0, 0, 0, 0, 0, 0, 0, 0, "Y"]

    def test_print_on_horizontal(self):
        """
        Tests logic of PrintOnHorizontal command
        :return:
        """
        PrintOnHorizontal.execute(self.graphic_editor, 2, 8, 9, "Z")

        for row in range(9):
            # Printed row
            if row == 8:
                assert self.graphic_editor[row] == [0, "Z", "Z", "Z", "Z", "Z", "Z", "Z", 0, 0]
            else:
                assert self.graphic_editor[row] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def test_print_rectangle(self):
        """
        Tests logic of PrintRectangle command
        :return:
        """
        PrintRectangle.execute(self.graphic_editor, 1, 1, 3, 3, "R")

        for row in range(len(self.graphic_editor)):
            # First three rows will be printed
            if row in range(0, 3):
                assert self.graphic_editor[row] == ["R", "R", "R", 0, 0, 0, 0, 0, 0, 0]
            else:
                assert self.graphic_editor[row] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def test_print_on_region(self):
        """
        Tests logic of PrintOnRegion command
        :return:
        """
        # Line 5 from columns 4 to 7 will be printed "X"
        PrintOnHorizontal.execute(self.graphic_editor, 4, 7, 5, "X")
        # Print region of item (5, 5) with value "R"
        PrintOnRegion.execute(self.graphic_editor, 5, 5, "R")

        # Only items on the 5th line should be printed as "R"
        for row in range(len(self.graphic_editor)):
            # Printed row
            if row == 4:
                assert self.graphic_editor[row] == [0, 0, 0, "R", "R", "R", "R", 0, 0, 0]
            else:
                assert self.graphic_editor[row] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def test_write_to_file(self):
        """
        Tests logic of WriteToFile command
        :return:
        """
        file_name = "text"
        file_path = "files/{0}.txt".format(file_name)

        CreateMatrix.execute(self.graphic_editor, 10, 9)
        WriteToFile.execute(self.graphic_editor, file_name)

        # Validates file content
        with open(file_path) as f:
            rows = f.readlines()
            assert rows is not None

        # Delete test file
        os.remove(file_path)
