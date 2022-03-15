from django import template
from requests import Request
from urllib.parse import urlparse, parse_qs

def get_yt_video_id(url):
    """Returns Video_ID extracting from the given url of Youtube
    
    Examples of URLs:
      Valid:
        'http://youtu.be/_lOT2p_FCvA',
        'www.youtube.com/watch?v=_lOT2p_FCvA&feature=feedu',
        'http://www.youtube.com/embed/_lOT2p_FCvA',
        'http://www.youtube.com/v/_lOT2p_FCvA?version=3&amp;hl=en_US',
        'https://www.youtube.com/watch?v=rTHlyTphWP0&index=6&list=PLjeDyYvG6-40qawYNR4juzvSOg-ezZ2a6',
        'youtube.com/watch?v=_lOT2p_FCvA',
      
      Invalid:
        'youtu.be/watch?v=_lOT2p_FCvA',
    """

    if url.startswith(('youtu', 'www')):
        url = 'http://' + url
        
    query = urlparse(url)
    
    if 'youtube' in query.hostname:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        elif query.path.startswith(('/embed/', '/v/')):
            return query.path.split('/')[2]
    elif 'youtu.be' in query.hostname:
        return query.path[1:]
    else:
        raise ValueError

register  = template.Library()



@register.inclusion_tag('my-tags/embed_youtube.html')
def embed_youtube_tag(watch_url ,*args, **kwargs):
    try:
        """embed_str = '/embed/'
        watch_str = '/watch?v='
        embed_url = embed_str.join(watch_url.split(watch_str))

        if embed_url.find('youtu.be') != -1:
            #print("nop")
            v_id = embed_url.split('/')[-1]
            embed_url = "https://www.youtube.com/embed/"+v_id
        """
        #print(embed_url,22)
        v_id = get_yt_video_id(watch_url)
        embed_url = "https://www.youtube.com/embed/"+v_id

        params = {}
        options = ['autoplay','mute']

        for option in options:
            if option in args:
                params[option] = 1

        pre_url = Request(url=embed_url,params=params)
        embed_url = pre_url.prepare().url

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
    