"""
Simple Flask web site for a class poll. 
Originally used to find office hours for CIS 322. 
Revision 4/2017 to survey CIS 422 students prior to forming teams.
Revision 8/2020 to modernize and use as an example
  of repository management
"""

import flask
from flask import request  # Data from a submitted form
from flask import url_for
# from flask import jsonify # For AJAX transactions

import json
import loader
import logging

import arrow
import configparser  

###
# Globals
###
app = flask.Flask(__name__)
config = configparser.ConfigParser()
config.read('config.ini')

app.secret_key = config["DEFAULT"]["cookie_key"] # Should allow using session variables

def config_get_list(category):
    items = (config["DEFAULT"][category]).split(",")
    items = map(lambda x: x.strip(), items)
    return list(items)

# Meeting periods 
days = config_get_list("Days")
periods = config_get_list("Periods")
meetings = [ ]
for day in days:
    meetings.append({ "day": day, "periods": periods })

proficiencies = config_get_list("proficiencies")
prof_items = { }
for prof in proficiencies:
    prof_items[prof] = config_get_list(prof)
app.logger.debug(proficiencies)
app.logger.debug(prof_items)

    

###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
    flask.g.poll = loader.load("polls/team_formation.yaml")
    # app.logger.debug("g.poll: {}".format(flask.g.poll))
    return flask.render_template('poll.html')



@app.route("/ish")
def prior():
    flask.g.choicegroups = meetings
    flask.g.proficiencies = proficiencies
    app.logger.debug("g.proficiencies: {}".format(flask.g.proficiencies))
    flask.g.prof_items = prof_items
    return flask.render_template('prior.html')


#######################
# Form handler
#
#######################

@app.route("/_submit", methods = ["POST"])
def enter():
  """
  Poll has been submitted. 
  Extract data to json-compatible form. 
  """
  app.logger.debug("Processing submission")
  results = request.form.copy()
  app.logger.debug(f"Form: {results}")
  ## Shovel form input into a structure that
  ## we can JSONify:  A dict of lists 
  results['kind'] = "CIS 422 entry poll"
  results["submitted"] = arrow.get().to("US/Pacific").format()
  # List of available times will not jsonify properly unless we specify
  # that it's a list ...
  results["available"] = request.form.getlist("available")
  stash_result(results)
  return flask.redirect(url_for("thanks"))

@app.route("/thanks")
def thanks():
  app.logger.debug("Thanks")
  return flask.render_template('thanks.html')

def stash_result(result):
    """
    STUB - instead of storing in a database, for now I'll 
    just append it to a file. 
    """
    app.logger.debug("Stashing result in file")
    
    stash = open("result.txt", "a")
    json.dump(result, stash)
    print("", file=stash)
    stash.close()
    app.logger.debug("Stashed")
    
#  result = db.poll.insert_one(results)  # See PyMongo initialization above
#  app.logger.debug("ID of inserted object: {}".format(result.inserted_id))


#################
# Functions used within the templates
#################

@app.template_filter( 'filt' )
def format_filt( something ):
    """
    Example of a filter that can be used within
    the Jinja2 code
    """
    return "Not what you asked for"
  
###################
#   Error handlers
###################
@app.errorhandler(404)
def error_404(e):
  app.logger.warning("++ 404 error: {}".format(e))
  return flask.render_template('404.html'), 404

@app.errorhandler(500)
def error_500(e):
   app.logger.warning("++ 500 error: {}".format(e))
   assert app.debug == False #  I want to invoke the debugger
   return flask.render_template('500.html'), 500

@app.errorhandler(403)
def error_403(e):
  app.logger.warning("++ 403 error: {}".format(e))
  return flask.render_template('403.html'), 403



#############

# Set up to run from cgi-bin script, from
# gunicorn, or stand-alone.
#

if __name__ == "__main__":
    # Standalone.
    port = config["DEFAULT"]["port"]
    app.debug = True
    app.logger.setLevel(logging.DEBUG)
    app.logger.debug("Opening for global access on port {}".format(port))
    app.run(port=int(port), host="0.0.0.0")
else:
    # Running from gunicorn WSGI server,
    # which makes the call to app.run.  Gunicorn may invoke more than
    # one instance for concurrent service.
    pass
