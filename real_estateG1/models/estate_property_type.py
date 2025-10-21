from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Tipo de Propiedad"
    name = fields.Char(string = "Nombre", required = True) 


    #constraints
    _sql_constraints = [
        ('unique_type','UNIQUE(name)','Solo puede existir un tipo de propiedad con el mismo nombre')
    ]

