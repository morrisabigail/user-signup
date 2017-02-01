#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#The form elements where the user inputs their username, password, password again, and email address must be named "username", "password", "verify", and "email", respectively.
# The form method must be POST, not GET.
# Upon invalid user input, your web app should re-render the form for the user.
# Upon valid user input, your web app should redirect to a welcome page for the user.
# This page must include both "Welcome" and the user's username.

import webapp2
import cgi
import re
def build(u_error,p_error,v_error,e_error):


    page_header = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>FlickList</title>
            <style type="text/css">
                span{
                    color: red;
                }
                label{
                    display:inline-block;
                    width: 110px;
                    padding:5px;
                }
            </style>
        </head>
        <body>
            <h1>Sign Up</h1>
        """

        # html boilerplate for the bottom of every page
    page_footer = """
        </body>
        </html>
        """

    username = "<label>Username:</label><input type='text' name='username'>"
    password = "<label>Password:</label><input type='password' name='password'>"
    verify = "<label>Verify Password:</label><input type='password' name='verify'>"
    email = "<label>Email(optional):</label><input type='text' name='email'>"
    submit = "<input type ='submit' value='submit'>"
    form = (page_header + "<form action='/verify' method='post'>" +
        username + "<span>"+ u_error + "</span>" + "<br>"+
        password + "<span>"+ p_error + "</span>" + "<br>"+
        verify + "<span>"+ v_error + "</span>"+ "<br>"+
        email + "<span>"+ e_error + "</span>"+ "<br>"+
        submit + page_footer + "</form>")
    return form

class MainHandler(webapp2.RequestHandler):

    def get(self):
        content = build("","","","")
        self.response.write(content)


class Welcome(webapp2.RequestHandler):
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        #verify password
        if re.match("^.{3,20}$",password):
            p_error = ''
        else:
            p_error = "That's not a valid password"

        #verify password and verify match
        if password == verify:
            v_error = ''
        else:
            v_error = "Your passwords didn't match"

        #verify proper email if email
        if re.match("^[\S]+@[\S]+.[\S]+$",email):
            e_error = ''
        elif email == '':
            e_error = ''
        else:
            e_error = "That's not a valid email"


        #yes but redirect to /welcome
        if re.match("^[a-zA-Z0-9_-]{3,20}$",username):
            u_error = ''
        else:
            u_error = "That's not a valid username"
            #self.response.write("<h1>Welcome, {} </h1>".format(username))


        if u_error == p_error == v_error == e_error:
            self.response.write("<h1>Welcome, {} </h1>".format(username))
        else:
            more_errors = build(u_error,p_error,v_error,e_error)
            self.response.write(more_errors)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/verify', Welcome)
], debug=True)
