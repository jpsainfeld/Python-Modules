#!/usr/bin/env python

## @mainpage Test Report Generator Documentation
#
#  @section intro_sec Introduction
#  This package is used to produce test reports in an HTML5 format
#  The constituant modules are:
#  --init__.py
#
#  OutputRedirector.py
#
#  Template_mixin.py
#
#  TestResult.py
#
#  TestRunner.py
#
#
#
#
#
#
#  @section reference_sec Reference
#  Understanding the workings of this package assumes the user is familiar with:
#  1) xml and the xml.sax python module
#     Extensive information can be found at the following location:
#
#     http://pyxml.sourceforge.net/topics/howto/section-SAX.html
#     Suffice to say here that we are using the xml.sax module to allow
#     easy substituion of defined varables in the HTML/HTML5 template
#     to be replaced by their computed conterpart resulting from the execution
#     of the testcases
#
#
#
#  @section design_sec Design
#  This module leverages a combination of technologies to produce the final result
#
#  1) A set of templates are used to describe the layout of the final HTML report
#  document. The template are collected in the direcotry ./tmpl_5
#
#  2) Javascript functions are used to allow manipulation of the document
#     given the user the possibility of  selecting several mode of display
#     i.e. showing or not the details of a particular test case
#
#
#  @section install_sec Installation
#  The package is installed in the Python path
#  c:\\Python34\\Lib\\site_packages
#  this is automatically done when the command
#  python setup.py install is invoked
#  see the setup.py documentation for details
#
#
#  @section license_sec License
#  Copyright 2015-2016 @em Logitech @em

from Template_mixin import Template_mixin
from xml.sax import saxutils
import sys
import datetime
from TestResult import _TestResult
import logging

__author__ = "Jean-Pierre Sainfeld"
__version__ = "0.0.1"



