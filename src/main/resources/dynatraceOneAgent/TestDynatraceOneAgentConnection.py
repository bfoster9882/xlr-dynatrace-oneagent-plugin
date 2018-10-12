#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import sys

params = { 'url': configuration.url }
api_url = configuration.dynatraceEventApiUrl
api_key = configuration.dynatraceToken
connection = HttpRequest(params)

# do an http get request to the server
logger.info('Base URL is %s' % configuration.url)
logger.info('API URL is %s' % api_url)
logger.info('API Key is %s' % api_key)
response = connection.get(api_url, headers={"Content-Type": "application/json", "Accept": "application/json", "Authorization": "Api-Token %s" % api_key})

# check response status code, if is different than 200 exit with error code
logger.info('Http Response code is %s' % response.status)
if response.status != 200:
    sys.exit(1)