
import argparse
import logging

_LOGGER = logging.getLogger(__name__)

class GentlerArgParser ( argparse.ArgumentParser ):

    throwExceptions = True

    def exit( self, status=0, message=None ):
        if self.throwExceptions:
            raise ValueError( message )

    def error( self, message ):
        if self.throwExceptions:
            raise ValueError(message)