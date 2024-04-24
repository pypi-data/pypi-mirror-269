# -*- coding: utf-8 -*-

"""
Copyright (C) 2024, Zato Source s.r.o. https://zato.io

Proprietary product. This is not open source software, reproduction is prohibited.
"""

# stdlib
import os

# ################################################################################################################################
# ################################################################################################################################

ENVIRONMENT = '''# -*- coding: utf-8 -*-

"""
Copyright (C) 2024, Zato Source s.r.o. https://zato.io

Proprietary product. This is not open source software, reproduction is prohibited.
"""

# stdlib
import os

# Zato
from zato.apitest.util import new_context # type: ignore

def before_feature(context, feature): # type: ignore
    environment_dir = os.path.dirname(os.path.realpath(__file__))
    context.zato = new_context(None, environment_dir)
'''

STEPS = '''# -*- coding: utf-8 -*-

"""
Copyright (C) 2024, Zato Source s.r.o. https://zato.io

Proprietary product. This is not open source software, reproduction is prohibited.
"""

# Behave
from behave import given, then

# Zato
from zato.apitest import steps as default_steps
from zato.apitest.steps.json import set_pointer
from zato.apitest.util import obtain_values
'''

# ################################################################################################################################
# ################################################################################################################################

CONFIG_INI = """
[behave]
options=--format pretty --no-source --no-timings

[user]
sample=Hello
"""

# ################################################################################################################################
# ################################################################################################################################

DEMO_FEATURE = """
Feature: Zato API Testing Demo

Scenario: *** REST API Demo ***

    Given address "http://apitest-demo.zato.io:8587"
    Given URL path "/demo/rest"
    Given query string "?demo=1"
    Given format "JSON"
    Given REST method "POST"
    Given header "X-Custom-Header" "MyValue"
    Given request is "{}"
    Given path "/a" in request is "abc"
    Given path "/foo" in request is an integer "7"
    Given path "/bar" in request is a list "1,2,3,4,5"
    Given path "/baz" in request is a random string
    Given path "/hi5" in request is one of "a,b,c,d,e"

    When the URL is invoked

    Then path "/action/msg" is "How do you do?"
    And path "/action/code" is an integer "0"
    And path "/action/flow" is a list "Ack,Done"
    And status is "200"
    And header "Server" is not empty

    # You can also compare responses directly with files disk
    And response is equal to that from "demo.json"
"""

DEMO_JSON_REQ = """{"hello":"world"}"""
DEMO_JSON_RESP = """{"action":{"code":0, "msg":"How do you do?", "flow":["Ack", "Done"]}}"""

# ################################################################################################################################
# ################################################################################################################################

def handle(base_path:'str') -> 'None':
    """ Sets up runtime directories and sample features.
    """
    # Top-level directory for tests
    features_dir = os.path.join(base_path, 'features')
    os.mkdir(features_dir)

    # Requests and responses
    request_json_dir = os.path.join(base_path, 'features', 'json', 'request')
    response_json_dir = os.path.join(base_path, 'features', 'json', 'response')

    os.makedirs(request_json_dir)
    os.makedirs(response_json_dir)

    # Demo feature
    _ = open(os.path.join(features_dir, 'demo.feature'), 'w').write(DEMO_FEATURE)
    _ = open(os.path.join(request_json_dir, 'demo.json'), 'w').write(DEMO_JSON_REQ)
    _ = open(os.path.join(response_json_dir, 'demo.json'), 'w').write(DEMO_JSON_RESP)

    # Add environment.py
    _ = open(os.path.join(features_dir, 'environment.py'), 'w').write(ENVIRONMENT)

    # Add steps
    steps_dir = os.path.join(features_dir, 'steps')
    os.mkdir(steps_dir)
    _ = open(os.path.join(steps_dir, 'steps.py'), 'w').write(STEPS)

    # User-provided CLI parameters, if any, passed to behave as they are.
    # Also, user-defined config stanzas.
    _ = open(os.path.join(features_dir, 'config.ini'), 'w').write(CONFIG_INI)

# ################################################################################################################################
# ################################################################################################################################
