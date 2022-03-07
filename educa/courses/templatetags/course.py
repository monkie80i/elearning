from django import template

register  = template.Library()

@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None

@register.filter
def inc_one(obj):
    try:
        return obj+1
    except Exception as e:
        return None

@register.filter
def dec_one(obj):
    try:
        return obj-1
    except Exception as e:
        return None

@register.filter
def page_number_list(total_pages):
    try:
        if total_pages > 7:
            default = [1,2,3,4,5]
            print('More than 7')
            default.append(None)
            default.append[total_pages-1,total_pages]
        else:
            print('Less than 7')
            default = range(1,total_pages+1)
        return default
    except Exception as e:
        print(e)
        return None
    

    