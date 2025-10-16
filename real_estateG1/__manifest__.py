{
    'name': 'Inmobiliaria',
    'version': '1.0',
    'author': 'Alfredo, Ramiro, Manuel',
    'category': 'Real Estate',
    'depends': ['base'],
    'data': [
        'security/real_estate_res_groups.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_users_views.xml',
        'views/real_estate_menuitem.xml',
        
    ],          # para las vistas
    'installable': True,  
    'application': True,  # para que aparezca en Apps

}