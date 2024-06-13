# models/discord_bot.py

import requests
import json
from datetime import datetime
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class DiscordBot(models.AbstractModel):
    _name = 'discord.bot'
    _description = 'Discord Bot'

    @api.model
    def fetch_and_send_activities(self):
        """Fetch activities from Odoo and send messages to Discord."""
        _logger.info("Starting to fetch and send activities")
        
        # Retrieve the Discord bot token and channel ID from the settings
        discord_token = self.env['ir.config_parameter'].sudo().get_param('discord.bot.token')
        channel_id = self.env['ir.config_parameter'].sudo().get_param('discord.channel.id')

        # Check if the required parameters are set
        if not discord_token or not channel_id:
            _logger.warning("Discord token or channel ID not set.")
            return  # Exit if the required parameters are not set

        # Fetch activities that need to be sent to Discord
        activities = self.fetch_activities()
        if activities:
            # Extract user IDs from the activities
            user_ids = [activity.user_id.id for activity in activities if activity.user_id]
            # Fetch Discord handlers for these user IDs
            discord_handlers = self.fetch_discord_handlers(user_ids)
            _logger.info("Fetched activities and user handlers")
            
            # Send messages to the Discord channel and direct messages to users
            self.send_discord_messages(discord_token, channel_id, activities, discord_handlers)
        else:
            _logger.info("No activities found to send")

    def fetch_activities(self):
        """Fetch activities from Odoo that need to be sent to Discord."""
        today = datetime.today().date()
        _logger.info("Fetching activities with deadline <= %s", today)
        
        # Search for activities with the custom flag and a deadline up to today
        activities = self.env['mail.activity'].search([
            ('activity_type_id.discord_connector', '=', True),
            ('date_deadline', '<=', today)
        ])
        
        _logger.info("Fetched %d activities", len(activities))
        return activities

    def fetch_discord_handlers(self, user_ids):
        """Fetch Discord handlers for given user IDs."""
        _logger.info("Fetching Discord handlers for user IDs: %s", user_ids)
        
        # Search for users with the specified user IDs
        users = self.env['res.users'].search([('id', 'in', user_ids)])
        # Create a dictionary mapping user IDs to their Discord handlers
        discord_handlers = {user.id: user.discord_handler for user in users}
        
        _logger.info("Fetched Discord handlers: %s", discord_handlers)
        return discord_handlers

    def send_discord_messages(self, discord_token, channel_id, activities, discord_handlers):
        """Send messages to the Discord channel and direct messages to users."""
        _logger.info("Sending messages to Discord channel %s", channel_id)
        
        headers = {
            "Authorization": f"Bot {discord_token}",
            "Content-Type": "application/json"
        }
        base_url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
        
        for activity in activities:
            discord_handler = discord_handlers.get(activity.user_id.id) if activity.user_id else None
            # Format the message to be sent
            message = self.format_activity_message(activity, discord_handler)
            if discord_handler:
                message = f"{message}\n<@{discord_handler}>"
                
            # Send the message to the specified Discord channel
            payload = {"content": message}
            response = requests.post(base_url, headers=headers, data=json.dumps(payload))
            
            if response.status_code != 200:
                _logger.error("Failed to send message to Discord channel: %s", response.text)
            else:
                _logger.info("Successfully sent message to Discord channel: %s", message)
            
            # Send a direct message to the user if they have a discord_handler set
            if discord_handler:
                user_message = self.format_activity_message(activity, None)
                self.send_direct_message(discord_token, discord_handler, user_message)
    
    def send_direct_message(self, discord_token, discord_handler, message):
        """Send a direct message to a Discord user."""
        _logger.info("Sending direct message to Discord user %s", discord_handler)
        
        headers = {
            "Authorization": f"Bot {discord_token}",
            "Content-Type": "application/json"
        }
        
        # Get the user's ID from the Discord API using their handler
        user_id = self.get_discord_user_id(discord_token, discord_handler)
        if not user_id:
            _logger.error("Failed to get Discord user ID for handler: %s", discord_handler)
            return
        
        # Create a DM channel with the user
        dm_url = "https://discord.com/api/v9/users/@me/channels"
        payload = {"recipient_id": user_id}
        response = requests.post(dm_url, headers=headers, data=json.dumps(payload))
        
        if response.status_code != 200:
            _logger.error("Failed to create DM channel: %s", response.text)
            return
        
        dm_channel_id = response.json().get("id")
        
        # Send the message to the DM channel
        dm_message_url = f"https://discord.com/api/v9/channels/{dm_channel_id}/messages"
        payload = {"content": message}
        response = requests.post(dm_message_url, headers=headers, data=json.dumps(payload))
        
        if response.status_code != 200:
            _logger.error("Failed to send DM message: %s", response.text)
        else:
            _logger.info("Successfully sent DM message: %s", message)
    
    def get_discord_user_id(self, discord_token, discord_handler):
        """Get the Discord user ID from the handler."""
        headers = {
            "Authorization": f"Bot {discord_token}",
            "Content-Type": "application/json"
        }
        user_url = f"https://discord.com/api/v9/users/{discord_handler}"
        response = requests.get(user_url, headers=headers)
        
        if response.status_code == 200:
            return response.json().get("id")
        else:
            _logger.error("Failed to get user ID for handler %s: %s", discord_handler, response.text)
            return None

    def format_activity_message(self, activity, discord_handler):
        """Format the activity message to be sent to Discord."""
        user_name = activity.user_id.name if activity.user_id else 'Unassigned'
        discord_user = discord_handler if discord_handler else 'Unassigned'
        
        return (f"Activity: {activity.res_name}\n"
                f"Type: {activity.activity_type_id.name}\n"
                f"Deadline: {activity.date_deadline}\n"
                f"Assigned to: {user_name}")
                #f"Discord User: {discord_user}")