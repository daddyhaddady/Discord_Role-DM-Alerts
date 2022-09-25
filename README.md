# DM Role Alerts
A Discord bot that allows you to customize embed messages to be DM'd to members when roles you have configured have been assigned.



 ### Discord Bot Token and Server Invitation

1. Login to Discord web - https://discord.com
2. Navigate to Discord Developer Portal - https://discord.com/developers/applications
3. Click *New Application*
4. Give the Appplication a name and *Create*
5. Add image for Discord icon
6. Go to Bot tab and click *Add Bot*
7. Enable **SERVER MEMBERS INTENT**
8. Add a bot image
9. Copy the token and paste it into `.sample_env` file, then rename that file to `.env`
10. Navigate to OAuth2 Tab > URL Generator
11. Check **bot** and **applications.commands**
12. In the **BOT PERMISSIONS** section, check the following:
    - Manage Roles
    - Send Messages

13. Copy the GENERATED URL link and paste it into your browser or in a discord message. Click the link to invite the bot



### Getting Started

#### Prequisites

1. Install Python 3.10+
2. install dependencies - `pip install -r requirements.txt` or `poetry install`


### Configuring the bot

1. If you haven't already, paste your token from earlier into the `.sample_env` file, then save and rename that file to `.env`
2. Run the bot


Now that the bot is running you may view, add, edit, or remove any roles and their messages that you have configured.  Once messages have been configured for the roles, when those role are assigned, the member that received the role will receive your customized embed as a DM.
___
*Warning: Members can prevent incoming messages from non-friends, even if in the same guild (this includes bots) If this is enabled, that member will not receive a DM*
___
### Commands
All commands in this bot are slash commands and are available with `/`  
`[` `]` represents <u>**optional**</u> parameters  
`(` `)` represents <u>**required**</u> parameters

Command | Description 
--- | --- 
`/config view [role_name]` | Displays all currently configured roles with their customized embed message. Include the optional `role_name` parameter to view a specific role's configured message
`/config add (role)` | Add a new customized message for the specified role
`config remove (role_name)` | Remove the specified role's current configuration
`/config edit (role_name)` | Edit the customized message for the specified role