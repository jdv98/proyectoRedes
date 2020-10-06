from telegram.ext import Updater, CommandHandler
import ijson
import json

def articles_count(update, context):
    ar=[]
    try:
        f  = ijson.parse(open('db3.json', 'r'))
        objects = ijson.items(f, 'dog_tags.item')
        ar = (o for o in objects if o['JM'] != None)
    
        count=0
        for x in ar:
            count+=1
        update.message.reply_text('Total count of IEEE Journals & Magazines Articles mapped \= *{}*'.format(count),parse_mode='MarkdownV2')
    except:
        update.message.reply_text('I am really sorry\! *Try again please*',parse_mode='MarkdownV2')

def out_of_scope(update, context):
    oos=[]
    try:
        with open('oos.json') as json_file:
            oos = json.load(json_file)["out_of_scope"]
        update.message.reply_text('Total out of scope Journals & Magazines \= *{}*'.format(len(oos)),parse_mode='MarkdownV2')
    except:
        update.message.reply_text('I am really sorry\! *Try again please*',parse_mode='MarkdownV2')

def last_time(update, context):
    last='0'
    try:
        with open('last9.json') as json_file:
            last = json.load(json_file)["last_time"]
        update.message.reply_text('Last time data was collected from the IEEE website \= *{}*'.format(last.replace('-','\-').replace('.','\.')),parse_mode='MarkdownV2')

    except: 
        update.message.reply_text('I am really sorry\! *Try again please*',parse_mode='MarkdownV2')

updater = Updater('1233391819:AAHXsQJBqH4VgJqp4TWmHthFvziTHuRfe78', use_context=True)

updater.dispatcher.add_handler(CommandHandler('ar', articles_count))
updater.dispatcher.add_handler(CommandHandler('oos', out_of_scope))
updater.dispatcher.add_handler(CommandHandler('last', last_time))

updater.start_polling()
updater.idle()
