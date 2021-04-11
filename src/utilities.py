import discord
from discord.ext import commands


class SuggestUtilities:
    async def get_suggest_user(ctx, self, messageID):
        message = await ctx.fetch_message(messageID)
        messageContent = str(message.content)
        authorID = int(messageContent[:messageContent.find(" (")])
        author = ctx.guild.get_member(authorID)
        return author

    async def get_suggest_content(ctx, self, messageID):
        message = await ctx.fetch_message(messageID)
        messageContent = str(message.content)
        return messageContent[messageContent.find('```css\n'):]
