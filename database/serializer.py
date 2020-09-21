from .db import ma

class __UserSchema(ma.Schema):
    '''
    Helps to serialise the USer model
    '''
    class Meta:
        fields = ("id", "email") # only these are exposed

class __CompanySchema(ma.Schema):
    '''
    Helps to serialise the the company model
    '''
    class Meta:
        fields = ("id", "c_name", "c_addr", "contact_name", "contact_email", "product", "is_form_done", "form_data") # only these are exposed

class __MsgSchema(ma.Schema):
    '''
    Helps to serialise the messaege model
    '''
    class Meta:
        # Fields to expose
        fields = ("id", "c_id", "msg", "tstamp", "by") # only these are exposed

### Below are the objets used to dump the queried content
user_schema = __UserSchema()
users_schema = __UserSchema(many=True)
comp_schema = __CompanySchema()
comps_schema = __CompanySchema(many=True)
msgs_schema = __MsgSchema(many=True)
