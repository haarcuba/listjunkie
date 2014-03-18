import subprocess
import logging

class Run( object ):
	def __init__( self, command ):
		logging.info( 'running: %s' % command )
		subprocess.check_call( command, shell = True, close_fds = True, stderr = open( '/dev/null', 'w' ), stdout = open( '/dev/null', 'w' ) )
