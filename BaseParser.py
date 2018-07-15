"""
This is the parent class for different gcode parsers
It reads through a gcode file, keeping track of the machine state and performing certain actions to modify the code
"""


class BaseParser:

    def __init__(self, filename):
        self._filename = filename

        # Keep track of the state of cutting
        self._cutting = False

        # Track the position of the machine
        self.pos = (0, 0)

        # Track the current feed rate (speed)
        self._feedrate = 0

        # A dictionary representing the pieces of the current line being parsed
        self.current_line = {}

        # Keep a buffer of the lines to be re-written to the file when finished processing
        self.lines_buffer = []

    @property
    def cutting(self):
        return self._cutting

    @cutting.setter
    def cutting(self, value):
        if self._cutting is False and value is True:
            self._begin_cut()
        self._cutting = value

    @property
    def feedrate(self):
        return self._feedrate

    @feedrate.setter
    def feedrate(self, value):
        self._on_feed_change(value)
        self._feedrate = value

    def process_file(self):
        file = open(self._filename, "r")
        for line in file.readlines():
            self._process_line(line)

        # Write output to the same file, overwriting it
        self._write_changes(self._filename)

    def _process_line(self, line):
        segments = line.split(" ")

        # Create a dictionary for the current line with the command prefix as the keys (i.e. "G" -> 01, "F" -> 250)
        self.current_line = {segment[0]: float(segment[1:]) for segment in segments}

        # Iterate over command segments and update machine state
        for command, value in self.current_line.items():
            if command == "G":
                if value == 0:
                    self.cutting = False
                elif value == 1:
                    self.cutting = True
            elif command == "F":
                self.feedrate = value
            elif command == "X":
                self.pos = (value, self.pos[1])
            elif command == "Y":
                self.pos = (self.pos[0], value)

        # Put the line back together and re-write it with any changes that were made
        line = " ".join([k + str(v) for k, v in self.current_line.items()])
        self.lines_buffer.append(line)

    def _write_changes(self, output_filename):
        with open(output_filename, "w") as out_file:
            out_file.writelines(self.lines_buffer)

    def _begin_cut(self):
        pass

    def _on_feed_change(self, new_feed):
        pass


