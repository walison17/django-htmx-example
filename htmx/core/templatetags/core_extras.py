from urllib.parse import urlencode

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def order_querystring(context, order_option, field):
    query_dict = context['request'].GET.dict().copy()
    query_dict.update(order=field, dir='asc')
    if order_option.field == field:
        query_dict['dir'] = 'asc' if order_option.direction == 'desc' else 'desc'

    return urlencode(query_dict)


@register.simple_tag(takes_context=True)
def merge_querystring(context, *, exclude_param=None, **kwargs):
    query_dict = context['request'].GET.dict().copy()
    if exclude_param is not None:
        try:
            del query_dict[exclude_param]
        except KeyError:
            pass

    for k, v in kwargs.items():
        query_dict[k] = v

    return urlencode(query_dict)


@register.filter
def split_numbers(nums_string, separator=','):
    return map(int, nums_string.split(separator))
