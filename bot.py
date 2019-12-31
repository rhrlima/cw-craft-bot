import os
import logging

from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.ext import MessageHandler, Filters

import cw_craft as util


def parse_message(update, context):
    text = update.message.text

    is_valid = util.parse_text_from_guild(text)
    print('Guild warehouse: ', is_valid)

    is_valid = util.parse_text_from_craft(text)
    print('Craft', is_valid)


def unknown_command(update, context):

    from_ = update.effective_user
    text = update.message.text
    logging.warning(f'User: {from_.username} sent an unknown command: {text}')

    text = "Sorry, I didn't understand that command.\n"
    text +="Please, use /help to see available commands."

    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def start_command(update, context):

    logging.info('Starting the bot')

    text = """Hi! I am a bot.
    check /help to see what I can do.

    /collectors_riot"""

    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def list_help(update, context):

    text = 'Available commands:\n'
    text +='/craft to see possible crafts\n'
    text +='/craft_full to see full list\n'
    text +='/craft_reset to reset the craft buffer'

    update.message.reply_text(text)


def list_crafts(update, context):

    lines = util.list_possible_crafts(False)

    for i, line in enumerate(lines):
        lines[i] = f'`{line[0]:<3} {line[1]:>2}|{line[2]:>2} {line[3]:2} `{line[4]}'

    update.message.reply_text('List of Recipes/Parts:')
    if len(lines) > 0:
        update.message.reply_text('\n'.join(lines), parse_mode='Markdown')
    else:
        update.message.reply_text('No available crafts\nUse /craft_full to see full list.')


def list_crafts_full(update, context):

    lines = util.list_possible_crafts(True)

    for i, line in enumerate(lines):
        lines[i] = f'`{line[0]:<3} {line[1]:>2}|{line[2]:>2} {line[3]:2} `{line[4]}'

    update.message.reply_text('List of Recipes/Parts:')
    update.message.reply_text('\n'.join(lines), parse_mode='Markdown')
    

def list_craft_reset(update, context):

    util._reset_items('items.json')
    update.message.reply_text('Craft buffer reseted.')


def main():

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    token = os.environ['cw_craft_bot_token']
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, parse_message))

    dp.add_handler(CommandHandler('start', start_command))

    dp.add_handler(CommandHandler('help', list_help))
    dp.add_handler(CommandHandler('craft', list_crafts))
    dp.add_handler(CommandHandler('craft_full', list_crafts_full))
    dp.add_handler(CommandHandler('craft_reset', list_craft_reset))

    dp.add_handler(MessageHandler(Filters.command, unknown_command))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()