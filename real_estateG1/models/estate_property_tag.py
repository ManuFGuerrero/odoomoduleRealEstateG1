from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Etiqueta de Propiedad"
    name = fields.Char(string = "Nombre", required = True) 



    #constraints
    _sql_constraints = [
        ('unique_tag_name','UNIQUE(name)','El nombre de la etiqueta debe de ser unico')
    ]
    
    
