from odoo import models, fields
from datetime import date
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):   
    _name = 'estate.property'
    _description = 'Propiedad'

    name = fields.Char(string="Título", required=True)
    description = fields.Text(string="Descripción")  
    postcode = fields.Char(string="Código Postal")
    date_availability = fields.Date(
        string="Fecha disponibilidad",copy=False,
        default = date.today()+ relativedelta(months=3)
        ) 
    expected_price = fields.Float(string="Precio esperado")
    selling_price = fields.Float(string="Precio de venta",copy=False) 
    bedrooms = fields.Integer(string="Habitaciones", default=2)
    living_area = fields.Integer(string="Superficie cubierta")
    facades = fields.Integer(string="Fachadas")  
    garage = fields.Boolean(string="Garage")  
    garden = fields.Boolean(string="Jardín")  
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
                   ('sold','Vendido'),
                   ('canceled','Cancelado')],
        default ="new",           
        string="estado",
        copy = False,
        required =True
    )
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

    