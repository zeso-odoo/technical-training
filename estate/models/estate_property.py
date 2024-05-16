from odoo import api,fields,models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError,ValidationError
from odoo.tools import float_compare,float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _inherit = ['mail.thread']

    _order="id desc"
    _sql_constraints=[
        ('check_expected_price','CHECK(expected_price>0)','Expected Price must be positive'),
        ('check_selling_price','CHECK(selling_price>=0)','Selling price must be positive')
    ]
    name = fields.Char(default='unknown')
    description = fields.Char(string='Description')
    postcode = fields.Char()
    expected_price = fields.Float(required=True,tracking=True)
    selling_price = fields.Float(readonly=True, copy=False)
    date_availability = fields.Date(string='Date of Availability', default=fields.Date.today()+relativedelta(months=3),copy=False)
    bedrooms = fields.Integer(default=2)  # Corrected typo in the field name
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    living_area = fields.Integer('Living Area (sqm)')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        
    ) 
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [('new', 'New'), ('offer_received', 'Offer Received'),('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'), ('canceled', 'Canceled')],
        required=True, copy=False, default="new"
    )
    image=fields.Image(string='image')
    property_type_id=fields.Many2one('estate.property.type', string='Property Type')
    salesman_id=fields.Many2one('res.users',string='Salesman')
    buyer_id=fields.Many2one('res.partner',string='Buyer',readonly=True,copy=False)
    tag_ids=fields.Many2many('estate.property.tag',string='Tags')
    offer_ids=fields.One2many('estate.property.offer','property_id',string='Offers')
    best_price = fields.Integer(compute='_compute_best_price')
    total_area = fields.Integer(compute='_compute_total_area')

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price')) if property.offer_ids else 0
            
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if record.state=='canceled':
                print(record)
                raise UserError('Property cannot be sold')
            elif record.state=='new':
                record.state='sold'

    def action_cancel(self):
        for record in self:
            if record.state=='sold':
                raise UserError('Sold property cannot be canceled')
            elif record.state=='new':
                record.state='canceled'

    @api.constrains('expected_price','selling_price')
    def _check_selling_price(self):
        print("\n\n", self, "\n\n")
        for rec in self:
            if not float_is_zero(rec.selling_price,precision_rounding=0.01) and float_compare(rec.selling_price,rec.expected_price*0.9,precision_rounding=0.01)<0:
                raise ValidationError(
                        "The selling price must be at least 90% of the expected price! "
                        + "You must reduce the expected price if you want to accept this offer."
                    )
    
    @api.ondelete(at_uninstall=False)
    def _unlink_except_offer_accept(self):
        for record in self:
            if record.state!='new' and record.state!='canceled':
                raise UserError("You Can Only delete new or canceled property")

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
    
    def action_add_offer(self):
        return {
            'type':'ir.actions.act_window',
            'name':'Add offer',
            'res_model':'estate.property.add_offer.wizard',
            'view_mode':'form',
            'target':'new',
            'context':{'default_property_id':self.id},
        }