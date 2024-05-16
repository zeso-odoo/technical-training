from odoo import models,fields,api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools import float_compare,float_is_zero

class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Estate Property Offer"
    _order="price desc"

    price=fields.Float(required=True)
    validity=fields.Integer(default=7)
    status=fields.Selection(
        copy=False,
        default=False,
        selection=[('accepted','Accepted'),('refused','Refused')]
    )
    date_deadline=fields.Date('Deadline',compute='_compute_date_deadline',inverse='_inverse_date_deadline')
   
    partner_id=fields.Many2one('res.partner',string='Partner',required=True)
    property_id=fields.Many2one('estate.property',string='Property',required=True)
    offer_ids=fields.Many2one('estate.property',string='Property Offer')
    property_type_id=fields.Many2one(related='property_id.property_type_id',string='Property Type')
    
    _sql_constraints=[
        ('check_offer_price','CHECK(price>0)','Price must be positive'),
    ]
    @api.depends('validity','create_date')
    def _compute_date_deadline(self):
        for record in self:
            date=record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline=date+relativedelta(days=record.validity)
    
    @api.depends('validity','create_date')
    def _inverse_date_deadline(self):
        for record in self:
            date=record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline-date).days


    def action_accept(self):
        if "accepted" in self.mapped("property_id.offer_ids.status"):
            # raise UserError("An offer as already been accepted")
        # self.status='accepted'
            self.property_id.offer_ids.status="refused"
        for record in self:
            record.status='accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        # for record in self:
        #     record.status='accepted'

    @api.model
    def create(self, vals):
        if vals.get("property_id") and vals.get("price"):
            prop = self.env["estate.property"].browse(vals["property_id"])
            if prop.offer_ids:
                max_offer = max(prop.mapped("offer_ids.price"))
                if float_compare(vals["price"], max_offer, precision_rounding=0.01) <= 0:
                    raise UserError("The offer must be higher than %.2f" % max_offer)
            prop.state = "offer_received"
        return super().create(vals)

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
    
   
