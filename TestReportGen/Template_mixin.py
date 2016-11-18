#!/usr/bin/env python

import site
import logging

class Template_mixin(object):

    '''
    Define  templates for report customerization and generation.

    Overall structure of an HTML report in either HTML or HTML5

    HTML
    +------------------------+
    |<html>                  |
    |  <head>                |
    |                        |
    |   STYLESHEET           |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </head>               |
    |                        |
    |  <body>                |
    |                        |
    |   HEADING              |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   REPORT               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   ENDING               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </body>               |
    |</html>                 |
    +------------------------+


  HTML5
    +------------------------+
    |<html>                  |
    |  <head>                |
    |                        |
    |  Reference external css|
    |                        |
    |  </head>               |
    |                        |
    |  <body>                |
    |                        |
    |   HEADING              |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   REPORT               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   ENDING               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </body>               |
    |</html>                 |
    +------------------------+


    '''



    def __init__(self):
        """
            Constructor
            Upon instantiation of this object the various templates are loaded
            in object variables. They can be referenced later in the code in the
            derived classs objects
        """
        self.logger = logging.getLogger(__name__)
        self.logger.debug('Template_mixin')
        ## possible results of the execution of a single test step
        #
        #  0: Indicates that the test step was successful and met the
        #     expectations
        #
        #  1: Indicates that the corresponding file contains informaiton of a
        #     detected problem in the execution of a given test step
        #
        #  2: Indicates that an error has occured in the execution of a single
        #     test step
        #
        self.status = {
			0: 'pass',
			1: 'file',
			2: 'error',
		}

        ## setup default value for title
        #
        self.default_title = 'Unit Test Report'

        ## setup default value for description
        #
        self.default_description = ''

        ## path of  python packages
        path = site.getsitepackages()[1]

        ## append the template directory
        # The templates have been installed there by the setup.py program
        # this happen at system installation
        path += '\\tmpl'

        ## ----------------------------------------------------------------------
        # HTML Template
        # variables: (title, generator, stylesheet, heading, report, ending)
        with open (path + '\\html.tmpl', 'r') as html_file:
            self.html_tmpl = html_file.read()


        ## ----------------------------------------------------------------------
        # Stylesheet
        #
        #  Alternatively use a \<link\> for external style sheet, e.g.
        # \<link rel='stylesheet' href='$url' type='text/css'\>
        #  We now use the HTML5 construct to use external CSS
        #
        use_local_css = False
        if use_local_css is True:
            with open(path + '\\stylesheet.tmpl', 'r') as stylesheet_file:
                self.stylesheet_tmpl = stylesheet_file.read()

        # ---------------------------------------------------------------------
        # Heading
        # Read in the definition of the heading from the template location
        # and save it in a class variable


        ## ---------------------------------------------------------------------
        # Heading
        #
        #   template variables: (title, parameters, description)
        #
        with open(path + '\\heading.tmpl', 'r') as heading_file:
            self.heading_tmpl = heading_file.read()

        # #---------------------------------------------------------------------
        # Heading Attributes
        #
        # template variables: (name, value)
        #
        with open(path + '\\heading_attribute.tmpl', 'r') as heading_attribute_file:
            self.heading_attribute_tmpl = heading_attribute_file.read()


        # ---------------------------------------------------------------------
        # Report
        # Read in the definition of the report from the template location
        # and save it in a class variable

        #

        ## ----------------------------------------------------------------------
        # Report
        #
        # template variables: (test_list, count, Pass, fail, error)
        #
        with open(path + '\\report.tmpl', 'r') as report_file:
            self.report_tmpl = report_file.read()

        ## ----------------------------------------------------------------------
        # Report Class
        #
        # template variables: (style, desc, count, Pass, fail, error, cid)
        #
        with open(path + '\\report_class.tmpl', 'r') as report_class_file:
            self.report_class_tmpl = report_class_file.read()

        ## ----------------------------------------------------------------------
        # Report Test With Output
        #
        # template variables: (tid, Class, style, desc, status)
        #
        with open(path + '\\report_test_with_output.tmpl', 'r') as report_test_with_output_file:
            self.report_test_with_output_tmpl = report_test_with_output_file.read()

        ## ----------------------------------------------------------------------
        # Report Test No Output
        #
        # template variables: (tid, Class, style, desc, status)
        #
        with open(path + '\\report_test_no_output.tmpl', 'r') as report_test_no_output_file:
            self.report_test_no_output_tmpl = report_test_no_output_file.read()

        ## ----------------------------------------------------------------------
        # Report Test Output
        #
        # template variables: (id, output)
        #
        with open(path + '\\report_test_output.tmpl', 'r') as report_test_output_file:
            self.report_test_output_tmpl = report_test_output_file.read()

        ## ------------------------------------------------------------------------
        # ENDING
        # Read in the definition of the ending from the template location
        # and save it in a class variable
        #
        with open(path + '\\ending.tmpl', 'r') as ending_file:
            self.ending_tmpl = ending_file.read()

        return
