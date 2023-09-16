from django import template

register = template.Library()

@register.simple_tag
def call_method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)

@register.filter(name='split')
def split(value, arg):
    args = arg.split('__')
    split_ = [x for x in value.split(args[0]) if x]
    return split_[int(args[1])]