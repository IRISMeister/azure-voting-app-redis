from flask import Flask, request, render_template
import os
import random
import irisnative
import socket
import sys

app = Flask(__name__)

# Load configurations from environment or config file
app.config.from_pyfile('config_file.cfg')

if ("VOTE1VALUE" in os.environ and os.environ['VOTE1VALUE']):
    button1 = os.environ['VOTE1VALUE']
else:
    button1 = app.config['VOTE1VALUE']

if ("VOTE2VALUE" in os.environ and os.environ['VOTE2VALUE']):
    button2 = os.environ['VOTE2VALUE']
else:
    button2 = app.config['VOTE2VALUE']

if ("TITLE" in os.environ and os.environ['TITLE']):
    title = os.environ['TITLE']
else:
    title = app.config['TITLE']

# Redis configurations
redis_server = os.environ['REDIS']

# Redis Connection
try:
    if "REDIS_PWD" in os.environ:
        connection = irisnative.createConnection(hostname=redis_server,
                        port=1972,
                        namespace='USER',
                        username='_SYSTEM',
                        password=os.environ['IRIS_PWD'])
    else:
        connection = irisnative.createConnection(hostname=redis_server,
                        port=1972,
                        namespace='USER',
                        username='_SYSTEM',
                        password='SYS')
    r = irisnative.createIris(connection)
except:
    exit('Failed to connect to Redis, terminating.')

# Change title to host name to demo NLB
if app.config['SHOWHOST'] == "true":
    title = socket.gethostname()

# Init Redis
if not r.get(button1): r.set(0,button1)
if not r.get(button2): r.set(0,button2)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':

        # Get current values
        vote1 = r.get(button1)
        vote2 = r.get(button2)        

        # Return index with values
        return render_template("index.html", value1=int(vote1), value2=int(vote2), button1=button1, button2=button2, title=title)

    elif request.method == 'POST':

        if request.form['vote'] == 'reset':
            
            # Empty table and return results
            r.set(0,button1)
            r.set(0,button2)
            vote1 = r.get(button1)
            vote2 = r.get(button2)
            return render_template("index.html", value1=int(vote1), value2=int(vote2), button1=button1, button2=button2, title=title)
        
        else:

            # Insert vote result into DB
            vote = request.form['vote']
            r.increment(1,vote)
            
            # Get current values
            vote1 = r.get(button1)
            vote2 = r.get(button2)  
                
            # Return results
            return render_template("index.html", value1=int(vote1), value2=int(vote2), button1=button1, button2=button2, title=title)

if __name__ == "__main__":
    app.run()
