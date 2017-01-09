# !/usr/bin/python
# -*- coding: utf8 -*-

from prettytable import PrettyTable


class Command(object):

    def execute(self, graphic_editor, *args):
        """
        'Interface' method for every command to implement
        :param graphic_editor:
        :param args:
        :return:
        """
        raise NotImplementedError("Implement this method before using it")


class CreateMatrix(Command):

    @staticmethod
    def execute(graphic_editor, *args):
        """
        Creates a MxN Matrix
        :param graphic_editor:
        :param args:
        :return:
        """
        # Gather arguments
        columns = int(args[0])
        rows = int(args[1])

        graphic_editor.matrix = [[0 for _ in range(columns)] for _ in range(rows)]


class CleanMatrix(Command):

    @staticmethod
    def execute(graphic_editor, *args):
        """
        Cleans a given matrix with all values 0
        :param graphic_editor:
        :param args:
        :return:
        """
        graphic_editor.matrix = [[0 for _ in range(len(graphic_editor[0]))] for _ in range(len(graphic_editor))]


class PrintPixel(Command):

    @staticmethod
    def execute(graphic_editor, *args):
        """
        Prints only one print at (x, y)
        :param graphic_editor:
        :param args:
        :return:
        """
        # Gather arguments
        column = int(args[0]) - 1
        row = int(args[1]) - 1
        color = str(args[2]).upper()

        graphic_editor[row][column] = color


class PrintOnVertical(Command):

    @staticmethod
    def execute(graphic_editor, *args):
        """
        Prints a column within a given line range
        :param graphic_editor:
        :param args:
        :return:
        """
        # Gather arguments
        column = int(args[0]) - 1
        row_start = int(args[1])
        row_end = int(args[2])
        color = str(args[3]).upper()

        row_number = 0
        for _ in graphic_editor:
            if row_number + 1 in range(row_start, row_end + 1):
                graphic_editor[row_number][column] = color

            row_number += 1


class PrintOnHorizontal(Command):

    @staticmethod
    def execute(graphic_editor, *args):
        """
        Prints a line within a given column range
        :param graphic_editor:
        :param args:
        :return:
        """
        # Gather arguments
        column_start = int(args[0]) - 1
        column_end = int(args[1])
        row = int(args[2]) - 1
        color = str(args[3]).upper()

        graphic_editor[row][column_start:column_end] = [color for _ in range(column_start, column_end)]


class PrintRectangle(Command):

    @staticmethod
    def execute(graphic_editor, *args):
        """
        Prints a rectangle from the top-left (x1, y1) to the bottom-right (x2, y2)
        :param graphic_editor:
        :param args:
        :return:
        """
        # Gather arguments
        column_start = int(args[0]) - 1
        row_start = int(args[1]) - 1
        column_end = int(args[2])
        row_end = int(args[3])
        color = str(args[4]).upper()

        for row in range(row_start, row_end):
            graphic_editor[row][column_start:column_end] = [color for _ in range(column_start, column_end)]


class PrintOnRegion(Command):

    old_value = None
    color = None

    @classmethod
    def execute(cls, graphic_editor, *args):
        """
        Prints a given region following the rules inside 'instructions.txt'
        :param graphic_editor:
        :param args:
        :return:
        """
        # Gather arguments
        column = int(args[0]) - 1
        row = int(args[1]) - 1
        cls.color = str(args[2]).upper()

        cls.old_value = graphic_editor[row][column]
        graphic_editor.matrix = cls.print_recursively(graphic_editor.matrix, row, column)

    @classmethod
    def print_recursively(cls, matrix, x, y):
        """
        Recursive method for printing logic
        :param matrix:
        :param x:
        :param y:
        :return:
        """

        # If it's not equal the old color, return
        if matrix[x][y] != cls.old_value:
            return

        # Set the new color to current (x,y)
        matrix[x][y] = cls.color

        # Try to set the new color on clockwise direction
        try:
            up = matrix[x - 1][y]
            cls.print_recursively(matrix, x - 1, y)
        except IndexError:
            pass

        try:
            right = matrix[x][y + 1]
            cls.print_recursively(matrix, x, y + 1)
        except IndexError:
            pass

        try:
            down = matrix[x + 1][y]
            cls.print_recursively(matrix, x + 1, y)
        except IndexError:
            pass

        try:
            left = matrix[x][y - 1]
            cls.print_recursively(matrix, x, y - 1)
        except IndexError:
            pass

        return matrix


class WriteToFile(Command):

    @staticmethod
    def execute(graphic_editor, *args):
        """
        Writes matrix content to a file
        :param graphic_editor:
        :param args:
        :return:
        """
        # Gather arguments
        file_name = "{0}/{1}.txt".format("files", str(args[0]))

        fp = open(file_name, "wt")
        fp.write(str(graphic_editor))
        fp.close()


class QuitProgram(Command):

    @staticmethod
    def execute(graphic_editor, *args):
        """
        Finish program execution
        :param graphic_editor:
        :param args:
        :return:
        """
        print("Bye, bye!")
        exit()


class GraphicEditor(object):
    matrix = []

    COMMANDS = {
        "I": CreateMatrix,
        "C": CleanMatrix,
        "L": PrintPixel,
        "V": PrintOnVertical,
        "H": PrintOnHorizontal,
        "K": PrintRectangle,
        "F": PrintOnRegion,
        "S": WriteToFile,
        "X": QuitProgram
    }

    def __len__(self):
        return len(self.matrix)

    def __getitem__(self, position):
        return self.matrix[position]

    def __str__(self):
        table = PrettyTable()

        for row in self:
            table.add_row(row)

        return str(table)


def main():

    graphic_editor = GraphicEditor()

    while True:
        # Command input
        commands = input("Insert a valid command: ").split(" ")

        # Separate command and arguments
        command = str(commands[0]).upper()
        parameters = commands[1:]

        if command not in graphic_editor.COMMANDS.keys():
            continue

        # Execute command
        try:
            graphic_editor.COMMANDS[command].execute(graphic_editor, *parameters)
            print("Command successfully executed: \n{0}".format(graphic_editor))
        except IndexError:
            print("Invalid parameters list, try again!")

if __name__ == '__main__':
    main()
