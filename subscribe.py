import run
import logging

class Subscribe( object ):
	def __init__( self, server, listName, subscriberAddress, fullName, emailAccount ):
		self._server = server
		self._listName = listName
		self._subscriberAddress = subscriberAddress.replace( '@', '%40' )
		self._fullName = fullName.replace( ' ', '+' )
		self._request()
		self._confirm( emailAccount.confirmationCookie( self._listName ) )

	def _request( self ):
		logging.info( 'requesting subscription for %s' % self._listName )
		postData = 'email=%(email)s&fullname=%(fullName)s&pw=&pw-conf=&digest=0&email-button=Subscribe' % dict( email = self._subscriberAddress, fullName = self._fullName )
		run.Run( "wget -O- --post-data '%(postData)s'  http://%(server)s/mailman/subscribe/%(listName)s" % dict( postData = postData, server = self._server, listName = self._listName ) )

	def _confirm( self, cookie ):
		logging.info( 'confirming subscription to %s' % self._listName )
		postData = 'realname=%(fullName)s&digests=0&language=en&cookie=%(cookie)s&submit=Subscribe+to+list+%(listName)s' %\
			dict( fullName = self._fullName, cookie = cookie, listName = self._listName )
		run.Run( "wget -O- --post-data '%(postData)s' http://%(server)s/mailman/confirm/%(listName)s" % dict( server = self._server, postData = postData, listName = self._listName ) )
