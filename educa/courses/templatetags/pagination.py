from django import template

register  = template.Library()

@register.inclusion_tag('my-tags/pagination.html')
def pagination_tag(total_pages,page_number,pagination_url,*args, **kwargs):
    try:
        return_obj = {
            'total_pages':total_pages,
            'page_number':page_number,
        }  
        prev_page = pagination_url+str(page_number-1)+'/'
        next_page = pagination_url+str(page_number+1)+'/'
        print(next_page,prev_page)
        page_number_list = range(1,total_pages+1)
        return_obj['prev_page'] = prev_page
        return_obj['next_page'] = next_page
        return_obj['page_number_list'] = page_number_list
        return_obj['pagination_url'] = pagination_url
        return return_obj
    except Exception as e:
        print(e)
        return None
    
@register.inclusion_tag('my-tags/test.html')
def test_cat():
    return {'var':'cat'}