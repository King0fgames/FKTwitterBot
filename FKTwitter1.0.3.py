#	FKTwitter Discord Bot
#	Author: King0fgames
#	Ver: 1.0.3
#	Last update: 9/10/22

from code import interact
import json
import interactions
import validators


# Get configuration.json
with open("configuration.json", "r") as config: 
	data = json.load(config)
	token = data["token"]
	prefix = data["prefix"]
	owner_id = data["owner_id"]


bot = interactions.Client(token)

# Nitter Slash Command
@bot.command(
    name="nitter",
    description="Retrieve the Nitter.it link from a Twitter link",
	options = [
        interactions.Option(
            name="twitter_link",
            description="link from twitter.com",
            type=interactions.OptionType.STRING,
            required=True,
		),
	],
)
async def nitter_replace(ctx: interactions.CommandContext, twitter_link: str):

	old_url = "https://twitter.com"
	new_url = "https://nitter.it"
	
	await replace_url(ctx, twitter_link, old_url, new_url, False)

# Nitter Context Menu Command
@bot.command(
    name="Get Nitter Link",
	type=interactions.ApplicationCommandType.MESSAGE,	
)
async def nitter_replace(ctx):

	link = ctx.target.content
	old_url = "https://twitter.com"
	new_url = "https://nitter.it"
	
	await replace_url(ctx, link, old_url, new_url, False)

# VXTwitter Slash Command
@bot.command(
    name="vxtwitter",
    description="Retrieve the VXTwitter link from a Twitter link",
	options = [
        interactions.Option(
            name="twitter_link",
            description="link from twitter.com",
            type=interactions.OptionType.STRING,
            required=True,
		),
	],
)
async def vxtwitter_replace(ctx: interactions.CommandContext, twitter_link: str):

	old_url = "https://twitter.com"
	new_url = "https://vxtwitter.com"
	
	await replace_url(ctx, twitter_link, old_url, new_url)


# VXTwitter Context Menu Command
@bot.command(
    name="Get VXTwitter Link",
	type=interactions.ApplicationCommandType.MESSAGE,	
)
async def vxtwitter_replace(ctx):

	link = ctx.target.content
	old_url = "https://twitter.com"
	new_url = "https://vxtwitter.com"
	
	await replace_url(ctx, link, old_url, new_url)
	
# Libreddit Slash Command
@bot.command(
    name="libreddit",
    description="Retrieve the Libreddit link from a Reddit link",
	options = [
        interactions.Option(
            name="reddit_link",
            description="link from reddit.com",
            type=interactions.OptionType.STRING,
            required=True,
		),
	],
)
async def libreddit_replace(ctx: interactions.CommandContext, reddit_link: str):

	old_url = "https://www.reddit.com"
	new_url = "https://libredd.it"
	
	await replace_url(ctx, reddit_link, old_url, new_url)


# Libreddit Context Menu Command
@bot.command(
    name="Get LibReddit Link",
	type=interactions.ApplicationCommandType.MESSAGE,	
)
async def reddit_replace(ctx):
	
	link = ctx.target.content
	old_url = "https://www.reddit.com"
	new_url = "https://libredd.it"
	
	await replace_url(ctx, link, old_url, new_url)


async def replace_url(ctx, link: str, old_url: str, new_url: str, embedded=True):
	if(old_url in link and (validators.url(link))):
		new_link = link.replace(old_url,new_url)
		new_link.strip()
		new_link = new_link.split("?")[0]

		if embedded:
			await ctx.send(f'{new_link}')
		else:
			await ctx.send(f'<{new_link}>')
	else:
		await ctx.send("Not a valid URL", ephemeral=True)

bot.start()
