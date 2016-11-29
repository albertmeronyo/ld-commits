#!/usr/bin/env python

# ld-commits.py: backend for LD commits

from flask import Flask, request, jsonify, make_response
import json
from rdflib import Graph, URIRef, RDF, Namespace
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)-15s [%(levelname)s] (%(module)s.%(funcName)s) %(message)s')
logger = logging.getLogger(__name__)

g = Graph()

# endpoint_url = 'http://ld-commits.amp.ops.labs.vu.nl'

# ldp_url = URIRef("http://www.w3.org/ns/ldp#")
# ldp = Namespace(ldp_url)

# g.add((URIRef(endpoint_url), RDF.type, ldp['Resource']))
# g.add((URIRef(endpoint_url), RDF.type, ldp['RDFSource']))
# g.add((URIRef(endpoint_url), RDF.type, ldp['Container']))
# g.add((URIRef(endpoint_url), RDF.type, ldp['BasicContainer']))
# g.bind('ldp', ldp)

@app.route('/', methods=['GET'])
def landing():
    # return 'LD-commits server here, listening to your POST commit HTTP requests :-)'
    resp = make_response(g.serialize(format='application/ld+json'))
    resp.headers['X-Powered-By'] = 'https://github.com/albertmeronyo/ld-commits'
    resp.headers['Allow'] = 'POST, GET'
    resp.headers['Content-Type'] = 'application/ld+json'

    return resp

@app.route('/', methods=['POST'])
def post_hook():
    push = json.loads(request.data)
    for c in push['commits']:
        commit_message = c['message']
    logger.debug('Received commit message: {}'.format(commit_message))

    # We'll ignore the first line of the commit message
    # Typically this line is by humans for humans
    rdf_message = commit_message.split('\n', 1)[-1]
    
    logger.debug('Parsing triples from commit message')

    g.parse(data=rdf_message, format='turtle')
    logger.debug('RDF graph parsed {} triples'.format(len(g)))
    
    return c['message']

if __name__ == '__main__':
    app.run(port=5000, debug=True)
