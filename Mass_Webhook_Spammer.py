import discord
import random
import asyncio
from colorama import init, Fore

# Initialize colorama
init()

client = discord.Client()

spamming = False
webhooks = {}  # Dictionary to store channel IDs and webhook objects

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    global spamming  # Declare 'spamming' as global

    if message.content.lower() == '.ice':
        if spamming:
            await message.channel.send('Spamming is already in progress.')
        else:
            spamming = True
            guild = message.guild

            # Get all text channels in the guild
            text_channels = [channel for channel in guild.channels if isinstance(channel, discord.TextChannel)]

            if len(text_channels) < 20:
                # Create a webhook for each available channel
                for channel in text_channels:
                    webhook = await channel.create_webhook(name='.gg/eviction ran me')
                    webhooks[channel.id] = webhook  # Store the channel ID and webhook object in the dictionary
                    print(f"{Fore.MAGENTA}Webhook created in channel: {channel.name} ({channel.id})")
                    print(f"Webhook URL: {webhook.url}{Fore.RESET}")
            else:
                # Randomly select 20 text channels
                selected_channels = random.sample(text_channels, k=10)
                # Create a webhook in each selected channel
                for channel in selected_channels:
                    webhook = await channel.create_webhook(name='.gg/eviction ran me')
                    webhooks[channel.id] = webhook  # Store the channel ID and webhook object in the dictionary
                    print(f"{Fore.MAGENTA}Webhook created in channel: {channel.name} ({channel.id})")
                    print(f"Webhook URL: {webhook.url}{Fore.RESET}")

            # Continuously send the message using the webhooks until interrupted
            while spamming:
                for channel_id, webhook in webhooks.items():
                    await webhook.send('Myztery X syngate was here @everyone')
                    print(f"{Fore.GREEN}Message sent in channel: {guild.get_channel(channel_id).name} ({channel_id}){Fore.RESET}")
                    await asyncio.sleep(0.3)  # Delay between sending messages

            await message.channel.send('Spamming started in the specified channels.')

    elif message.content.lower() == '.stopspam':
        spamming = False
        await message.channel.send('Spamming stopped.')

@client.event
async def on_webhook_update(payload):
    global spamming  # Declare 'spamming' as global

    # Check if a webhook has been deleted
    if payload.action_type == discord.AuditLogAction.webhook_delete:
        webhook_id = payload.target_id
        for channel_id, webhook in webhooks.items():
            if webhook.id == webhook_id:
                del webhooks[channel_id]

                # Check if there are any webhooks left
                if not webhooks:
                    spamming = False

client.run("Enter Token here")
