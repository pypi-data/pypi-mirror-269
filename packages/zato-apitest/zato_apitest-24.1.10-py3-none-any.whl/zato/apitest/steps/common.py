# -*- coding: utf-8 -*-

"""
Copyright (C) 2024, Zato Source s.r.o. https://zato.io

Proprietary product. This is not open source software, reproduction is prohibited.
"""

# stdlib
import ast
import json
import time
import os
from logging import getLogger

# Behave
from behave import given, when, then # type: ignore

# Bunch
from bunch import Bunch

# datadiff
from datadiff.tools import assert_equals # type: ignore

# etree
from lxml import etree

# jsonpointer
from jsonpointer import resolve_pointer as get_pointer

# Request
from requests import api as req_api
from requests.auth import HTTPBasicAuth

# Zato
from zato.apitest import util
from zato.apitest import Auth, Channel_Type, Invalid, No_Value

# ################################################################################################################################
# ################################################################################################################################

if 0:
    from zato.apitest.typing_ import any_, anylistnone, callable_

# ################################################################################################################################
# ################################################################################################################################

logger = getLogger(__name__)

# ################################################################################################################################
# ################################################################################################################################

Context = Bunch

# ################################################################################################################################
# ################################################################################################################################

@when('the URL is invoked')
def when_the_url_is_invoked(ctx:'Context', adapters:'anylistnone'=None) -> 'None':

    response_data = None

    try:

        if ctx.zato.get('zato_channel_type') == Channel_Type.WSX:
            invoke_zato_web_sockets_service(ctx)
        else:
            invoke_http(ctx, adapters)

            response_data = ctx.zato.response.data_text

            # If no response_format is set, assume it's the same as the request format.
            # If the request format hasn't been specified either, assume 'RAW'.
            response_format = ctx.zato.request.get('response_format', ctx.zato.request.get('format', 'JSON'))

            if response_format == 'JSON':
                ctx.zato.response.data_impl = json.loads(ctx.zato.response.data_text)

            elif response_format == 'RAW':
                ctx.zato.response.data_impl = ctx.zato.response.data_text

            elif response_format == 'FORM':
                ctx.zato.response.data_impl = ctx.zato.response.data_text

    except Exception as e:
        logger.warn('Caught an exception while invoking `%s` with `%s`; req=`%s`; resp=`%s`, (%s)',
            ctx.zato.full_address, ctx.zato.request.method, ctx.zato.request.data, response_data, e.args[0])
        raise

# ################################################################################################################################
# ################################################################################################################################

def invoke_http(ctx:'Context', adapters:'anylistnone'=None) -> 'None':

    adapters = adapters or []
    method = ctx.zato.request.get('method', 'GET')
    address = ctx.zato.request.get('address')
    url_path = ctx.zato.request.get('url_path', '/')
    qs = ctx.zato.request.get('query_string', '')
    files = None
    data = ''

    if 'data_impl' in ctx.zato.request:
        if ctx.zato.request.get('is_xml'):
            data = etree.tostring(ctx.zato.request.data_impl)
        elif ctx.zato.request.get('is_json'):
            data = json.dumps(ctx.zato.request.data_impl, indent=2)
            ctx.zato.request.headers['Content-Type'] = 'application/json'
        elif ctx.zato.request.get('is_raw'):
            data = ctx.zato.request.data_impl
        elif ctx.zato.request.get('is_form'):
            data = ctx.zato.request.get('form', '')
            files = ctx.zato.request.get('files', None)
            ctx.zato.request.headers['Content-Type'] = 'application/x-www-form-urlencoded'

            if files is not None:
                # multipart/formdata should let requests set the content-type header
                del ctx.zato.request.headers['Content-Type']
        else:
            # Default to JSON
            data = json.dumps(ctx.zato.request.data_impl, indent=2)
            ctx.zato.request.headers['Content-Type'] = 'application/json'

    ctx.zato.request.method = method
    ctx.zato.request.data = data
    ctx.zato.full_address = '{}{}{}'.format(address, url_path, qs)

    auth = None

    # New in 1.1 hence optional
    if ctx.zato.get('auth'):
        if ctx.zato.auth['type'] == Auth.Basic_Auth:
            auth = HTTPBasicAuth(ctx.zato.auth['username'], ctx.zato.auth['password'])

    ctx.zato.response = Bunch()

    session = req_api.sessions.Session() # type: ignore

    for adapter in adapters:
        session.mount('http://', adapter)
        session.mount('https://', adapter)

    ctx.zato.response.data = session.request(
        method,
        ctx.zato.full_address,
        data=data,
        files=files,
        headers=ctx.zato.request.headers,
        auth=auth)

    ctx.zato.response.data_text = ctx.zato.response.data.text

