#!/usr/bin/env python
import logging


GLOBAL_VERBOSITY = 0

class LoggingErrorFilter(logging.Filter):
  def filter(self, record):
    if record.__dict__.get("verbosity", 0) > GLOBAL_VERBOSITY:
      #print ("Log message verbosity is greater than threshold, logging line:{0}".format(record))
      return True
    #print ("Log message verbosity is lower than threshold, not logging line:{0}".format(record))
    return False

