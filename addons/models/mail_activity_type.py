# -*- coding: utf-8 -*-

from odoo import models, fields

class MailActivityType(models.Model):
    _inherit = 'mail.activity.type'

    discord_connector = fields.Boolean(string='Discord Connector', help='Does this activity type should be connected to Discord?')