# ################################################################################################################################
# ################################################################################################################################

def invoke_zato_web_sockets_service(ctx:'Context') -> 'None':

    ctx.zato.response = Bunch()
    ctx.zato.response.data_text = json.dumps(ctx.zato.wsx_client.invoke(ctx.zato.request.data_impl).data)
    ctx.zato.response.data_impl = json.loads(ctx.zato.response.data_text)

# ################################################################################################################################
# ################################################################################################################################

@given('address "{address}"')
@util.obtain_values
def given_address(ctx:'Context', address:'str') -> 'None':
    ctx.zato.request.address = address

# ################################################################################################################################

@given('URL path "{url_path}"')
@util.obtain_values
def given_url_path(ctx:'Context', url_path:'str') -> 'None':
    ctx.zato.request.url_path = url_path

# ################################################################################################################################

@given('REST method "{method}"')
def given_http_method(ctx:'Context', method:'str') -> 'None':
    ctx.zato.request.method = method

# ################################################################################################################################
# ################################################################################################################################

def set_request_format(ctx:'Context', format:'str') -> 'None':
    ctx.zato.request.format = format

    ctx.zato.request.is_xml = ctx.zato.request.format == 'XML'
    ctx.zato.request.is_json = ctx.zato.request.format == 'JSON'
    ctx.zato.request.is_raw = ctx.zato.request.format == 'RAW'
    ctx.zato.request.is_form = ctx.zato.request.format == 'FORM'

@given('format "{format}"')
@util.obtain_values
def given_format(ctx:'Context', format:'str') -> 'None':
    set_request_format(ctx, format)

# ################################################################################################################################

@given('request format "{format}"')
@util.obtain_values
def given_request_format(ctx:'Context', format:'str') -> 'None':
    set_request_format(ctx, format)

# ################################################################################################################################

@given('response format "{format}"')
@util.obtain_values
def given_response_format(ctx:'Context', format:'str') -> 'None':
    ctx.zato.request.response_format = format

# ################################################################################################################################

@given('user agent is "{value}"')
@util.obtain_values
def given_user_agent_is(ctx:'Context', value:'str') -> 'None':
    ctx.zato.request.headers['User-Agent'] = value

# ################################################################################################################################

@given('header "{header}" "{value}"')
@util.obtain_values
def given_header(ctx:'Context', header:'str', value:'str') -> 'None':
    ctx.zato.request.headers[header] = value

# ################################################################################################################################
# ################################################################################################################################

def given_request_impl(ctx:'Context', data:'any_') -> 'None':

    ctx.zato.request.data = data

    if ctx.zato.request.get('is_json'):
        ctx.zato.request.data_impl = json.loads(ctx.zato.request.data)
    elif ctx.zato.request.get('is_raw'):
        ctx.zato.request.data_impl = ctx.zato.request.data
    else:
        ctx.zato.request.data_impl = json.loads(ctx.zato.request.data)

# ################################################################################################################################

@given('request "{request_path}"')
@util.obtain_values
def given_request(ctx:'Context', request_path:'str') -> 'None':
    return given_request_impl(ctx, util.get_data(ctx, 'request', request_path))

# ################################################################################################################################

@given('request is "{data}"')
@util.obtain_values
def given_request_is(ctx:'Context', data:'any_') -> 'None':
    return given_request_impl(ctx, data)

# ################################################################################################################################

@given('request file "{name}" is "{value}"')
@util.obtain_values
def given_request_file(ctx:'Context', name:'str', value:'any_') -> 'None':
    ctx.zato.request.data_impl = None
    files = ctx.zato.request.get('files', {})

    full_path = util.get_full_path(ctx.zato.environment_dir, 'form', 'request', value)

    if not os.path.isfile(full_path):
        raise ValueError('File upload not found: {}'.format(full_path))

    files[name] = open(full_path, 'rb')

    ctx.zato.request.files = files

# ################################################################################################################################

@given('request param "{name}" is "{value}"')
@util.obtain_values
def given_request_param(ctx:'Context', name:'str', value:'any_') -> 'None':
    ctx.zato.request.data_impl = None
    form = ctx.zato.request.get('form', {})
    if name in form:
        if isinstance(form[name], list):
            form[name].append(value)
        else:
            form[name] = [form[name], value]
    else:
        form[name] = value

    ctx.zato.request.form = form

