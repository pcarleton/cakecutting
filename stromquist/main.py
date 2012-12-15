#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import logging
import inspect
from datetime import datetime
import json
import jinja2

from Prefs import Prefs
from strom import StromquistKnives, StromquistCheater, StromquistCheater2, StromquistAllCheat

jinja_environment = jinja2.Environment(autoescape=True,
  loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))


class MainHandler(webapp2.RequestHandler):

  def get(self):
    template_values = {}
    template = jinja_environment.get_template('strom.html')
    self.response.out.write(template.render(template_values))



class StromHandler(webapp2.RequestHandler):

  def get(self):
    p1 = prefsFromText(self.request.get("prefs1"))
    p2 = prefsFromText(self.request.get("prefs2"))
    p3 = prefsFromText(self.request.get("prefs3"))

    stromOpts = [StromquistKnives, StromquistCheater, StromquistCheater2, StromquistAllCheat]

    stromk = stromOpts[int(self.request.get("type"))](p1, p2, p3)
    records, vals, endpoints = stromk.run()

    template_values = { 'rawData' : records,
                        'values' : json.dumps(vals),
                        'endpoints': endpoints }
    template = jinja_environment.get_template('vis.html')
    self.response.out.write(template.render(template_values))


def prefsFromText(text):
  points = []
  for line in text.split("\n"):
    x, y = [float(k) for k in line.split()]
    points.append((x, y))

  return Prefs(points)
    

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/runstrom', StromHandler)],
                              debug=True)
