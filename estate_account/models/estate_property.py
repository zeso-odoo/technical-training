from odoo import fields,models

class EstateProperty(models.Model):
    _inherit='estate.property'

    
    def action_sold(self):
        res=super().action_sold()
        journal=self.env["account.journal"].search([("type","=","sale")],limit=1)

        for rec in self:
            self.env["account.move"].create(
                {
                    "partner_id":rec.buyer_id.id,
                    "move_type":"out_invoice",
                    "journal_id":journal.id,
                    "invoice_line_ids":[
                        (0,0,{"name":rec.name,"quantity":1.0,"price_unit":rec.selling_price*6.0/100.0,},),
                        (0,0,{"name":"Administrative fees","quantity":1.0,"price_unit":100.0,},),
                    ],
                }
            )
        return res
                