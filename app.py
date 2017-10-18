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
##    output = ""
##
##    if str(text).lower().find("near") >-1 and str(text).lower().find("me") > -1:
##        query = text
##        s = "http://www.google.co.in/search?q="+query+"&oq=petrol+pump&gs_l=psy-ab.3.0.0l3j0i131k1.2650.16739.0.19169.31.24.4.0.0.0.1498.4928.0j2j0j2j2j1j1j1.9.0..3..0...1.1.64.psy-ab..20.11.3920.6..0i67k1j35i39k1.iIX3uFwT7Xc"
##        a = r.get(s)
##        entries = a.text.replace("\"", "'").replace("[+]", " ").replace("%26", "&").replace("\u0026amp;", "-").replace("\"", "'").split("role='heading'")
##        results = {}
##        for i in entries:
##            if str(i).find("</div><div>") > -1:
##                a = i.split("</div><div>")
##                place = a[0]
##                ##        print place
##                if i.find("</div><div><span>") > -1:
##                    addr = i.split("</div><div><span>")[1]
##                    if addr.find("</span>") > -1:
##                        addr = addr.split("</span>")[0]
##                        results[str(addr)] = str(place)
##        
##        for addr,place in results.iteritems():
##            output = str(output) +"\n"+str(place)+"\n\t"+str(addr)
##    else:
##        output = text

        
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
        "speech": speech,
        "displayText": filterCommand,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
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
