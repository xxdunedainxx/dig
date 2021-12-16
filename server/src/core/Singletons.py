class Singletons:

  @staticmethod
  def generate_singletons():
    Singletons.setup_integrations()

  @staticmethod
  def setup_integrations():
    pass
    # Singletons.discordInt = DiscordIntegration.get_discord_integration()