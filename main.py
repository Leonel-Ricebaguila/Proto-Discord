"""Main entry point for the Discord music bot."""
import os
from bot import create_bot
from utils.config import DISCORD_TOKEN


def main():
    """Main function to run the bot."""
    try:
        # Start HTTP server if PORT is set (for Render web service)
        if os.environ.get('PORT'):
            import server
            port = int(os.environ.get('PORT', 10000))
            server.start_server(port)
            print(f"✓ Health check server started on port {port}")
        
        # Start Discord bot
        bot = create_bot()
        bot.run(DISCORD_TOKEN)
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease ensure you have:")
        print("1. Created a .env file in the project root")
        print("2. Added your Discord bot token: DISCORD_TOKEN=your_token_here")
        print("\nFor help setting up your bot, see the README.md file.\n")
    except Exception as e:
        print(f"\n❌ Error starting bot: {e}\n")


if __name__ == "__main__":
    main()

