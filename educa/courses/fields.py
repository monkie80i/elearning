from dataclasses import field
from webbrowser import get
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class OrderField(models.PositiveIntegerField):
    """
    1. You check whether a value already exists for this field in the model instance.
    You use self.attname, which is the attribute name given to the field in the
    model. If the attribute's value is different to None, you calculate the order you
    should give it as follows:
        1. You build a QuerySet to retrieve all objects for the field's model. You
        retrieve the model class the field belongs to by accessing self.model.
        2. If there are any field names in the for_fields attribute of the field,
        you filter the QuerySet by the current value of the model fields in
        for_fields. By doing so, you calculate the order with respect to
        the given fields.
        3. You retrieve the object with the highest order with last_item =
        qs.latest(self.attname) from the database. If no object is found,
        you assume this object is the first one and assign the order 0 to it.
        4. If an object is found, you add 1 to the highest order found.
        5. You assign the calculated order to the field's value in the model
        instance using setattr() and return it.
    2. If the model instance has a value for the current field, you use it instead
    of calculating it.
    """
    def __init__(self,for_fields=None,*args,**kwargs):
        self.for_fields = for_fields
        super().__init__(*args,**kwargs)
    
    def pre_save(self, model_instance, add):
        if getattr(model_instance,self.attname) is None:
            #no current value
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    #filter by objecs with the same field values
                    #for the fields in the "for_fields"
                    query = {field:getattr(model_instance,field) for field in self.for_fields}
                    qs = qs.filter(**query)
                #get the order of the latest item
                last_item = qs.latest(self.attname)
                value = last_item.order+1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance,self.attname,value)
            return value
        else:
            return super().pre_save(model_instance, add)