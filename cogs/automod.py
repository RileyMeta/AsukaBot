import os
import discord
import threading
from discord.ext import commands

# File monitoring
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

LOGS = int(os.getenv("LOGS"))

class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.banned_words_file = os.path.join(os.getcwd(), 'banned_words.txt')
        self.banned_words = self.load_banned_words()
        self.start_file_watcher()

    def load_banned_words(self):
        try:
            with open(self.banned_words_file, 'r') as file:
                return [line.strip().lower() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"[Automod] {self.banned_words_file} not found.")
            return []

    def reload_banned_words(self):
        print("[Automod] Reloading banned words...")
        self.banned_words = self.load_banned_words()

    def start_file_watcher(self):
        class BannedWordsFileHandler(FileSystemEventHandler):
            def __init__(self, filepath, callback):
                self.filepath = os.path.abspath(filepath)
                self.callback = callback

            def on_modified(self, event):
                if os.path.abspath(event.src_path) == self.filepath:
                    self.callback()

        handler = BannedWordsFileHandler(self.banned_words_file, self.reload_banned_words)
        observer = Observer()
        observer.schedule(handler, path=os.path.dirname(self.banned_words_file) or '.', recursive=False)
        thread = threading.Thread(target=observer.start, daemon=True)
        thread.start()
        print("[AutoMod] Started watching banned_words.txt for changes.")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore bots and DMs
        if message.author.bot or not message.guild:
            return

        content_lower = message.content.lower()

        for word in self.banned_words:
            if word in content_lower:
                try:
                    await message.delete()

                    # Notify user of banned word
                    await message.channel.send(
                            f"{message.author.mention} your message was removed for containing a banned word.",
                            delete_after=5
                        )

                    # Get moderation cog
                    mod_cog = self.bot.get_cog("Moderation")
                    if mod_cog:
                        member = message.guild.get_member(message.author.id)

                        if member:
                            await mod_cog.mute_member(
                                ctx=None,
                                member=member,
                                reason=f"Used banned word: '{word}'",
                                original_message=message
                            )

                        # if member:
                        #     await mod_cog.mute_member(
                        #         ctx=None,
                        #         message.author,
                        #         reason="Used a banned word",
                        #         original_message=message
                        #     )
                        else:
                            printf("[Automod] Failed to get member from guild.")
                    else:
                        print("[Automod] Moderation cog not found.")

                except discord.Forbidden:
                    print("[Automod] Missing permissions to delete message.")
                break
def setup(bot):
    bot.add_cog(Automod(bot))
