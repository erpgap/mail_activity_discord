# models/res_config_settings.py

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    discord_bot_token = fields.Char(string="Discord Bot Token", config_parameter='discord.bot.token')
    discord_channel_id = fields.Char(string="Discord Channel ID", config_parameter='discord.channel.id')
