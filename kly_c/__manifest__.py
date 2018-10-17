{
    'name': 'kly',
    'version': '1.0',
    'category': 'website',
    'description': """""",
    'summary': 'Story teller',
    'author': 'Desmarets Colin',
    'website': 'https://www.nubeo.be',
    'depends': [
        'base',
        'web',
        'contacts',
        'website',
    ],
    'data': [
        'security/ir.model.access.csv',
        'datas/menus.xml',
        'views/inventory_views.xml',
        'views/templates.xml',
        'views/assets.xml',
    ],
    'qweb': [
    ],  
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 0,
}
