import os
import telebot
from text import *
from VirusTotalAPI import VTApi

bot = telebot.TeleBot(os.environ.get('token'))

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(chat_id=message.chat.id, text=start_msg)

@bot.message_handler(content_types=['text'])
def text_handler(message):
    if message.entities:
        if message.entities[0].type != 'url':
            return bot.send_message(chat_id=message.chat.id, text='Incorrect url')
        scan = vt_api.url_report(vt_api.scan_url(message.text))
        get_report(chat_id=message.chat.id, scan=scan, scan_type='url_report', edit=False)

@bot.message_handler(content_types=['document'])
def files_handler(message):
    upload_msg = bot.send_message(chat_id=message.chat.id, text='Uploading file...')
    try:
        file_info = bot.get_file(message.document.file_id)
    except:
        bot.edit_message_text(chat_id=message.chat.id, message_id=upload_msg.message_id, text='Maximum file size to upload is 20 MB.')
        return ''
    downloaded_file = bot.download_file(file_info.file_path)
    scan = vt_api.file_report(vt_api.scan_file(downloaded_file))
    get_report(chat_id=message.chat.id, scan=scan, scan_type='file_report', message_id=upload_msg.message_id)

def get_report(chat_id, scan, scan_type, message_id=None, edit=True, upload_msg=None):
    markup = telebot.types.InlineKeyboardMarkup()
    info_button = telebot.types.InlineKeyboardButton(text='Details', url=scan['more'])
    markup.add(info_button)
    if scan['positives'] == 0:
        alert_message = '<b>No engines detected this {}.</b>'.format(scan_type.split('_')[0])
    else:
        alert_message = f'<b>{scan["positives"]} engines detected in this {scan_type.split("_")[0]}.</b>'
    if scan_type == 'file_report':
        total_message = '<code>{}</code>\n\n{}\nLast analysis: {}'.format(scan['results'], alert_message, scan['scan_date'])
    else:
        total_message = '<code>{}</code>\n\n{}\nURL: {}\nLast analysis: {}'.format(scan['results'], alert_message, scan['url'], scan['scan_date'])
    if message_id:
        bot.delete_message(chat_id=chat_id, message_id=message_id)
    bot.send_message(chat_id=chat_id, text=total_message, parse_mode='HTML', reply_markup=markup)

if __name__ == '__main__':
    vt_api = VTApi(os.environ.get('vt_token'))
    bot.polling(none_stop=True, interval=0)