#	FKTwitter Discord Bot
#	Author: King0fgames
#	Ver: 1.3.0
#	Last update: 4/4/23
#	Source: https://github.com/King0fgames/FKTwitterBot

import json
import interactions
import validators
from urllib.parse import urlparse, urlunparse

# enables url parse debugging
debug = False

# Get configuration.json
with open("configuration.json", "r") as config: 
	data = json.load(config)
	token = data["token"]
	prefix = data["prefix"]
	owner_id = data["owner_id"]


bot = interactions.Client(token)

class Site:
    def __init__(self, inputs, output, embed=True, del_query=True):      
        self.inputs = inputs
        self.output = output
        self.embed = embed
        self.del_query = del_query

#Site objects (inputs, output, embed, del_query)
nitter = Site(
    ("twitter.com", "mobile.twitter.com", "vxtwitter.com"),
    "nitter.net",
	embed = False
)
vxtwitter = Site(
    ("twitter.com", "mobile.twitter.com", "nitter.net"),
    "vxtwitter.com"
)
libreddit = Site(
    ("www.reddit.com","old.reddit.com", "reddit.com"),
    "r.nf"
)
invidious = Site(
    ("www.youtube.com", "youtube.com", "youtu.be"),
    "yewtu.be",
	del_query = False
)
proxitok = Site(
    ("www.tiktok.com", "tiktok.com"),
    "proxitok.pabloferreiro.es"
)

# Nitter Slash Command
@bot.command(
    name="nitter",
    description="Convert to Nitter, alternative Twitter front-end",
	options = [
        interactions.Option(
            name="twitter_link",
            description="twitter.com",
            type=interactions.OptionType.STRING,
            required=True,
		),
	],
)
async def nitter_replace(ctx: interactions.CommandContext, twitter_link: str):

	await replace_url(ctx, twitter_link, nitter)

# Nitter Context Menu Command
@bot.command(
    name="Twitter -> Nitter",
	type=interactions.ApplicationCommandType.MESSAGE,	
)
async def nitter_replace(ctx):
	link = ctx.target.content
	await replace_url(ctx, link, nitter)
	


# VXTwitter Slash Command
@bot.command(
    name="vxtwitter",
    description="Convert to VXTwitter, to fix embedding",
	options = [
        interactions.Option(
            name="twitter_link",
            description="twitter.com",
            type=interactions.OptionType.STRING,
            required=True,
		),
	],
)
async def vxtwitter_replace(ctx: interactions.CommandContext, twitter_link: str):
	await replace_url(ctx, twitter_link, vxtwitter)

# VXTwitter Context Menu Command
@bot.command(
    name="Twitter -> VXTwitter",
	type=interactions.ApplicationCommandType.MESSAGE,	
)
async def vxtwitter_replace(ctx):
	link = ctx.target.content
	await replace_url(ctx, link, vxtwitter)
	

# Libreddit Slash Command
@bot.command(
    name="libreddit",
    description="Convert to Libreddit, alternative Reddit front-end",
	options = [
        interactions.Option(
            name="reddit_link",
            description="reddit.com",
            type=interactions.OptionType.STRING,
            required=True,
		),
	],
)
async def libreddit_replace(ctx: interactions.CommandContext, reddit_link: str):
	await replace_url(ctx, reddit_link, libreddit)

# Libreddit Context Menu Command
@bot.command(
    name="Reddit -> LibReddit",
	type=interactions.ApplicationCommandType.MESSAGE,	
)
async def libreddit_replace(ctx):
	link = ctx.target.content
	await replace_url(ctx, link, libreddit)

# Invidious Slash Command
@bot.command(
    name="invidious",
    description="Convert to Invidious, alternative Youtube front-end",
	options = [
        interactions.Option(
            name="youtube_link",
            description="youtube.com or youtu.be link",
            type=interactions.OptionType.STRING,
            required=True,
		),
	],
)
async def invidious_replace(ctx: interactions.CommandContext, youtube_link: str):
	await replace_url(ctx, youtube_link, invidious)

# Invidious Context Menu Command
@bot.command(
    name="Youtube -> Invidious",
	type=interactions.ApplicationCommandType.MESSAGE,	
)
async def invidious_replace(ctx):
	link = ctx.target.content	
	await replace_url(ctx, link, invidious)


# ProxiTok Slash Command
@bot.command(
    name="proxitok",
    description="Convert to ProxiTok, alternative TikTok front-end",
	options = [
        interactions.Option(
            name="tiktok_link",
            description="tiktok.com link",
            type=interactions.OptionType.STRING,
            required=True,
		),
	],
)
async def proxitok_replace(ctx: interactions.CommandContext, tiktok_link: str):
	await replace_url(ctx, tiktok_link, proxitok)

# ProxiTok Context Menu Command
@bot.command(
    name="TikTok -> ProxiTok",
	type=interactions.ApplicationCommandType.MESSAGE,	
)
async def proxitok_replace(ctx):
	link = ctx.target.content	
	await replace_url(ctx, link, proxitok)

# Validate, replace, and send new url
async def replace_url(ctx, link: str, site: Site):
	
	#url validation
	url = urlparse(link)

	#url parse debugging, apparently python's urllib doesn't support .it extensions
	if(debug):
		print("Validating:\nscheme: " + url.scheme + "\nnetloc: " + url.netloc + "\npath: " 
				+ url.path + "\nquery:" + url.query + "\nfragment:" + url.fragment)
	
	if(url.netloc in site.inputs and (validators.url(link))):

		#replace query string, usually tracking garbage
		if(site.del_query): #default = True
			url = url._replace(query = '')

		#replace domain with target site
		url = url._replace(netloc = site.output)
		new_link = urlunparse(url)

		#send new link
		if site.embed: #default = True
			await ctx.send(f'{new_link}')
		else:
			await ctx.send(f'<{new_link}>')
	#Failure message		
	else:
		await ctx.send(f"Invalid URL, accepted URLS: ".join(site.inputs), ephemeral=True)

print("FKTwitter Bot starting")
bot.start()
print("FKTwitter Bot shutting down")
