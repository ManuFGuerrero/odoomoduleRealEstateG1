from odoo import models, fields, api
from datetime import timedelta, date

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Oferta sobre propiedad"
    name = fields.Char(string = "Nombre", required = True)
    price = fields.Float(string = "Precio")
    validity  = fields.Integer(string = "Validez(dias)", default = 7)
    date_deadline = fields.Date (string = "Fecha limite", compute ="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)
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

    property_type = fields.Char(related='property_id.property_type_id.name')


    #email = fields.Char(related='partner_id.email')


        #TODO verificar computo
  
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = (record.create_date + timedelta(days=record.validity))
            else:
                record.date_deadline = False

    @api.depends("create_date", "validity")
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days
           