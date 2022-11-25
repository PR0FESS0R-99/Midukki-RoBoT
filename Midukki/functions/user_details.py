def user_mention(bot):
  mention = bot.from_user.mention if bot.from_user else None
  return mention 
