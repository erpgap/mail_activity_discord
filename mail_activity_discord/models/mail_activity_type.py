# -*- coding: utf-8 -*-
from odoo import models, fields
import requests
import json

class MailActivityType(models.Model):
    _inherit = 'mail.activity.type'

    discord_connector = fields.Boolean(string='Discord Connector', help='Does this activity type should be connected to Discord?')


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    def _cron_fetch_and_send_activities(self):
        """
        Fetch activities from Odoo and send messages to Discord.
        This method is triggered by a scheduled action (CRON).
        """
        domain = [
            ('activity_type_id.discord_connector', '=', True),
            ('date_deadline', '<=', fields.Date.context_today(self))
        ]

        # Retrieve the Discord bot token from the settings
        discord_token = self.env['ir.config_parameter'].sudo().get_param('discord.bot.token')

        if not discord_token:
            return

        # Fetch activities that need to be sent to Discord
        activities = self.search(domain).filtered(
            lambda a: hasattr(self.env[a.res_model], 'active') and self.env[a.res_model].browse(a.res_id).active or False)

        if activities:
            # Extract user IDs from the activities
            user_ids = [activity.user_id.id for activity in activities if activity.user_id]
            # Fetch Discord handlers for these user IDs
            discord_handlers = self._fetch_discord_handlers(user_ids)
            # Send Discord direct messages to users
            self._send_discord_messages(discord_token, activities, discord_handlers)

    def _fetch_discord_handlers(self, user_ids):
        """
        Fetch Discord handlers for given user IDs.
        """
        # Search for users with the specified user IDs
        users = self.env['res.users'].search([('id', 'in', user_ids)])
        # Create a dictionary mapping user IDs to their Discord handlers
        return {user.id: user.discord_handler for user in users}

    def _send_discord_messages(self, discord_token, activities, discord_handlers):
        """
        Send direct messages to users.
        """
        headers = {"Authorization": f"Bot {discord_token}", "Content-Type": "application/json"}

        for activity in activities:
            discord_handler = discord_handlers.get(activity.user_id.id) if activity.user_id else None
            # Format the message to be sent
            message = self._format_activity_message(activity, discord_handler)
            if discord_handler:
                message = f"{message}\n<@{discord_handler}>"

            # Send a direct message to the user if they have a discord_handler set
            if discord_handler:
                user_message = self._format_activity_message(activity, None)
                self._send_direct_message(discord_token, discord_handler, user_message)

    def _send_direct_message(self, discord_token, discord_handler, message):
        """
        Send a direct message to a Discord user.
        """
        headers = {"Authorization": f"Bot {discord_token}", "Content-Type": "application/json"}

        # Get the user's ID from the Discord API using their handler
        user_id = self._get_discord_user_id(discord_token, discord_handler)
        if not user_id:
            return

        # Create a DM channel with the user
        dm_url = "https://discord.com/api/v9/users/@me/channels"
        payload = {"recipient_id": user_id}
        response = requests.post(dm_url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            dm_channel_id = response.json().get("id")
            # Send the message to the DM channel
            self._post_message(f"https://discord.com/api/v9/channels/{dm_channel_id}/messages", headers, message)

    def _post_message(self, url, headers, message):
        """
        Post a message to the specified URL.
        """
        payload = {"content": message}
        requests.post(url, headers=headers, data=json.dumps(payload))

    def _get_discord_user_id(self, discord_token, discord_handler):
        """
        Get the Discord user ID from the handler.
        """
        headers = {"Authorization": f"Bot {discord_token}", "Content-Type": "application/json"}
        user_url = f"https://discord.com/api/v9/users/{discord_handler}"
        response = requests.get(user_url, headers=headers)

        if response.status_code == 200:
            return response.json().get("id")
        return None

    def _format_activity_message(self, activity, discord_handler):
        """
        Format the activity message to be sent to Discord.
        """
        user_name = activity.user_id.name if activity.user_id else 'Unassigned'

        lead = self.env['crm.lead'].browse(activity.res_id)
        lead_title = lead.name if lead else 'No Lead Title'

        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        lead_url = f"{base_url}/web#id={lead.id}&model=crm.lead"


        return (f"Lead: {lead_title}\n"
                f"Link: {lead_url}\n"
                f"Deadline: {activity.date_deadline}\n"
        )