class TestRunner(Template_mixin):
    """
        This is the class TestRunner
        it is a derived class from the Template_mixin class
    """

    ## Constructor
    #
    # @param stream: an Open stream to save output
    # @param verbosity: A verbosity level
    # @param title: Title of the report
    # @param description: Description
    #
    def __init__(self, stream=sys.stdout, verbosity=1, title=None, description=None):

        # invoke the contructor of the base class
        super().__init__()

        # save all the arguments and set default when appropriate
        self.stream = stream
        self.verbosity = verbosity
        if title is None:
            self.title = self.default_title
        else:
            self.title = title

        if description is None:
            self.description = self.default_description
        else:
            self.description = description

        self.startTime = datetime.datetime.now()

        self.logger = logging.getLogger(__name__)
        self.logger.debug('Test ')
        self.result = []
        return

    ## run
    # @param test: The current test case or suite
    #
    def run(self, test, index):
        """
            This function executes the specified test or test suite
        """

        "Run the given test case or test suite."
        r = _TestResult(self.verbosity)
        self.result.append(r)
        test(self.result[index])
        self.stopTime = datetime.datetime.now()
        self.generateReport(test, self.result, index)
        duration = self.stopTime - self.startTime
        self.logger.info(duration)
        self.logger.info('Time Elapsed: %s' % duration)
        return self.result[index]

    ## Sort
    # @param result_list: a list of result elements
    #
    #
    def sortResult(self, result_list):
        """
            This function sort the result
        """
        # unittest does not seems to run in any particular order.
        # Here at least we want to group them together by class.
        self.logger.debug('sortResult')
        rmap = {}
        classes = []
        # n is ? 0,1,2 result of test
        # t is test class ( test case)
        # o is ?
        # e is trace back buffer
        for n,t,o,e in result_list:
            cls = t.__class__
            if cls not in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n,t,o,e))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    ## getReportAttributes
    # @param result:
    #
    def getReportAttributes(self, result, ri):
        self.logger.debug('getReportAttributes')
        startTime = str(self.startTime)[:19]
        duration = str(self.stopTime - self.startTime)
        status = []
        if result[ri].success_count:
            status.append('Pass %s'    % result[ri].success_count)
        if result[ri].failure_count:
            status.append('Failure %s' % result[ri].failure_count)
        if result[ri].error_count:
            status.append('Error %s'   % result[ri].error_count  )
        if status:
            status = ' '.join(status)
        else:
            status = 'none'
        return [
            ('Start Time', startTime),
            ('Duration', duration),
            ('Status', status),
        ]

    ## generateReport
    # @param test: the current test case or suite
    # @param result: the set of collected results
    #
    def generateReport(self, test, result, r_index):
        """
            This function generate the Report the
            specified test and the corresponding results
        """
        self.logger.debug('generateReport')
        # Get the Report Attributes
        report_attrs = self.getReportAttributes(result, r_index)

        generator = 'TestRunner %s' % __version__

        # this is no longer needed as we use the HTML5 external style sheet.
        use_local_css = False

        if use_local_css is True:
            stylesheet = self._generate_stylesheet()

        # Generate Heading
        heading = self._generate_heading(report_attrs)

        # Generate Report
        report = self._generate_report(result, r_index)

        # Generate Ending
        ending = self._generate_ending()

        # Create the Output string
        if use_local_css is True:

            output = self.html_tmpl % dict(
                title = saxutils.escape(self.title),
                generator = generator,
                stylesheet = stylesheet,
                heading = heading,
                report = report,
                ending = ending,
            )
        else:
             output = self.html_tmpl % dict(
                title = saxutils.escape(self.title),
                generator = generator,
                heading = heading,
                report = report,
                ending = ending,
                run_index = r_index,
            )

        #self.stream.write(output.encode('utf8'))
        try:
            self.stream.write(output)
        except:
            self.stream.write(output.encode('utf8'))

    ## Generate the style sheet
    #

    def _generate_stylesheet(self):
        """
            This function generate the stylesheet information
            Note: in order to implement external style sheet
                  some changes are required
        """
        self.logger.debug('_generate_stylesheet')
        return self.stylesheet_tmpl

    ## Generate the Report Heading
    # @param report_attrs:  specifies the various report attributes
    #
    def _generate_heading(self, report_attrs):
        """
            This function generate the required heading for the
            Html file
        """
        self.logger.debug('_generate_heading')
        # Start with an empty array of lines
        a_lines = []

        # Walk the tuple [name,value] in the report_attributes ( generated)
        for name, value in report_attrs:

            # Build the line for the current tuple [name,value]
            line = self.heading_attribute_tmpl % dict(
                    name = saxutils.escape(name),
                    value = saxutils.escape(value),
                )

            # add this line to the heading array of lines
            a_lines.append(line)

        # Assemble the complete Heading
        heading = self.heading_tmpl % dict(
            title = saxutils.escape(self.title),
            parameters = ''.join(a_lines),
            description = saxutils.escape(self.description),
        )
        return heading

    ## Generate Report
    # @param result:
    #
    def _generate_report(self, result, ri):
        """
            This function generate the report
        """
        self.logger.debug('_generate_report')
        rows = []
        sortedResult = self.sortResult(result[ri].result)

        for cid, (cls, cls_results) in enumerate(sortedResult):
            # subtotal for a class
            numPass = numFail = numError = 0
            for n,t,o,e in cls_results:
                if n == 0:
                    numPass += 1
                elif n == 1:
                    numFail += 1
                else:
                    numError += 1

            # format class description
            if cls.__module__ == "__main__":
                name = cls.__name__
            else:
                name = "%s.%s" % (cls.__module__, cls.__name__)
            doc = cls.__doc__ and cls.__doc__.split("\n")[0] or ""
            desc = doc and '%s: %s' % (name, doc) or name

            # construct a report row
            row = self.report_class_tmpl % dict(
                style = numError > 0 and 'errorClass' or numFail > 0 and 'failClass' or 'passClass',
                desc = desc,
                count = numPass + numFail + numError,
                Pass = numPass,
                fail = numFail,
                error = numFail,
                cid = 'c%s' % (cid+1),
                run_index = ri,
            )
            rows.append(row)

            for tid, (n,t,o,e) in enumerate(cls_results):
                self._generate_report_test(rows, cid, tid, n, t, o, e, ri)

        count = (result[ri].success_count+result[ri].failure_count+result[ri].error_count)
        Pass = (result[ri].success_count)
        fail = (result[ri].failure_count)
        error = (result[ri].error_count)

        percent = 0
        if count != 0:
            percent = '{:.2%}'.format(Pass/count)
        report = self.report_tmpl % dict(
            test_list = ''.join(rows),
            count = str(count),
            Pass = str(Pass),
            fail = str(fail),
            error = str(error),
            percent = str(percent),
            run_index = ri,

        )

        self.logger.info ('Number of Success: %d' % Pass)
        self.logger.info ('Total number of test: %d' % count)
        self.logger.info ('Success Percentage: %s' % percent)

        return report

    ## Generate report for
    # @param rows :
    # @param cid :
    # @param tid:
    # @param n:
    # @param t:
    # @param o:
    # @param e:

    def _generate_report_test(self, rows, cid, tid, n, t, o, e, ri):
        """
            This function contruct a report line for a given test step
        """
        self.logger.debug('_generate_report_test:  %s' % t)
        # e.g. 'pt1.1', 'ft1.1', etc
        has_output = bool(o or e)
        tidn = (n == 0 and 'p' or 'f') + 't_' + str(ri) + '_' + '%s.%s' % (cid+1,tid+1)
        name = t.id().split('.')[-1]
        doc = t.shortDescription() or ""
        desc = doc and ('%s: %s' % (name, doc)) or name
        tmpl = has_output and self.report_test_with_output_tmpl or self.report_test_no_output_tmpl

        # o and e should be byte string because they are collected from stdout and stderr?
        if isinstance(o,str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # uo = unicode(o.encode('string_escape'))
            #uo = o.decode('latin-1')
            uo = o
        else:
            uo = o
        if isinstance(e,str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # ue = unicode(e.encode('string_escape'))
            #ue = e.decode('latin-1')
            ue = e
        else:
            ue = e

        script = self.report_test_output_tmpl % dict(
            id = tidn,
            output = saxutils.escape(uo+ue),
            run_index = ri,
        )

        row = tmpl % dict(
            tid = tidn,
            Class = (n == 0 and 'hiddenRow' or 'none'),
            style = n == 2 and 'errorCase' or (n == 1 and 'failCase' or 'none'),
            desc = desc,
            script = script,
            status = self.status[n],
            run_index = ri,
        )
        rows.append(row)
        if not has_output:
            return

    ## Generate Ending of report

    def _generate_ending(self):
        """
            This function generate the ending portion of the report
        """
        self.logger.debug('_generate_ending')
        return self.ending_tmpl