# ################################################################################################################################

@given('query string "{query_string}"')
@util.obtain_values
def given_query_string(ctx:'Context', query_string:'str') -> 'None':
    ctx.zato.request.query_string = query_string

# ################################################################################################################################

@given('date format "{name}" "{format}"')
@util.obtain_values
def given_date_format(ctx:'Context', name:'str', format:'str'):
    ctx.zato.date_formats[name] = format

# ################################################################################################################################
# ################################################################################################################################

@given('Basic Auth "{username}" "{password}"')
@util.obtain_values
def given_basic_auth(ctx:'Context', username:'str', password:'str') -> 'None':
    ctx.zato.auth['type'] = Auth.Basic_Auth
    ctx.zato.auth['username'] = username
    ctx.zato.auth['password'] = password

# ################################################################################################################################
# ################################################################################################################################

@given('I store "{value}" under "{name}"')
@util.obtain_values
def given_i_store_value_under_name(ctx:'Context', value:'str', name:'any_') -> 'None':
    ctx.zato.user_ctx[name] = value

# ################################################################################################################################
# ################################################################################################################################

@given('I store a random string under "{name}"')
@util.obtain_values
def given_i_store_a_random_string_under_name(ctx:'Context', name:'any_') -> 'None':
    ctx.zato.user_ctx[name] = util.rand_string()

# ################################################################################################################################
# ################################################################################################################################

@given('I store a random integer under "{name}"')
@util.obtain_values
def given_i_store_a_random_integer_under_name(ctx:'Context', name:'any_') -> 'None':
    ctx.zato.user_ctx[name] = util.rand_int()

# ################################################################################################################################
# ################################################################################################################################

@given('I store a random float under "{name}"')
@util.obtain_values
def given_i_store_a_random_float_under_name(ctx:'Context', name:'any_') -> 'None':
    ctx.zato.user_ctx[name] = util.rand_float()

# ################################################################################################################################
# ################################################################################################################################

@given('I store a random date under "{name}", format "{format}"')
@util.obtain_values
def given_i_store_a_random_date_under_name(ctx:'Context', name:'str', format:'str') -> 'None':
    ctx.zato.user_ctx[name] = util.rand_date(ctx.zato.date_formats[format])

# ################################################################################################################################
# ################################################################################################################################

@then('context is cleaned up')
@util.obtain_values
def then_context_is_cleaned_up(ctx:'Context') -> 'None':
    ctx.zato = util.new_context(ctx, '')

# ################################################################################################################################

@then('form is cleaned up')
@util.obtain_values
def then_form_is_cleaned_up(ctx:'Context') -> 'None':
    if 'form' in ctx.zato.request:
        del ctx.zato.request['form']
    if 'files' in ctx.zato.request:
        del ctx.zato.request['files']

# ################################################################################################################################

@then('status is "{expected_status}"')
@util.obtain_values
def then_status_is(ctx:'Context', expected_status:'any_') -> 'bool':
    expected_status = int(expected_status)
    assert ctx.zato.response.data.status_code == expected_status, 'Status expected `{!r}`, received `{!r}`'.format(
        expected_status, ctx.zato.response.data.status_code)
    return True

# ################################################################################################################################

@then('header "{expected_header}" is "{expected_value}"')
@util.obtain_values
def then_header_is(ctx:'Context', expected_header:'str', expected_value:'str') -> 'bool':
    value = ctx.zato.response.data.headers[expected_header]
    assert value == expected_value, 'Expected for header `{}` to be `{}` instead of `{}`'.format(
        expected_header, expected_value, value)
    return True

# ################################################################################################################################

@then('header "{expected_header}" is not "{expected_value}"')
@util.obtain_values
def then_header_isnt(ctx:'Context', expected_header:'str', expected_value:'str') -> 'bool':
    value = ctx.zato.response.data.headers[expected_header]
    assert expected_value != value, 'Expected for header `{}` not to be equal to `{}`'.format(
        expected_header, expected_value)
    return True

# ################################################################################################################################

@then('header "{expected_header}" contains "{expected_value}"')
@util.obtain_values
def then_header_contains(ctx:'Context', expected_header:'str', expected_value:'str') -> 'bool':
    value = ctx.zato.response.data.headers[expected_header]
    assert expected_value in value, 'Expected for header `{}` to contain `{}` in `{}`'.format(
        expected_header, expected_value, value)
    return True

