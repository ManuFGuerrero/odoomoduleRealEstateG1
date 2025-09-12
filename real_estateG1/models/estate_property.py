from odoo import models, fields
from datetime import date
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):   
    _name = 'estate.property'
    _description = 'Propiedades'

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
        selection=[('new','nuevo'),
                  ('offer received','oferta recibida'),
                   ('offer accepted','oferta aceptada'),
                   ('sold','vendido'),
                   ('canceled','candelado')],
        default ="new",           
        strings="estado",
        copy = False
    )