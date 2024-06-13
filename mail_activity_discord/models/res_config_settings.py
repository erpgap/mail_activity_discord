# models/res_config_settings.py

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    discord_bot_token = fields.Char(string="Discord Bot Token", config_parameter="base_setup.discord_bot_token")
    discord_channel_id = fields.Char(string="Discord Channel ID", config_parameter="base_setup.discord_channel_id")
