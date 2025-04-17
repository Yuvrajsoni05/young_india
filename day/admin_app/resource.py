from import_export import resources
from .models import Member_details




class Member_Detail_Resource(resources.ModelResource):
    class meta:
        model = Member_details
        