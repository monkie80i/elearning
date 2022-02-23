from dataclasses import field
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class OrderField(models.PositiveIntegerField):
    def __init__(self,for_field=None,*args,**kwargs):
        self.for_field = for_field
        super().__init__(*args,**kwargs)
    
    def pre_save(self,model_instance, add):
        if getattr(model_instance,self.attname) is None:
            #if the order field value is None
            try:
                qs = self.model.objects.all()
                if self.for_field:
                    field  = getattr(model_instance,self.for_field)
                    query = {self.for_field:field}
                    qs = qs.filter(**query)
                last_item = qs.latest(self.attname)
                value = getattr(last_item,self.attname) + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance,self.attname,value)
            return value    
        else:
            return super().pre_save(model_instance, add)
