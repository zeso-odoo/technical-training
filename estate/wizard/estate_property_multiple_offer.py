from odoo import fields,models,api

class EstateMultipleOffer(models.TransientModel):
    _name="estate.property.add.offer"
    _description="Wizard to make offers to multiple properties at once"

    price=fields.Integer(string="price")
    validity=fields.Integer(string="Validity",default=9)
    partner_id=fields.Many2one("res.partner",copy=False)

    def action_make_offers_wizard(self):
        property_ids=self.env.context.get('active_ids',[])
        property_rec=self.env['estate.property'].browse(property_ids)
        for property in property_rec:
            partner=self.env['estate.property.offer'].create({
                'price':self.price,
                'partner_id':self.partner_id.id,
                'property_id':property.id,
                'validity':self.validity,
                'property_type_id':property.property_type_id.id
            })
        return True