#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys, json
from com.xebialabs.xlrelease.api.v1.forms import  Variable


class Utils(object):
    def __init__(self):
        return

    @staticmethod
    def get_dynatrace_server(variables):
        dynatrace_server = variables['dynatraceServer']
        if dynatrace_server is None:
            raise Exception("No Dynatrace Server provided!")
        return dynatrace_server

    # Method to get the token from the task config or the Dynatrace Server config
    @staticmethod
    def get_dynatrace_api_token(variables):
        return variables['dynatraceServer']["dynatraceToken"]

    # Method to get the token from the task config or the Dynatrace Server config
    @staticmethod
    def get_dynatrace_server_url(variables):
        server_url = variables['dynatraceServer']['url']
        if server_url.endswith('/'):
            server_url = server_url[:len(server_url)-1]
        return server_url

    # Method to get construct a URL for this release
    @staticmethod
    def get_xlr_url(release_id, base_url):
        rel = release_id.replace("Applications/","").replace("/","-")
        # combine with XLR URL to make complete link to this specific release
        rel_url = '%s/#/releases/%s' % (base_url, rel)
        # print variable for verification
        print "Generated release URL: " + rel_url
        return rel_url

    # Method to get the XL Release server URL from a global variable
    @staticmethod
    def get_xlr_base_url(vars):
        global_xlrelease_url_name = "global.XLRServerURL"
        global_xlrelease_url = None

        #for var in  configurationApi.getGlobalVariables():
        for var in  vars:
            print "Processing variable %s" % var.key
            if global_xlrelease_url_name == var.key:
                print "found XL Release Base URL..."
                global_xlrelease_url = var
                base_url = global_xlrelease_url.value
                print "XLR Base URL is: %s" % base_url
                return base_url
            else:
                print 'Could not find Global variable XLRServerURL.  This must be set for the execution of this plugin'
                sys.exit(1)

    # Method to create a release variable to store things like this release's URL for later use
    @staticmethod
    def create_xlr_release_var(release_api, release_id, rel_url, var_name):
        variables=release_api.getVariables(release_id)
        create_var=True
        for var in variables:
            if var.key == var_name:
                create_var=False
        if create_var == True:
            ReleaseURL=Variable(var_name, rel_url )
            release_api.createVariable(release_id, ReleaseURL)
        else:
            print '%s is already set, moving on...' % var_name

    @staticmethod
    def handle_response(response, event, url):
        if response.isSuccessful():
            print "Registered a %s event with Dynatrace server at %s" % (event, url)
        else:
            print "Failed to register a %s event with Dynatrace server at %s" % (event, url)
            response.errorDump()
            sys.exit(1)
