# Copyright (c) 2022 AnandhKumar E S
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import email
from discord.ext import commands, bridge
from discord.ext.pages import Page, Paginator
import discord
import typing
from bot.bot import Bot


class Hundred(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.group(name="100", description="100 days of code challenge.")
    async def _100(self, ctx: commands.Context):
        pages = []

        page1 = discord.Embed(
            title="100 Days of Code",
            description="Code minimum an hour every day for the next 100 days. And commit your progress using me.",
            url="https://www.100daysofcode.com/",
        )
        page1.set_image(
            url="https://cdn.discordapp.com/avatars/989080128007045181/511983802f802a5122eff41554de1612.png?size=256"
        )
        page2 = discord.Embed(
            title="Rules",
            description="""
        
        ● Code for minimum an hour a day.
        
        ● Commit your progress daily with this bot.
        
        ● Linking github, will enable a feature that will check your github for progress and only allows to commit, if there is some progress in github. (Optional)
        
        ● Tweet your progress daily with the hastag: `#100DaysOfCode`. (Optional)
        
        ● Each day, reach out to at least people on Twitter who are also doing the challenge. (Optional)
        """,
        )
        page3 = discord.Embed(
            title="Benefits",
            description="""
        ● Coding will become a daily habit for you — a habit that you can easily maintain after you've finished the challenge.
        
        ● Every day that you consistently code, you'll build momentum. That momentum will make it easier for you to learn more advanced topics. You won't have to spend extra time trying to remember what you did previously. You can stay in the “flow” of coding.
        
        ● You'll make friends and meet like-minded people who are also working through this challenge alongside you. They'll help you find the strength to keep coding even on the days when you don't feel like you're making progress. They can also help you when you inevitably get stuck.
        
        ● The projects that you'll build will be small in scope, so by the time you finish, you'll have completed several of them — and gained a wide range of experience.
        """,
        )
        page4 = discord.Embed(
            description="""
        
        ● If you were just working through tutorials, you wouldn't have much to show for it. But with #100DaysOfCode, you'll build real portfolio projects that you can show to potential employers and share with your family.
        
        ● These projects will give you practice with concepts that frequently come up during developer job interviews.
        
        ● Your GitHub profile will look extremely active. And yes, hiring managers and recruiters do look at these.
        
        ● You'll greatly diminish your fear of starting a new coding project. It will become a natural, ordinary thing to do.
        
        ● You'll have a good reason to stop procrastinating and start coding every day.
        """
        )
        page5 = discord.Embed(
            title="Links",
            description="""
        
        ● [ Website ](https://www.100daysofcode.com/ \"Visit site\") - Visit offcial site and get more info about this challenge.
        
        ● [ Discord ](https://discord.gg/x7TGGTG \"Join Server\") - Join official discord server of `#100DaysOfCode`.
        
        ● [ Alex Kallaway ](https://twitter.com/ka11away \"See his profile\") - Creator of `#100DaysOfCode`.
        
        ● [100DaysOfCode ](https://twitter.com/_100DaysOfCode \"Twitter Bot\") - Twitter Bot that retweets the tweets that contain the `#100DaysOfCode`.
        
        ● [ Github Repo ](https://github.com/Kallaway/100-days-of-code \"Visit Repo\") - Github repository of `#100DaysOfCode`. 
        """,
        )

        pages.append(Page(embeds=[page1]))
        pages.append(Page(embeds=[page2]))
        pages.append(Page(embeds=[page3]))
        pages.append(Page(embeds=[page4]))
        pages.append(Page(embeds=[page5]))
        paginator = Paginator(pages=pages, timeout=100)
        await paginator.send(ctx)


def setup(bot: Bot):
    bot.add_cog(Hundred(bot))
