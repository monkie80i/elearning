from django import template
from requests import Request
register  = template.Library()



@register.inclusion_tag('my-tags/embed_youtube.html')
def embed_youtube_tag(watch_url ,*args, **kwargs):
    try:
        embed_str = '/embed/'
        watch_str = '/watch?v='
        embed_url = embed_str.join(watch_url.split(watch_str))

        if embed_url.find('youtu.be') != -1:
            #print("nop")
            v_id = embed_url.split('/')[-1]
            embed_url = "https://www.youtube.com/embed/"+v_id
        params = {}
        options = ['autoplay','mute']

        for option in options:
            if option in args:
                params[option] = 1

        pre_url = Request(url=embed_url,params=params)
        embed_url = pre_url.prepare().url
        #print(embed_url,22)

        if 'class_name' in kwargs:
            class_name = kwargs['class_name']
            #print("class name exits",class_name)
        else:
            #print("No class detected")
            class_name = ""
        
        return_obj = {
            'url':embed_url,
            'class_name':class_name
        } 
        
        return return_obj
    except Exception as e:
        print(e)
        return None
    