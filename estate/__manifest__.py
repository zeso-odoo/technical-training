{
    'name': 'ESTATE',
    'version': '1.0',
    'summary': 'Buy for property',
    'description': 'We provide best rate for your property',
    'website': 'https://www.odoo.com/app/estate',
    'category':'Estate/Brokerage',
    'license': 'LGPL-3',

    'depends': [
        'base','mail','website',
    ],
    'data': [
        'security/estate_security.xml',
        'security/ir.model.access.csv',

        'wizard/estate_property_multiple_offer_views.xml',

        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',

        'views/estate_property_offer_views.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_views.xml', 
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],
    'demo':[
        'demo/estate_property_demo_data.xml',
        'demo/estate_property_type_data.xml',
        'demo/property_tag.xml',
    ],
    'installable': True,
    'application': True,
}

