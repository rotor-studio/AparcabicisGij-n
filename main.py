from fastkml import kml
import geopy.distance
import telebot
from telebot import types
from telebot.apihelper import edit_message_reply_markup
from telebot.types import ReplyKeyboardRemove

bot = telebot.TeleBot('5752723251:AAGHVBXfDfBC8gsicjUQCZclZE-CB-M1s7M')

kml_filename = "828.kml"

user_coords = [-5.6769896788084, 43.52953996222519]
user_dist = 200

find = False
no = False
si = False

@bot.message_handler(content_types=['text'])
def send_location(message):

  global find
  global no
  global si
  global user_coords

  if message.text.isdigit() and find == True:
    a = message.text
    b= "Buscando alternativas a una distancia de "+a+" metros..."
    bot.send_message(message.chat.id, b)
    user_dist = int(a)


    with open(kml_filename) as kml_file:
        doc = kml_file.read().encode('utf-8')
        k = kml.KML()
        k.from_string(doc)

        outerFeature = list(k.features())
        innerFeature = list(outerFeature[0].features())
        placemarks = list(innerFeature[0].features())

        d = 0
        for p in placemarks:
            # print(p.geometry)
            coords = (p.geometry.x, p.geometry.y)
            dist = geopy.distance.geodesic(user_coords, coords).m
            print(geopy.distance.geodesic(user_coords, coords).m)

            if dist < user_dist:
                d = d + 1
                b = "Este es la alternativa de anclaje más cercana nº " + str(d)
                print(coords)
                bot.send_message(message.chat.id,b)
                bot.send_location(message.from_user.id, longitude=coords[0], latitude=coords[1])
                si = True
                no = False

            elif si == False:
                no = True

    if no == True:
     bot.send_message(message.chat.id, "Lo siento, no hay anclajes a esa distancia, prueba de nuevo!")
    if no == False:
     bot.send_message(message.chat.id, "Espero que alguno te sirva ;) ",reply_markup=telebot.types.ReplyKeyboardRemove())

    find = False

  if message.text == "/help":
      keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      button_geo = types.KeyboardButton(text="Dime tu ubicación", request_location=True)
      keyboard.add(button_geo)
      bot.send_message(message.chat.id,
                       "Si me dices donde estás, te ayudaré a buscar un anclaje ;)",reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def handle_location(message):

    global find
    global no
    global si
    global user_coords

    location = [message.location.longitude,message.location.latitude]
    print(location)
    user_coords = location
    print("Estas son las coordenadas: ",user_coords)

    bot.send_message(message.chat.id, "Ahora por favor, dime la máxima distancia a la que quieres buscar...")
    find = True
    no = False
    si = False

bot.polling()