import imaplib
import logging
import re
import time

class EmailAccount( object ):
	def __init__( self, imapServer, user, password ):
		self._imapServer = imapServer
		self._user = user
		self._password = password

	def login( self ):
		self._login( self._imapServer, self._user, self._password )
	
	def confirmationCookie( self, listName ):
		retries = 20
		while True:
			try:
				retries -= 1
				self._server.check()
				return self._confirmationCookie( listName )
			except:
				if retries == 0:
					raise
				logging.info( 'did not find confirmation cookie yet, retrying...' )
				time.sleep( 5 )

		raise Exception( 'failed imap search' )

	def _confirmationCookie( self, listName ):
		logging.info( 'looking for confirmation message' )
		status, data = self._server.search( None, '(FROM %s SUBJECT confirm)' % listName )
		if status != 'OK':
			raise Exception( 'failed imap search' )
		lastMessage = data[ 0 ].split()[ -1 ]

		status, messageInfoList = self._server.fetch( lastMessage, 'all' )
		messageInfo = messageInfoList[ 0 ]
		if status != 'OK':
			raise Exception( 'failed to retrieve confirmation message' )

		return self._extractCookie( messageInfo )

	def _extractCookie( self, messageInfo ):
		result = re.search( '"confirm (?P<cookie>[a-f0-9]+)"', messageInfo ).groupdict()[ 'cookie' ]
		logging.info( 'found cookie: %s' % result )
		return result

	def _login( self, imapServer, user, password ):
		logging.info( 'logging into %s@%s' % ( user, imapServer ) )
		self._server = imaplib.IMAP4_SSL( imapServer )
		status, unused = self._server.login( user, password )
		if status != 'OK':
			raise Exception( 'could not log in to imap server %s' % imapServer )
		self._server.select( 'inbox' )

	def cookie( self ):
		return self._cookie
