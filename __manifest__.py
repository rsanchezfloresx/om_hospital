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
    'depends': ['sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence.xml',
        'data/cron.xml',
        'wizards/create_appointment.xml',
        'views/patient.xml',
        'views/appointment.xml',
        'views/doctor.xml',
        'views/templates.xml',
        'views/lab.xml',
        'views/sale_order.xml',
        'views/settings.xml',
        'reports/report.xml',
        'reports/patient_card.xml',
        'reports/sale_report_inherit.xml',
        'reports/appointment.xml',
        'data/mail_template.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
