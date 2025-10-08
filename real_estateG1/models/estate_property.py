from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):   
    _name = 'estate.property'
    _description = 'Propiedad'

    # --------------------------------------- ATRIBUTOS ---------------------------------------------------

    name = fields.Char(string="Título", required=True)


    description = fields.Text(string="Descripción")  
    postcode = fields.Char(string="Código Postal")

    date_availability = fields.Date(
        string="Fecha disponibilidad",copy=False,
        default = date.today()+ relativedelta(months=3)
        ) 
    
    expected_price = fields.Float(string="Precio esperado", onchange="on_change_expected_price")

    selling_price = fields.Float(string="Precio de venta",copy=False) 

    bedrooms = fields.Integer(string="Habitaciones", default=2)

    living_area = fields.Integer(string="Superficie cubierta")

    facades = fields.Integer(string="Fachadas")  

    garage = fields.Boolean(string="Garage")  

    garden = fields.Boolean(string="Jardín", onchange="on_change_garden")  

    garden_orientation = fields.Selection(
        selection=[('north','Norte'),
                   ('south','Sur'),
                   ('east','Este'),
                   ('west','Oeste')],
        default="north",
        string="Orientación del jardín"
    )

    garden_area = fields.Integer(string="Superficie del jardín")  

    state = fields.Selection(
        selection=[('new','Nuevo'),
                  ('offer received','Oferta recibida'),
                   ('offer accepted','Oferta aceptada'),
                   ('sold','Vendida'),
                   ('canceled','Cancelado')],
        default ="new",           
        string="estado",
        copy = False,
        required =True
    )

    
    # --------------------------------------- RELACIONES ---------------------------------------------------

    property_type_id = fields.Many2one(
        comodel_name ='estate.property.type',
        string ='Tipo propiedad',
        required = True
    )

    buyer_id = fields.Many2one(
        comodel_name ='res.partner',   #es un campo propio de odoo que se utiliza para representar cualquier entidad con la que interactua nuestra empresa
        string = 'Comprador',
    )    

    salesman_id = fields.Many2one(
        comodel_name ='res.users',  #representa a las personas que tienen acceso al sistema odoo ej: nosotros creando un registro en el back
        string ='Vendedor',
        copy= False,
        default=lambda self: self.env.user,  # usuario logueado por defecto
    )

    tag_ids= fields.Many2many(
        'estate.property.tag',
        string="Etiquetas"
    )

    offer_ids = fields.One2many(
        comodel_name = "estate.property.offer",
        inverse_name = "property_id",
        string = "Ofertas"
    )

    # --------------------------------------- ATRIBUTOS COMPUTADOS ---------------------------------------------------
    
    total_area = fields.Integer(string = "Área total", compute = "_compute_total_area", store = True)

    best_offer = fields.Float(string = "Mejor oferta", compute = "_compute_best_offer", store = True)


    #FUNCIONES
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area
    
    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for rec in self:

            offers = rec.offer_ids.mapped("price")

            if offers:
                rec.best_offer = max(offers)
            else:
                rec.best_offer = 0
               
    @api.onchange('garden')
    def _on_change_garden(self):
        if self.garden:
            self.garden_area=10
        else:
            self.garden_area=0
            
    @api.onchange('expected_price')
    def _on_change_expected_price(self):
        result={}
        if self.expected_price  and self.expected_price < 10000 :
            raise UserError("El precio ingresado es bajo.")
        return result      

# --------------------------------------- ACCIONES ----------------------------------------------------------
    def action_mark_as_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("No se puede marcar como vendida una propiedad cancelada.")
            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("No se puede cancelar una propiedad vendida.")
            record.state = 'canceled'
        return True
 



                