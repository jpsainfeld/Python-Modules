#!/usr/bin/env python

from ctypes import *
import getopt
import configparser
import sys
import os
import re
import unittest
import binascii
import time
import subprocess
import logging
import logging.config
import logging.handlers
from progressbar import ProgressBar, SimpleProgress



def TestReportGenTestSuite(fn):
    start = '.'
    pattern = 'test*.py'
    top = None
    loader = unittest.TestLoader()
    suite = loader.discover(start, pattern, top)
    return suite


## Propoer Usage of the command
#
def usage():
    logger = logging.getLogger(__name__)
    logger.info('This is the proper usage function ')
    logger.info('Usage: ' + os.path.split(sys.argv[0])[1] +' [OPTIONS]')
    logger.info('Mandatory arguments to long options are mandatory for short options too.')
    logger.info('')

    return


def main(argv):
    global config
    global pbar
    global test_index

    lcfgPath = os.path.abspath(os.path.dirname(sys.argv[0])) + '\logging.cfg'
    logging.config.fileConfig(lcfgPath, defaults=None, disable_existing_loggers=True)
    logger = logging.getLogger(__name__)
    logger.debug('Test Report Generator Validation')

   # When this module is executed from the command line, run all its tests
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hc:v:r:m::x:s:', ['help', 'config=', 'verbose=', 'report=', 'mode=',  'repeat=', 'suite='])
    except getopt.GetoptError as err:
        # print help information and exit:
        logger.error (str(err)) # will print something like 'option -a not recognized
        logger.error('option not recognized')
        usage()
        sys.exit(2)

    mode   = None
    repeat = 1
    report_fn = None
    suite_fn = None
    config_fn = None
    config = None

    for o, a in opts:
        if o in ( '-v', '--verbose'):
            valid_levels = [ 'NOTSET',
                             'DEBUG',
                             'INFO',
                             'WARNING',
                             'ERROR',
                             'CRITICAL'
                             ]

            logger_levels = [logging.NOTSET,
                             logging.DEBUG,
                             logging.INFO,
                             logging.WARNING,
                             logging.ERROR,
                             logging.CRITICAL
                            ]
            verbose_level = a
            if verbose_level in valid_levels:
                i = valid_levels.index(verbose_level)
                logger.setLevel(logger_levels[i])
            else:
                usage()
                sys.exit()

        elif o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-c', '--config'):
            config_fn = a
            if os.path.exists(config_fn) is False:
                logger.error('The specified config file %s does not exist' % config_fn)
                sys.exit(3)
        elif o in ('-r', '--report'):
            report_fn = a
        elif o in ('-m', '--mode'):
            mode = a
        elif o in ('-x', '--repeat'):
            repeat = int(a)
        elif o in ('-s', '--suite'):
            suite_fn = a
            if os.path.exists(suite_fn) is False:
                logger.error('The specified test suite file %s does not exist' % suite_fn)
                sys.exit(3)
        else:
            assert False, 'unhandled option'


    #
    # handle configuration if specified on command line
    #
    if config_fn:

        logger.info('Handle configuration file')
        config = configparser.ConfigParser()
        try:
            config.read(config_fn)
        except:
            logger.error('we failed')

        logger.debug(config)
        logger.debug(config.sections())
        for c in config.sections():
            logger.debug(c)

    else:
        logger.info('Handle command line args only')




    if mode == 'HTML':
        logger.info('use the TestReportGen module')
        import TestRunner
        res = []
        with open('TestReportGenValidation_report.html', 'wb') as f:
            runner = TestRunner.TestRunner( stream = f, verbosity = 19,  title = 'Test Report Generator Validation', description = 'Test Report Generator Validation HTML report')
            for i in range(repeat):
                r = runner.run(TestReportGenTestSuite(suite_fn), i)
                res.append(r)
            f.close()

    else:
        # do report in text mode with the eventual report file name option
        logger.info('use Text mode')
        if report_fn:
            with open(report_fn, 'w', encoding='utf-8') as f:
                 for i in range(repeat):
                    unittest.TextTestRunner(stream = f, verbosity = 19).run(TestReportGenTestSuite(suite_fn), i)
            f.close()
        else:
            with open('TestReportGen_result.txt', 'w', encoding='utf-8') as f:
                for i in range(repeat):
                    unittest.TextTestRunner(stream = f, verbosity = 19).run(TestReportGenTestSuite(suite_fn), i)
            f.close()


    return 0

if __name__ == '__main__':
    main(sys.argv[1:])
