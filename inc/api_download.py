import os
import logging
import requests
import json
import apie
from api_external import external

class download(external):
    def __init__(this, name="download"):
        super().__init__(name)

        # We want to send binary data.
        this.mime = 'application/force-download'
        this.optionalKWArgs['decode'] = None
        
        this.supportedMethods = ['GET']

        # The redirect_url_field is used if the first request *this makes returns a json describing the file to be downloaded. In such a case, a second request is made to the url provided by the field specified in the json of the response to the first request.
        # If the redirect_url_field is None, the response to the first request is returned.
        this.optionalKWArgs['redirect_url_field'] = None

    # Required Endpoint method. See that class for details.
    def GetHelpText(this):
        return f'''\
Download any file by offloading the retrieval work to another API.
This does not (currently) have access to the local filesystem.

Per the parent 'external':
{super().GetHelpText()}
'''

    def MakeRequest(this):

        #TODO: does stream=True work? Can we pass a stream through requests to flask?

        if (not this.redirect_url_field):
            this.externalResponse = requests.request(**this.externalRequest, stream=True)
            return

        firstResponse = requests.request(**this.externalRequest)
        frJson = json.loads(firstResponse.content.decode('ascii'))

        this.externalResponse = requests.get(frJson[0][this.redirect_url_field], stream=True)

    # All we're doing here is setting a 2-stage download process.
    # We can use the external Call() method.