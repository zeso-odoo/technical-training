from odoo import models,fields,api

class EstateProperty(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order='name'
    name = fields.Char(name='Hous in surat')  
    sequence=fields.Integer('Sequence',default=1)   
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids=fields.One2many("estate.property.offer","property_type_id",string="offers")
    offer_count=fields.Integer(compute='_compute_offer_count')
    _sql_constraints=[
        ('unique_type_name','UNIQUE(name)','name must be unique')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count=len(record.offer_ids)

    def action_open_related_offers(self):
        return{
            'type':'ir.actions.act_window',
            'name':'offers',
            'res_model':'estate.property.offer',
            'view_mode':'tree,form',
            'domain':[('property_type_id','=','self.id')]
        }