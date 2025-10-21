from odoo import Command, models

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_mark_as_sold (self):
        
        for property in self:
            self.env["account.move"].create({

                "partner_id": property.buyer_id.id,
                "move_type": "out_invoice",
                "property_id" : property.id,
                "line_ids":[

                    Command.create({
                        "name": property.name,
                        "quantity": 1,
                        "price_unit": property.selling_price
                    }),

                    Command.create({
                        "name": "Gastos administrativos",
                        "quantity": 1,
                        "price_unit": 100,
                    })
                
                ],
            })
        return super().action_mark_as_sold() 
    

