"""Utilities for daily_programmer
"""
import json
import os


class JSONFileManager(object):
    """Manages the lifetime of a JSON file

    create - If file doesn't exist, create it
    default - default value to which object should be initialized ({} by default)
    """
    def __init__(self, fname, create=True, default=None):
        self.fname = fname
        if not os.path.exists(self.fname):
            if create:
                self.obj = default if default is not None else {}
                self.dump()
            else:
                raise OSError('Unable to load file at %s', self.fname)
        else:
            self.obj = self._load()

    def dump(self):
        """Dump the current object back to the json file
        """
        with open(self.fname, 'w') as json_file:
            json.dump(self.obj, json_file, sort_keys=True, indent=4)

    def _load(self):
        """Return the JSON object in the file at `fname`
        """
        with open(self.fname, 'r') as json_file:
            return json.load(json_file)
