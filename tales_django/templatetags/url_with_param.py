from django.template.defaultfilters import register
import re


@register.simple_tag
def url_with_param(url, param, value):   # param_and_value):
    # param, value = param_and_value.split(',')

    if url.find(param) != -1:
        # If the url already contains the parameter, replace with the new value
        return re.sub(r'' + param + '=(.[^&]*)', str(param) + '=' + str(value), url)
    else:
        # check if the url contains a question mark(?) to determine which symbol to use
        symbol = '&' if url.find('?') != -1 else '?'
        return url + symbol + str(param) + '=' + str(value)


@register.filter
def add_w_comma(arg1, arg2):
    return str(arg1) + ',' + str(arg2)
