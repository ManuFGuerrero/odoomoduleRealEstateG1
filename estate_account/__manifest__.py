{
    'name': 'Real Estate Invoicing',
    'version': '1.0',
    'author': 'Alfredo, Ramiro, Manuel',
    'category': 'Estate Account',
    'depends': ['account', 'real_estateG1','base'],
    'data': [
        'views/account_move_views.xml'
    ],          # para las vistas
    'installable': True,  
    'application': True,  # para que aparezca en Apps

}