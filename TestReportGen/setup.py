# see http://software-carpentry.codesourcery.com/entries/build/Distutils/Distutils.html for more information about this file

from distutils.core import setup
import distutils.sysconfig

setup (
    name = "TestReportGen",
    version = "0.0.1",
    description = "TestReportGen - Test Report Generation ",
    author = "Jean-Pierre Sainfeld",
    author_email = "jsainfeld@logitech.com",
    maintainer = "Jean-Pierre Sainfeld",
    maintainer_email = "jsainfeld@logitech.com",
    url = "",
    py_modules = ['OutputRedirector','Template_mixin', 'TestResult', 'TestRunner'],
    data_files = 
    	[
    	  (
	        distutils.sysconfig.get_python_lib()+'\\tmpl',
		[
			 'tmpl_5/ending.tmpl'
			,'tmpl_5/heading.tmpl'
			,'tmpl_5/heading_attribute.tmpl'
			,'tmpl_5/html.tmpl'
			,'tmpl_5/report.tmpl'
			,'tmpl_5/report_class.tmpl'
			,'tmpl_5/report_test_no_output.tmpl'
			,'tmpl_5/report_test_output.tmpl'
			,'tmpl_5/report_test_with_output.tmpl'
		
		]

	  ) 
	],
    )

