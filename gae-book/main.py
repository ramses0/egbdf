from google.appengine.api import users
from google.appengine.api import quota
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import datetime
import models
import os


class MainPage( webapp.RequestHandler ):
	def get( self ):
		foo = quota.get_request_cpu_usage()
		time = datetime.datetime.now()
		user = users.get_current_user()

		if not user:
			navbar = ( '<p>Welcome, <a href="%s">sign in</a>  to customize your experience.</p>'
					% (users.create_login_url( self.request.path ) ) )
			tz_form = ''
		else:
			prefs = models.get_userprefs( user.user_id() )
			time += datetime.timedelta( 0, 0, 0, 0, 0, prefs.tz_offset )

			navbar = ( '<p>Welcome %s, <a href="%s">sign out</a>.</p>'
					% ( user.email(), users.create_logout_url( self.request.path ) ) )

			tz_form = """
			<form action="/prefs" method="post">
				TZ Offset from UTC (can be negative):
				<input name="tz_offset" id="tz_offset" type="text" size="4" value="%d" />
				<input type="submit" value="Set!" />
			</form>
			""" % prefs.tz_offset
		bar = quota.get_request_cpu_usage()
		footer = "APPLICATION_ID=%s, CURRENT_VERSION_ID=%s, AUTH_DOMAIN=%s, SERVER_SOFTWARE=%s, begin=%s, end=%s" % (
			os.environ['APPLICATION_ID'],
			os.environ['CURRENT_VERSION_ID'],
			os.environ['AUTH_DOMAIN'],
			os.environ['SERVER_SOFTWARE'],
			foo,
			bar
		)

		self.response.headers['Content-Type'] = 'text/html'
		self.response.out.write( '%s<hr><p>The time is: %s ...</p><hr>%s<hr>&copy;2011<hr>%s'
			% ( navbar, str(time), tz_form, footer ) )

application = webapp.WSGIApplication(
		[('/', MainPage)],
		debug=True
	)

def main():
	run_wsgi_app( application )

if '__main__' == __name__:
	main()
