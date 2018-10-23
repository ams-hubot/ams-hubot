# coding: utf-8

from slackbot.bot import Bot
from botty_mcbotface import log


def main():
    """Start slackbot"""
    
    bot = Bot()
    bot.run()


if __name__ == "__main__":
	print('start slackbot')
	main()