import webapp2

class Hello(webapp2.RequestHandler):
    def get(self):
        self.response.write('hello!')
        
application3 = webapp2.WSGIApplication([
        ('/hello/world', Hello),
], debug=True)

