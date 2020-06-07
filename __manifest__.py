# -*- coding: utf-8 -*-
{
    'name': "Hospital Management",

    'summary': """
        Module for managing the hospitals
        """,

    'description': """
        * Module for managing the hospitals *
    """,

    'author': "GBS",
    'website': "http://www.gbs.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'extra-addons',
    'version': '13.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/patient.xml',
        'views/appointment.xml',
        'views/templates.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
