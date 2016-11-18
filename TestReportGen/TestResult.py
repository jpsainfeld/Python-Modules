#!/usr/bin/env python

import unittest
import OutputRedirector
import sys
import io
import logging


TestResult = unittest.TestResult
stdout_redirector = OutputRedirector.OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector.OutputRedirector(sys.stderr)

class _TestResult(TestResult):
    """
    _TestResult is a pure representation of results.
    It lacks the output and reporting ability compares to unittest._TextTestResult.
    """
    ## Constructor
    # As a wrapper objet
    # @param verbosity:
    #
    def __init__(self, verbosity=1):


        # invoke the constructor or the base class
        TestResult.__init__(self)
        ## A location to save the stdout
        self.stdout0 = None
        ## A location to save the stderr
        self.stderr0 = None

        # statistic counter
        # for sucess, failure, error

        ## Number of Successes
        self.success_count = 0

        ## Number of Failures
        self.failure_count = 0

        ## Number of Errors
        self.error_count = 0

        ## level of verbosisty passed as arg  but default to level=1
        self.verbosity = verbosity

        ## result is a list of result in 4 tuple
        # (
        #   result code (0: success; 1: fail; 2: error),
        #   TestCase object,
        #   Test output (byte string),
        #   stack trace,
        # )
        self.result = []
        self.logger = logging.getLogger(__name__)
        self.logger.debug('TestResult')
        return

    ## startTest
    # this member function is invoked at the start of the specified test
    # This function is a wrapper around the base class
    # TestResult.startTest function
    # The  output is redirected appropriately in such a way that
    # stdout and stderr are using the same buffer
    #
    # @param test: The test to execute

    def startTest(self, test):

        TestResult.startTest(self, test)
        # just one buffer for both stdout and stderr
        self.outputBuffer = io.StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer

        # Save the stdout  and stderr
        self.stdout0 = sys.stdout
        self.stderr0 = sys.stderr

        # Assign new values
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector
        return


    ## Complete_output
    # This member function complete the output for the test
    # it disconnects the output redirection and restore the
    # saved value of stdout and stderr which were modified
    # by the startTest
    # the function returns the content of the output buffer
    #
    #
    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()


    ## stopTest
    # @param test
    # This member function stops the specified test
    # and restore the output channel in their original assigments
    #
    def stopTest(self, test):

        # Usually one of addSuccess, addError or addFailure would have been called.
        # But there are some path in unittest that would bypass this.
        # We must disconnect stdout in stopTest(), which is guaranteed to be called.
        self.complete_output()
        return


    ## addSuccess
    # Add a Success for the specified  test
    # @param test: The current test for which we want to add a success
    #
    def addSuccess(self, test):
        """
            This function add a success
            it invole the corresponding member in the the base class
        """
        self.success_count += 1
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        self.result.append((0, test, output, ''))

        # output info based on verbosity
        if self.verbosity > 1:
           sys.stderr.write('ok ')
           sys.stderr.write(str(test))
           sys.stderr.write('\n')
           self.logger.debug( 'Ok %s' % str(test))
        else:
           sys.stderr.write('.')
        return

    ## addError
    # Add an Error for the specified test
    # @param test: The current test for which we want to add an error
    #
    def addError(self, test):
        """
            This function add an Error
            it invole the corresponding member in the the base class
        """
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str))

        # output info based  on verbosity
        if self.verbosity > 1:
            sys.stderr.write('E  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
            self.logger.debug( 'E %s' % str(test))
        else:
            sys.stderr.write('E')
        return


    ## addFailure
    # Add a failure for the specified test
    # @param test: The current test for which we want to add a failure
    # @param err: failure message
    #
    def addFailure(self, test, err):
        """
            This function add a Failure
            it invole the corresponding member in the the base class
        """
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('F  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
            self.logger.debug( 'F %s' % str(test))
        else:
            sys.stderr.write('F')
        return

