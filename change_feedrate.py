"""
Update a gcode file to change the overall feedrate
"""
from BaseParser import BaseParser
import argparse


class FeedParser(BaseParser):

    def __init__(self, filename, new_feedrate):
        self._override_feed = new_feedrate

        super().__init__(filename)

    def _on_feed_change(self, new_feed):
        if self.current_line["G"] == 1:
            self.current_line["F"] = self._override_feed


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--filename", dest='filename', type=str, required=True, help="Gcode file to change")
    arg_parser.add_argument("--feedrate", dest='feedrate', type=int, required=True, help="New feedrate for cuts")

    args = arg_parser.parse_args()

    file_parser = FeedParser(filename=args.filename, new_feedrate=args.feedrate)

    file_parser.process_file()
