import subscribe
import emailaccount
import logging
import argparse
import getpass
import time
import random

logger = logging.getLogger()
formatter = logging.Formatter( '%(asctime)s %(levelname)s: %(message)s' )
logger.setLevel( logging.DEBUG )
streamHandler = logging.StreamHandler()
streamHandler.setFormatter( formatter )
fileHandler = logging.FileHandler( 'subscriber.log', mode = 'w' )
fileHandler.setFormatter( formatter )
logger.addHandler( streamHandler )
logger.addHandler( fileHandler )

class Main( object ):
	def __init__( self, listsFile, subscriberAddress, fullName, imapServer, imapUser, imapPassword ):
		if imapUser == None:
			imapUser = subscriberAddress.split( '@' )[ 0 ]
		listsFile = eval( open( listsFile ).read() )

		emailAccount = emailaccount.EmailAccount( imapServer, imapUser, imapPassword )
		emailAccount.login()
		for server, lists in listsFile.iteritems():
			for listName in lists:
				try:
					subscribe.Subscribe( server, listName, subscriberAddress, fullName, emailAccount )
				except:
					logging.exception( 'failed to subscribe to %s on %s' % ( listName, server ) )

				duration = 60 * random.choice( [1,2,3] )
				logging.info( 'sleep %s seconds so as not to arrouse defenses in servers' % duration )
				time.sleep( duration )

		logging.info( 'all done.' )

if __name__ == '__main__':
	parser = argparse.ArgumentParser( description = "subscribe to multiple Red Hat mailing lists" )
	parser.add_argument( 'listsFile', help = "file with all the details of the mailing lists in JSON, see example.conf" )
	parser.add_argument( 'email', help = "address of subscriber, e.g. myuser@redhat.com" )
	parser.add_argument( 'fullName', help = 'your full name, e.g. "I. M. Weasel"' )
	parser.add_argument( '--imapServer', default = 'mail.corp.redhat.com', help = 'your IMAP mail server. default = mail.corp.redhat.com' )
	parser.add_argument( '--imapUser', help = 'user on IMAP mail server. if not specified, I will use you email address to deduce it', default = None )
	arguments = parser.parse_args()
	imapPassword = getpass.getpass( 'your email password please: ' )
	Main( arguments.listsFile, arguments.email, arguments.fullName, arguments.imapServer, arguments.imapUser, imapPassword )
