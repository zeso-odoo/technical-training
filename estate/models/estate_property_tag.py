from odoo import models,fields

class EstateProperty(models.Model):
    _name="estate.property.tag"
    _description="Property Tag"
    _order='name'

    name=fields.Char(default="Property tag")
    color=fields.Integer(default=1)

    _sql_constraints=[
        ('unique_tag_name','UNIQUE(name)','The must be unique'),
    ]
    
    
   