import telebot
import os
from PIL import Image
from PIL.ExifTags import TAGS,GPSTAGS
from dotenv import load_dotenv

load_dotenv()

AUTH_TOKEN = os.getenv('AUTH_TOKEN')
bot = telebot.TeleBot(AUTH_TOKEN)

# This is bot code already done
def exif(path):
    var = ''
    image = Image.open(path)
    exifdata = image.getexif()
    for tagid in exifdata:
        tagname = TAGS.get(tagid,tagid)
        value = exifdata.get(tagid)
        if isinstance(value,bytes):
            value = value.decode()
        var += f"{tagname:30}:{value}\n"
    return var


def create_google_maps_url(gps_coords): 
    try:   
        dec_deg_lat = convertor(float(gps_coords["lat"][0]),  float(gps_coords["lat"][1]), float(gps_coords["lat"][2]), gps_coords["lat_ref"])
        dec_deg_lon = convertor(float(gps_coords["lon"][0]),  float(gps_coords["lon"][1]), float(gps_coords["lon"][2]), gps_coords["lon_ref"])
    except:
        return f"Geographical information can be retrieved Sorry for the inconvienience"
    # print(f"https://maps.google.com/?q={dec_deg_lat},{dec_deg_lon}")
    return f"https://maps.google.com/?q={dec_deg_lat},{dec_deg_lon}"


def GPSinformation(path):
    image = Image.open(path)
    gps_coords = {}
    # for tag,value in image._getexif().items():
    for tag,value in image._getexif().items():
        tagname = TAGS.get(tag)
        if tagname == "GPSInfo":
            for key,val in value.items():
                if GPSTAGS.get(key) == "GPSLatitude":
                            gps_coords["lat"] = val
                elif GPSTAGS.get(key) == "GPSLongitude":
                            gps_coords["lon"] = val
                elif GPSTAGS.get(key) == "GPSLatitudeRef":
                            gps_coords["lat_ref"] = val
                elif GPSTAGS.get(key) == "GPSLongitudeRef":
                            gps_coords["lon_ref"] = val
    return gps_coords
                


def convertor(degree,minutes,seconds,direction):
    decimal_degrees = degree + minutes / 60 + seconds / 3600
    if direction == "S" or direction == "W":
        decimal_degrees *= -1
    return decimal_degrees




# /start command reply code.
@bot.message_handler(commands=['start'])
def greet(message):
    bot.reply_to(message,'👋 Hello there, Just send the image as Document/File.\nThe bot will send the metadata!😃')
    


# Sent Image as Document

@bot.message_handler(content_types=['document'])
def document(message):
    # print('---------------SENT AS DOCUMENT---------------')
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    path = os.getcwd()+'\\Path\\'+file_name
    with open(path,'wb') as f:
        f.write(downloaded_file)
    try:
        data = exif(path)   #this is bots stuff
    except:
        data = ''
    try:
        gps_coords = GPSinformation(path)
    except:
        gps_coords = {}
    url = url = create_google_maps_url(gps_coords)
    # No meta data
    if data == '':
        bot.reply_to(message,'The meta date is already stripped. sorry ')
    else:
        bot.reply_to(message,f'The device info {data}\n{gps_coords}\nThe Google Maps link : {url}')
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
