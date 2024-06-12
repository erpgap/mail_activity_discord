# -*- coding: utf-8 -*-

from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"

    discord_handler = fields.Char(string='Discord User Handler')
    
