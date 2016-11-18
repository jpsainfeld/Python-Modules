#!/usr/bin/env python

# ------------------------------------------------------------------------
# The redirectors below are used to capture output during testing.
# Output sent to sys.stdout and sys.stderr are automatically captured.
# However in some cases sys.stdout is already cached before our TestRunner is
# invoked (e.g. calling logging.basicConfig).
# In order to capture those  output, use the redirectors for the cached stream.
# ------------------------------------------------------------------------

## Object used to redirect the output to the specified stream
#  the function members are
#  write
#  writelines
#  flush
#
class OutputRedirector(object):
    """
        Wrapper to redirect stdout or stderr
        The redirectors below are used to capture output during testing.
        Output sent to sys.stdout and sys.stderr are automatically captured.
        However in some cases sys.stdout is already cached before our TestRunner is
        invoked (e.g. calling logging.basicConfig).
        In order to capture those  output, use the redirectors for the cached stream
    """
    def __init__(self, fp):
        """
            Constructor
        """
        self.fp = fp

    def write(self, s):
        """
            Write a string to the specified stream
        """
        self.fp.write(s)

    def writelines(self, lines):
        """
            Write a set of lines to the specified stream
        """
        self.fp.writelines(lines)

    def flush(self):
        """
            Flush the the stream
        """
        self.fp.flush()
