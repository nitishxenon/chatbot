from flask import Flask, render_template, request, jsonify
import aiml
import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from selenium import webdriver 
import time 
  
# set webdriver path here it may vary 

  
app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('chat.html')

@app.route("/ask", methods=['POST'])
def ask():
	message = request.form['messageText'].encode('utf-8').strip()

	kernel = aiml.Kernel()

	if os.path.isfile("bot_brain.brn"):
	    kernel.bootstrap(brainFile = "bot_brain.brn")
	else:
	    kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
	    kernel.saveBrain("bot_brain.brn")

	# kernel now ready for use
	while True:
	    if message == "quit":
	        exit()
	    elif message == "save":
	        kernel.saveBrain("bot_brain.brn")
	    else:
	        bot_response = kernel.respond(message)
	        # print bot_response
	        return jsonify({'status':'OK','answer':bot_response})
            
@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')

    kernel = aiml.Kernel()

    if os.path.isfile("bot_brain.brn"):
	    kernel.bootstrap(brainFile = "bot_brain.brn")
    else:
	    kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
	    kernel.saveBrain("bot_brain.brn")

    while True:
	    if msg == "quit":
	        exit()
	    elif msg == "save":
	        kernel.saveBrain("bot_brain.brn")
	    else:
		    resp = MessagingResponse()
		    bot_response = kernel.respond(msg)
		    resp.message(format(kernel.respond(msg)))
	     
	    return str(resp) 
	                  

if __name__ == "__main__":
    app.run(host='0.0.0.0')
