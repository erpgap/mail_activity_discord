# models/res_config_settings.py

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    discord_bot_token = fields.Char(string="Discord Bot Token")
    discord_channel_id = fields.Char(string="Discord Channel ID")

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('discord.bot.token', self.discord_bot_token)
        self.env['ir.config_parameter'].sudo().set_param('discord.channel.id', self.discord_channel_id)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            discord_bot_token=self.env['ir.config_parameter'].sudo().get_param('discord.bot.token'),
            discord_channel_id=self.env['ir.config_parameter'].sudo().get_param('discord.channel.id'),
        )
        return res