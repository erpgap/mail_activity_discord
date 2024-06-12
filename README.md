# Odoo Discord Bot Module

## Overview

This Odoo module allows you to send Odoo activities to a Discord channel and direct messages to users. It is designed to work with both Odoo Community Edition (CE) and Odoo Enterprise Edition.

## Features

- Send Odoo activities to a specified Discord channel.
- Send direct messages to users with a Discord handler.
- Configurable settings for Discord bot token and channel ID.
- Scheduled task (CRON) to automate sending messages at specified intervals.

## Configuration

### Discord Bot Settings

1. Navigate to the **Settings** menu in Odoo.
2. In the **General Settings** section, locate the **Discord Bot Settings** section.
3. Enter your Discord Bot Token in the **Discord Bot Token** field.
4. Enter the Discord Channel ID in the **Discord Channel ID** field.
5. Save the settings.

### User Configuration

1. Ensure users have their Discord handler set up in their user profile.
2. Navigate to **Settings** -> **Users & Companies** -> **Users**.
3. Open a user profile and set the **Discord Handler** field with the user's Discord ID.

### Activity Type Configuration

1. Navigate to **Settings** -> **Technical** -> **Email** -> **Activity Types**.
2. Open an activity type that you want to be sent to Discord.
3. Enable the **Discord Connector** checkbox.
4. Save the activity type.

### Scheduled Task (CRON)

1. The module includes a CRON job to automate sending messages.
2. By default, the CRON job runs every hour.
3. You can adjust the timing by going to **Settings** -> **Technical** -> **Automation** -> **Scheduled Actions**.
4. Locate the **Send Discord Messages** action and adjust the **Interval Number** and **Interval Unit** as needed.

## Usage

Once configured, the module will automatically fetch activities from Odoo and send messages to the specified Discord channel and direct messages to users based on the following conditions:

- Activities with a deadline on or before today.
- Activities with a custom flag indicating they should be sent to Discord.

## Notes

- Ensure your Discord bot has the necessary permissions to send messages to the specified channel and to create DM channels with users.
- This module assumes that users' Discord handlers are stored in the `discord_handler` field in their user profile.

![alt text](/mail_activity_discord/data/promptequation_logo.png)
![alt text](/mail_activity_discord/data/erpgap_logo.png)
