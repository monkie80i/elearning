from django import template

register  = template.Library()

def get_pages_range(total_pages,page_number):
    lower = 3
    higher = total_pages-1
    tail = [higher,total_pages]
    if total_pages>7:
        if page_number < lower+2 :
            pages_list = [i for i in range(1,lower+3)]+[None]+tail
        else:
            pages_list = [i for i in range(1,lower+1)]
            if page_number > higher-2:
                pages_list += [None]+[i for i in range(higher-1,total_pages+1)]
            else:
                pages_list += [None]+[i for i in range(page_number-1,page_number+2)]+[None]+tail
    else:
        pages_list = range(1,total_pages+1)
    return pages_list

@register.inclusion_tag('my-tags/pagination.html')
def pagination_tag(total_pages,page_number,pagination_url,*args, **kwargs):
    try:
        return_obj = {
            'total_pages':total_pages,
            'page_number':page_number,
        }  
        prev_page = pagination_url+str(page_number-1)+'/'
        next_page = pagination_url+str(page_number+1)+'/'
        page_number_list = get_pages_range(total_pages,page_number)
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