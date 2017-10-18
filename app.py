from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response
##import requests as r

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/')
def homepage():
    return "Welcome to API.AI"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    

##    res = processRequest(req)
    if req.get("result").get("action") != "myIntent":
        return {}
    text = req.get("result").get("parameters").get("text")
        
    speech = "Hi Prabhakar,"+str(text)

    voiceCommand = text.lower()
    filteredVoiceCMD = voiceCommand
    filterCommand =""
    if(((voiceCommand.find("lock") > -1 and voiceCommand.find("computer") > -1 )) or (voiceCommand.find("lock")  > -1 and voiceCommand.find("laptop") > -1) or (voiceCommand.find("lock") > -1 and voiceCommand.find("pc") > -1 )):
        filterCommand = "lock";
    if((voiceCommand.find("shutdown") > -1 or voiceCommand.find("shut down") > -1) and (voiceCommand.find("computer")  > -1 or voiceCommand.find("pc")  > -1 or voiceCommand.find("machine") > -1)):
        filterCommand = "shutdown";
    if((voiceCommand.find("reboot") > -1 or voiceCommand.find("re boot")  > -1 or voiceCommand.find("re start")  > -1 or voiceCommand.find("restart") > -1) and (voiceCommand.find("computer")  > -1 or voiceCommand.find("pc")  > -1 or voiceCommand.find("machine") > -1)):
        filterCommand = "restart";
			


    
    res = {
        "speech": filterCommand,
        "displayText": filterCommand,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-my-robot-sample"
    }


    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