# ################################################################################################################################

@then('header "{expected_header}" does not contain "{expected_value}"')
@util.obtain_values
def then_header_doesnt_contain(ctx:'Context', expected_header:'str', expected_value:'str') -> 'bool':
    value = ctx.zato.response.data.headers[expected_header]
    assert expected_value not in value, 'Header `{}` shouldn\'t contain `{}` in `{}`'.format(
        expected_header, expected_value, value)
    return True

# ################################################################################################################################

@then('header "{expected_header}" exists')
@util.obtain_values
def then_header_exists(ctx:'Context', expected_header:'str') -> 'bool':
    value = ctx.zato.response.data.headers.get(expected_header, Invalid)
    assert value != Invalid, 'Header `{}` should be among `{}`'.format(expected_header, ctx.zato.response.data.headers)
    return True

# ################################################################################################################################

@then('header "{expected_header}" does not exist')
@util.obtain_values
def then_header_doesnt_exist(ctx:'Context', expected_header:'str') -> 'bool':
    value = ctx.zato.response.data.headers.get(expected_header, Invalid)
    assert value == Invalid, 'Header `{}` shouldn\'t be among `{}`'.format(expected_header, ctx.zato.response.data.headers)
    return True

# ################################################################################################################################

@then('header "{expected_header}" is empty')
@util.obtain_values
def then_header_is_empty(ctx:'Context', expected_header:'str') -> 'bool':
    value = ctx.zato.response.data.headers[expected_header]
    assert value == '', 'Header `{}` should be empty instead of `{}`'.format(expected_header, value)
    return True

# ################################################################################################################################

@then('header "{expected_header}" is not empty')
@util.obtain_values
def then_header_isnt_empty(ctx:'Context', expected_header:'str') -> 'bool':
    value = ctx.zato.response.data.headers[expected_header]
    assert value != '', 'Header `{}` shouldn\'t be empty'.format(expected_header)
    return True

# ################################################################################################################################

@then('header "{expected_header}" starts with "{expected_value}"')
@util.obtain_values
def then_header_starts_with(ctx:'Context', expected_header:'str', expected_value:'str') -> 'bool':
    value = ctx.zato.response.data.headers[expected_header]
    assert value.startswith(expected_value), 'Expected for header `{}` to start with `{}` but it\'s `{}`'.format(
        expected_header, expected_value, value)
    return True

# ################################################################################################################################

@then('header "{expected_header}" does not start with "{expected_value}"')
@util.obtain_values
def then_header_doesnt_starts_with(ctx:'Context', expected_header:'str', expected_value:'str') -> 'bool':
    value = ctx.zato.response.data.headers[expected_header]
    assert not value.startswith(expected_value), 'Expected for header `{}` not to start with `{}` yet it\'s `{}`'.format(
        expected_header, expected_value, value)
    return True

# ################################################################################################################################

@then('header "{expected_header}" ends with "{expected_value}"')
@util.obtain_values
def then_header_ends_with(ctx:'Context', expected_header:'str', expected_value:'str') -> 'bool':
    value = ctx.zato.response.data.headers[expected_header]
    assert value.endswith(expected_value), 'Expected for header `{}` to end with `{}` but it\'s `{}`'.format(
        expected_header, expected_value, value)
    return True

# ################################################################################################################################

@then('header "{expected_header}" does not end with "{expected_value}"')
@util.obtain_values
def then_header_doesnt_end_with(ctx:'Context', expected_header:'str', expected_value:'str') -> 'bool':
    value = ctx.zato.response.data.headers[expected_header]
    assert not value.endswith(expected_value), 'Expected for header `{}` not to end with `{}` yet it\'s `{}`'.format(
        expected_header, expected_value, value)
    return True

# ################################################################################################################################
# ################################################################################################################################

@then('I store "{path}" from response under "{name}", default "{default}"')
@util.obtain_values
def then_store_path_under_name_with_default(ctx:'Context', path:'str', name:'str', default:'str') -> 'None':
    if ctx.zato.request.get('is_xml'):
        value = ctx.zato.response.data_impl.xpath(path)
        if value:
            if len(value) == 1:
                value = value[0].text
            else:
                value = [elem.text for elem in value]
        else:
            if default == No_Value:
                raise ValueError('No such path `{}`'.format(path))
            else:
                value = default
    else:
        value = get_pointer(ctx.zato.response.data_impl, path, default)
        if value == No_Value:
            raise ValueError('No such path `{}`'.format(path))

    ctx.zato.user_ctx[name] = value

