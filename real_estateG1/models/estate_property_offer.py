from odoo import models, fields, api
from datetime import timedelta, date
from odoo.exceptions import UserError

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

    property_type = fields.Char(related='property_id.property_type_id.name', stored=True)

# --------------------------------------- COMPUTADOS ----------------------------------------------------------
  
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.validity:
                record.date_deadline = fields.Datetime.now() + timedelta(days=record.validity)
            else:
                record.date_deadline = False

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days
                


#Onchange creado para que la interfaz sea mas "amigable", no habia mucha performance en que la validity se actualice tarde

    @api.onchange('date_deadline')
    def _on_change_date_deadline(self):
        for record in self:
            if fields.Datetime.now() and record.date_deadline:
                delta = record.date_deadline - fields.Datetime.now().date()
                record.validity = max(delta.days, 0)  # Para evitar numeros negativos
            else:
                record.validity = 0
                
# --------------------------------------- ACCIONES ----------------------------------------------------------
    def action_accept_offer(self):
        #1-Si la propiedad ya tiene una oferta aceptada , error - Si la propiedad ya esta vendida/cancelada , error
        if self.property_id.offer_ids.filtered(lambda p: p.status=="accepted"):
            raise UserError("Esta propiedad ya tiene una oferta aceptada.")
        if self.property_id.state in ['sold', 'canceled']:
                raise UserError("No se puede aceptar ofertas para una propiedad vendida o cancelada.")
        
        #2-Aceptar la oferta
        self.status="accepted"
        
        #3-Actualizar datos de propiedad
        self.property_id.state="offer accepted"
        self.property_id.buyer_id=self.partner_id
        self.property_id.selling_price=self.price
        
        return True
    
    #Por default todas estan en reject, no hace falta rechazarlas
    #def action_reject_offers(self, accepted_offer):
    #   self.filtered(lambda o: o.property_id == accepted_offer.property_id and o.id != accepted_offer.id).write({"status": "refused"})   