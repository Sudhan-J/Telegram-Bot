import telebot
import os
from PIL import Image
from PIL.ExifTags import TAGS
from dotenv import load_dotenv

load_dotenv()

AUTH_TOKEN = os.getenv('AUTH_TOKEN')
bot = telebot.TeleBot(AUTH_TOKEN)


def exif(path):
    var = ''
    image = Image.open(path)
    exifdata = image.getexif()
    for tagid in exifdata:
        tagname = TAGS.get(tagid,tagid)
        value = exifdata.get(tagid)
        var += f"{tagname:20}:{value}\n"
    return var


# /start command reply code.
@bot.message_handler(commands=['start'])
def greet(message):
    bot.reply_to(message,'👋 Hello there, Just send the image as Document/File.\nThe bot will send the metadata!😃')
    


# Sent Image as Document

@bot.message_handler(content_types=['document'])
def document(message):
    print('---------------SENT AS DOCUMENT---------------')
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    path = os.getcwd()+'\\path\\'+file_name
    with open(path,'wb') as f:
        f.write(downloaded_file)
    data = exif(path)
    if data == '':
        bot.reply_to(message,'The meta date is already stripped. sorry ')
    else:
        bot.reply_to(message,data+'\n\nThank You for using our service!!!')
    try:
        os.remove(path)
    except:
        print('---------------FILE IS NOT DELETED---------------')
    print('Extracted and Sent!')
    


# Sent as Image 

@bot.message_handler(content_types=['photo'])
def photo(message):
    bot.reply_to(message,"Please send the Image in Document/file format as Telegram by default removes the meta data(Exif data) off of the image while sending it.\n Send the image as document/file.\nClick on the below link to see demo video.😃\nhttps://youtube.com/shorts/5ynhOeIQOeA?feature=share")


@bot.message_handler(content_types=['video','audio'])
def video(message):
    bot.reply_to(message,'Sorry, Videos and audios are not supported yet!!')

# main funtion 
def main():
    bot.infinity_polling()

# actually calling the main function
if __name__ == "__main__":
    main()