# ################################################################################################################################

@then('I store "{path}" from response under "{name}"')
@util.obtain_values
def then_store_path_under_name(ctx:'Context', path:'str', name:'str') -> 'None':
    return then_store_path_under_name_with_default(ctx, path, name, No_Value)

# ################################################################################################################################
# ################################################################################################################################

def needs_json(func:'callable_'): # type: ignore
    def inner(ctx:'any_', **kwargs:'any_') -> 'None':
        if ctx.zato.request.get('response_format', ctx.zato.request.get('format', 'RAW')) != 'JSON':
            raise TypeError('This step works with JSON replies only.')
        return func(ctx, **kwargs)
    return inner

# ################################################################################################################################

def _response_is_equal_to(ctx:'Context', expected:'any_') -> 'bool':
    assert_equals(expected, ctx.zato.response.data_impl)
    return True

# ################################################################################################################################

@then('response is equal to that from "{path}"')
@needs_json
@util.obtain_values
def then_response_is_equal_to_that_from(ctx:'Context', path:'str') -> 'bool':
    return _response_is_equal_to(ctx, json.loads(util.get_data(ctx, 'response', path)))

# ################################################################################################################################

@then('JSON response is equal to "{expected}"')
@needs_json
@util.obtain_values
def then_response_is_equal_to(ctx:'Context', expected:'any_') -> 'bool':
    return _response_is_equal_to(ctx, json.loads(expected))

# ################################################################################################################################

#@then('response is equal to "{expected}"')
#@needs_json
#@util.obtain_values
#def then_response_is_equal_to(ctx:'Context', expected:'any_') -> 'None':
#    return _response_is_equal_to(ctx, expected)

# ################################################################################################################################
# ################################################################################################################################

@then('I sleep for "{sleep_time}"')
@util.obtain_values
def then_i_sleep_for(ctx:'Context', sleep_time:'int') -> 'None':
    time.sleep(float(sleep_time))

# ################################################################################################################################
# ################################################################################################################################

@given('I encode "{value}" using Base64 under "{name}"')
@util.obtain_values
def given_i_encode_value_using_base64_under_name(ctx:'Context', value:'str', name:'str') -> 'None':
    ctx.zato.user_ctx[name] = value.encode('base64','strict')

# ################################################################################################################################
# ################################################################################################################################

def variable_is(variable:'any_', value:'any_') -> 'None':
    expected_value = ast.literal_eval(value)
    assert variable == expected_value, 'Value `{}` is not equal to expected `{}`'.format(variable, expected_value)

# ################################################################################################################################

@then('variable "{variable}" is a list "{value}"')
@util.obtain_values
def and_variable_is_a_list(ctx:'Context', variable:'any_', value:'any_') -> 'None':
    variable_is(variable, value)

# ################################################################################################################################

@then('variable "{variable}" is an empty list')
@util.obtain_values
def and_variable_is_an_empty_list(ctx:'Context', variable:'any_') -> 'None':
    assert variable == [], 'Value `{}` is not an empty list'.format(variable)

# ################################################################################################################################

@then('variable "{variable}" is an integer "{value}"')
@util.obtain_values
def and_variable_is_an_integer(ctx:'Context', variable:'any_', value:'any_') -> 'None':
    variable_is(variable, value)

# ################################################################################################################################

@then('variable "{variable}" is a float "{value}"')
@util.obtain_values
def and_variable_is_a_float(ctx:'Context', variable:'any_', value:'any_') -> 'None':
    variable_is(variable, value)

# ################################################################################################################################

@then('variable "{variable}" is a string "{value}"')
@util.obtain_values
def and_variable_is_a_string(ctx:'Context', variable:'any_', value:'any_') -> 'None':
    assert variable == value, 'Value `{}` is not equal to expected `{}`'.format(variable, value)

# ################################################################################################################################

@then('variable "{variable}" is True')
@util.obtain_values
def and_variable_is_true(ctx:'Context', variable:'any_') -> 'None':
    variable_is(variable, 'True')

# ################################################################################################################################

@then('variable "{variable}" is False')
@util.obtain_values
def and_variable_is_false(ctx:'Context', variable:'any_') -> 'None':
    variable_is(variable, 'False')

# ################################################################################################################################
# ################################################################################################################################
