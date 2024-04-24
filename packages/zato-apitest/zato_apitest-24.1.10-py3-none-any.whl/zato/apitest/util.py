# -*- coding: utf-8 -*-

"""
Copyright (C) 2024, Zato Source s.r.o. https://zato.io

Proprietary product. This is not open source software, reproduction is prohibited.
"""

# stdlib
import csv, operator, os, random, uuid, re
from collections import OrderedDict
from datetime import timedelta
from io import StringIO
from itertools import zip_longest

# Arrow
from arrow import api as arrow_api

# Bunch
from bunch import Bunch, bunchify

# ConfigObj
from configobj import ConfigObj # type: ignore

# Dateutil
from dateutil.parser import parse as parse_dt

# Zato
from zato.apitest import version

random.seed()

# Singleton used for storing Zato's own context across features and steps.
# Not thread/greenlet-safe so this will have to be added if need be.
context = Bunch()

# ################################################################################################################################
# ################################################################################################################################

if 0:
    from zato.apitest.typing_ import any_, anydict, anylist, callable_, intlist, strlist

# ################################################################################################################################
# ################################################################################################################################

Context = Bunch

# ################################################################################################################################
# ################################################################################################################################

def get_value_from_environ(ctx:'Context', name:'str') -> 'str':
    return os.environ[name]

# ################################################################################################################################
# ################################################################################################################################

def get_value_from_ctx(ctx:'Context', name:'str') -> 'str':
    return ctx.zato.user_ctx[name]

# ################################################################################################################################
# ################################################################################################################################

def get_value_from_config(ctx:'Context', name:'str') -> 'str':
    return ctx.zato.user_config[name]

# ################################################################################################################################
# ################################################################################################################################

def get_value_from_vault(ctx:'Context', name:'str') -> 'str':
    """ Returns a selected value from Vault. Will use default Vault connection unless a specific one was requested.
    """
    client = ctx.zato.vault_config['default'].client
    path = name.replace('vault:', '', 1)
    return client.read(path)['data']['value']

# ################################################################################################################################
# ################################################################################################################################

config_functions = {
    '$': get_value_from_environ,
    '#': get_value_from_ctx,
    '@': get_value_from_config,
    'vault:': get_value_from_vault,
}

# ################################################################################################################################
# ################################################################################################################################

def obtain_values(func:'callable_') -> 'any_': # type: ignore
    """ Functions decorated with this one will be able to obtain values from config sources prefixed with $, # or @.
    """
    def inner(ctx:'Context', *args:'any_', **kwargs:'any_'):

        def replacer(match:'any_'):
            config_key = match.groups()[1]
            config_func = config_functions[config_key]
            return str(config_func(ctx, match.groups()[2]))

        for kwarg, value in kwargs.items():
            if value:
                for config_key in config_functions:
                    if value.startswith(config_key):
                        config_func = config_functions[config_key]
                        kwargs[kwarg] = config_func(ctx, value[1:] if len(config_key) == 1 else value)
                        break
                else:
                    kwargs[kwarg] = re.sub(r'((\$|\#|\@)\{(\w+)\})', replacer, value)

        return func(ctx, *args, **kwargs)
    return inner

# ################################################################################################################################
# ################################################################################################################################

def new_context(old_ctx:'Context', environment_dir:'str', user_config:'any_'=None) -> 'Context':
    _context = Bunch()
    _context.auth = {}
    _context.user_ctx = {}
    _context.date_formats = {'default':'YYYY-MM-DDTHH:mm:ss'}
    _context.environment_dir = old_ctx.zato.environment_dir if old_ctx else environment_dir
    _context.request = Bunch()
    _context.request.headers = {'User-Agent':'zato-apitest/{} (+https://zato.io)'.format(version)}
    _context.request.ns_map = {}
    _context.cassandra_ctx = {}

    config_ini = bunchify(ConfigObj(os.path.join(_context.environment_dir, 'config.ini')))
    _context.user_config = user_config if user_config is not None else config_ini['user'] # type: ignore

    context.clear()
    context.update(_context)

    return context

# ################################################################################################################################
# ################################################################################################################################

def get_full_path(base_dir:'str', *path_items:'str') -> 'str':
    return os.path.normpath(os.path.join(base_dir, *path_items))

# ################################################################################################################################

def get_file(path:'str') -> 'str':
    return open(path).read()

# ################################################################################################################################

def get_data(ctx:'Context', req_or_resp:'str', data_path:'str') -> 'str':

    full_path = get_full_path(
        ctx.zato.environment_dir,
        ctx.zato.request.get('response_format', ctx.zato.request.get('format', 'RAW')).lower(),
        req_or_resp,
        data_path
    )

    data = get_file(full_path) if data_path else ''

    if ctx.zato.request.format == 'XML' and not data:
        raise ValueError('No {} in `{}`'.format(req_or_resp, data_path))

    return data

