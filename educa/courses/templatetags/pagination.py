from django import template

register  = template.Library()

@register.inclusion_tag('my-tags/pagination.html',takes_context=False)
def pagination(total_pages,page_number):
    try:
        return_obj = {
            'total_pages':total_pages,
        }  
    except Exception as e:
        #print(e)
        return None
    