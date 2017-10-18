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
import sqlite3
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
        "speech": speech,
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
@app.route('/get')
def get_task():
    conn = sqlite3.connect("Database.db")
    cur = conn.cursor()
    cur.execute("select action,mode from sample")
    a = cur.fetchall()

    execute = ""
    assets = "<assets>hjl04302</assets>"
    for i in a:
        execute = "<execute>"+str(i[0])+"___"+str(i[1])+"</execute>"
    conn.close()
    return str(execute)+"\n"+str(assets)

@app.route('/reset_all',methods=['GET'])
def reset_all():
    conn = sqlite3.connect("Database.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM sample")

    conn.commit()
    conn.close()
    return "Data cleared"

@app.route('/push',methods=['GET'])
def push_task():
    task_name = request.args.get('action')
    mode = request.args.get('mode')
    machine = request.args.get('pc')

    conn = sqlite3.connect("Database.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS asset_allocation(resource_name text, asset_name text)")
    cur.execute("CREATE TABLE IF NOT EXISTS device_mapping(username text, imei text)")
    cur.execute("CREATE TABLE IF NOT EXISTS sample (action text, mode text,hostname text)")
    #machine = 'hjl04302'
    #cur.execute("insert into sample values ('%s','%s','%s')"%(str(task_name),'metric',str(machine)))
    if request.args.get('Play'):
            mode = str(request.args.get('mode'))
            clip = str(request.args.get('clip'))
            if str(mode) == "open":
                mode = "clip"
            else:
                mode = "close"
                clip = "wmplayer"
            cur.execute("insert into sample values ('%s','%s','%s')"%(str(clip),str(mode),str(machine)))

    elif request.args.get('metric'):
            metric_type = str(request.args.get('metric_type'))
            cur.execute("insert into sample values ('%s','%s','%s')"%(str(metric_type),'metric',str(machine)))
            conn.commit()
    elif request.args.get('Go'):
            if str(request.args.get('demo')) != 'none.jar' and request.args.get('demo'):
                cur.execute("insert into sample values ('%s','%s','%s')"%(str(request.args.get('demo')),'jar',str(machine)))
                conn.commit()
            elif request.args.get('mode') and request.args.get('action'):
                cur.execute("insert into sample values ('%s','%s','%s')"%(str(request.args.get('action')),str(request.args.get('mode')),str(machine)))
                conn.commit()
    else:
        cur.execute("insert into sample values ('"+str(task_name)+"','"+str(mode)+"','"+str(machine)+"')")
    conn.commit()

    conn.close()
    return "<b>push task</b>"


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
