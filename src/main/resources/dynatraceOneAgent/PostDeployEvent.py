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
from dynatraceOneAgent.Utils import Utils

# Setup vars
dynatrace_server = Utils.get_dynatrace_server(locals())
release_id = getCurrentRelease().id
rel_url = Utils.get_xlr_url(release_id, Utils.get_xlr_base_url(configurationApi.getGlobalVariables()))
release_owner = "releaseVariables[release.owner]"
api_key = Utils.get_dynatrace_api_token(locals())
api_url = Utils.get_dynatrace_event_api_url(locals())
server_url = Utils.get_dynatrace_server_url(locals())

# Some debug
print 'The Release ID  is: %s' % release_id

# For convenience, create a release variable with this releases URL
Utils.create_xlr_release_var(releaseApi, release_id, rel_url, releaseUrlVariableName)

# Setup http connection
connection = HttpRequest(dynatrace_server)

# Body of the http call to the Dynatrace server
content = {'eventType' : eventType,
           'attachRules' : {'tagRule' : {'meTypes' : meType, 'tags' : [ customTags ] } },
           'deploymentName' : deploymentName,
           'deploymentVersion' : deploymentVersion,
           'deploymentProject' : deploymentProject,
           'remediationAction' : remediationUrl,
           'ciBackLink' : rel_url,
           'source' : source,
           'customProperties' : {'Owner' : release_owner, 'Release ID' : release_id} }

print 'Json content is: '
print json.dumps(content)

# Post Event to the Dynatrace server
response = connection.post(api_url, body=json.dumps(content), contentType = 'application/json', headers={"Accept": "application/json", "Authorization": "Api-Token %s" % api_key})

# Check the http response of the post
Utils.handle_response(response, "Deployment", server_url)