# ################################################################################################################################
# ################################################################################################################################

def parse_list(value:'str') -> 'anylist':
    return [elem.strip() for elem in tuple(csv.reader(StringIO(value)))[0]]

# ################################################################################################################################

def any_from_list(value:'str') -> 'any_':
    return random.choice(tuple(elem.strip() for elem in parse_list(value) if elem))

# ################################################################################################################################
# ################################################################################################################################

def rand_string(count:'int'=1) -> 'str | strlist':
    # First character is 'a' so it nevers starts with a digit.
    # Some parsers will insist a string is an integer if they notice a digit at idx 0.
    if count == 1:
        return 'a' + uuid.uuid4().hex
    else:
        return ['a' + uuid.uuid4().hex for _ in range(count)]

# ################################################################################################################################

def rand_int(min:'int'=0, max:'int'=100, count:'int'=1) -> 'int | intlist':
    if count == 1:
        return random.choice(range(min, max))
    else:
        return [random.choice(range(min, max)) for _ in range(count)]

# ################################################################################################################################

def rand_float(min:'int'=0, max:'int'=100) -> 'float':
    return float(rand_int(min, max)) + random.random() # type: ignore

# ################################################################################################################################

def rand_date(format:'str', start:'any_'=None, stop:'any_'=None) -> 'str | None':
    if not (start and stop):
        # Now is as random as any other date
        return now(format)

# ################################################################################################################################
# ################################################################################################################################

def now(format:'str') -> 'str':
    return arrow_api.now().format(format)

# ################################################################################################################################

def utcnow(format:'str') -> 'str':
    return arrow_api.utcnow().format(format)

# ################################################################################################################################

def utcnow_minus_hour(format:'str') -> 'str':
    utc = arrow_api.utcnow()
    return utc.replace(hours=-1).format(format)

# ################################################################################################################################
# ################################################################################################################################

def date_after_before(base_date:'str', format:'str', direction:'str', limit:'float', needs_parse:'bool'=True) -> 'str':
    if needs_parse:
        base_date = parse_dt(base_date) # type: ignore

    days=rand_int(0, abs(limit)) # type: ignore
    return arrow_api.get(direction(base_date, timedelta(days=days))).format(format) # type: ignore

# ################################################################################################################################

def date_after(base_date:'str', format:'str', limit:'int'=100000, needs_parse:'bool'=True) -> 'str':
    return date_after_before(base_date, format, operator.add, limit, needs_parse) # type: ignore

# ################################################################################################################################

def date_before(base_date:'str', format:'str', limit:'int'=100000, needs_parse:'bool'=True) -> 'str':
    return date_after_before(base_date, format, operator.sub, limit, needs_parse) # type: ignore

# ################################################################################################################################

def date_between(start_date:'str', end_date:'str', format:'str') -> 'str':
    start_date = parse_dt(start_date) # type: ignore
    end_date = parse_dt(end_date) # type: ignore

    diff = int((start_date - end_date).days) # type: ignore
    func = date_after if end_date > start_date else date_before
    return func(start_date, format, diff, False)

# ################################################################################################################################
# ################################################################################################################################

comparison_operators = {
    'equal to': '=',
    'not equal to': '!=',
    'less than': '<',
    'greater than': '>',
    'less or equal to': '<=',
    'greater or equal to': '>='
}

# ################################################################################################################################

def wrap_into_quotes(values:'str') -> 'str':
    return '\'{}\''.format('\', \''.join(values.split(', ')))

# ################################################################################################################################

def make_dict(*args:'any_') -> 'anydict':
    components = []
    phrases = OrderedDict()
    for item in args:
        components.append([segment.strip() for segment in item.split(',')])
    for items in zip_longest(*components):
        phrases[items[0]] = items[1:]
    return phrases

# ################################################################################################################################

def build_filter(*args:'any_') -> 'str':
    filter_dict = make_dict(*args)
    filter_ = ''
    for i, key in enumerate(filter_dict.keys()):
        operator = comparison_operators[filter_dict[key][0]]
        if filter_dict[key][2] is not None:
            join_by = filter_dict[key][2]
        if i == 0:
            filter_ += "WHERE %s%s'%s' " % (key, operator, filter_dict[key][1])
        else:
            filter_ += "%s %s%s'%s' " % (join_by, key, operator, filter_dict[key][1]) # type: ignore
    return filter_

# ################################################################################################################################
# ################################################################################################################################
