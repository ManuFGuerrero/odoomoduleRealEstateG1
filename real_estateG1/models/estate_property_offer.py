from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Oferta sobre propiedad"

    name = fields.Char(string = "Nombre", required = True)
    price = fields.Float(string = "Precio")
    status = fields.Selection(
        selection=[('accepted','Aceptado'),
                   ('refused','Rechazado'),
                    ],
        string="Estado",
        default='refused'
    )

    partner_id = fields.Many2one(
        comodel_name ='res.partner',
        string ='Ofertante',
        required = True
    )

    property_id  = fields.Many2one(
        comodel_name ='estate.property',
        string ='Propiedad',
        required = True
    )

