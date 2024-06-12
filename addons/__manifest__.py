# __manifest__.py

{
    'name': 'Discord Bot',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Module to send Odoo activities to Discord',
    'description': 
    """
    This module sends Odoo activities to Discord using a bot.
    """,

    'author': 'Eduardo Esteves',
    'website': 'https://www.erpgap.com',

    'depends': [
        'base',
        'base_setup',
        'mail',
        'crm'
    ],

    'data': [
        #security
        'security/ir.model.access.csv',
        #'securiy/access_rights.xml',
        #data
        'data/ir_cron_data.xml',
        #views
        'views/res_config_settings_views.xml',
        'views/mail_activity_views.xml',
        'views/res_users_views.xml'
    ],

    'installable': True,
    'application': True,

    'license': 'LGPL-3',
}