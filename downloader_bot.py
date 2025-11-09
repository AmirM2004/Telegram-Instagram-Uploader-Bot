import asyncio  , os  , random  , json , time , requests 
from pyrogram import Client, filters, types , errors

# ⚠️⚠️ warning : this bot just send videos to wtarget channel wich links that minned in local_searcher.py

# ___________________________________ basic data ___________________________________

bot = Client("bot", api_id='22901108', api_hash= '0e94c7511deb3550372f2dc18a562770', bot_token="7210735611:AAFc8uFasnL_3QhdwUIPjB1QyIO7kmUx7jk")

max_vedio_size = 20 # MB

min_waiting_time_singl_media =  7
max_waiting_time_singl_media = 10

min_waiting_time_multi_media = 10
max_waiting_time_multi_media = 15

send_multi_media = True # at the end of sending each multi_media in a single message if this variable == True ، we will send a group media message !

way1_instagram = -1002222623271 # way1_instagram channel id (way 1 insta)
way1_telegram = -1001960933682 
way2 = -1001886335240

minig_links = 0 # it means we are sending videos  and photos at this moment
total_errors = 0  # if we got problem to send a media
total_success = 0 # if evry thing is okey to send a media
all_requests = 0
size_warrning = 0

ID_robot = 7210735611
ID_bot_admins = [5507957134]

# _____________________________ main updators _____________________________

@bot.on_message(filters.command("start"))
async def start_func(client, message):

    global minig_links , total_errors , total_success , ID_bot_admins

    ID = message.from_user.id

    if ID in ID_bot_admins :
        await message.reply_text("Hello , send me the file to start the good jobs ... 🤭")
    else :
        await message.reply_text("❌ you dont have access , only admins can to any shit !")

@bot.on_message(filters.command("status"))
async def status_func(client, message):

    global minig_links , total_errors , total_success , ID_bot_admins , all_requests

    ID = message.from_user.id

    if ID in ID_bot_admins :

        if minig_links == 1 :
            await message.reply_text(f"total tries : {total_errors + total_success}\n\ntotal success : {total_success}\n\ntotal errors : {total_errors}\n\nremainig : {all_requests}")
        else :
            await message.reply_text("There is no Activity")

    else :
        await message.reply_text("❌ you dont have access , only admins can to any shit !")

@bot.on_message(filters.command("error"))
async def error_func(client, message):

    ID = message.from_user.id

    if ID in ID_bot_admins :

        try: 
            await bot.send_document(ID , "nohup.out" , caption="Errors")
        except:
            await message.reply_text("There is no error")

        try :
            os.remove("nohup.out" )
        except :
            pass

    else :
        await message.reply_text("❌ you dont have access , only admins can to any shit !")

@bot.on_message(filters.document & filters.private)
async def messager(client, message): 

    global minig_links , total_errors , total_success , all_requests , ID_bot_admins , ID_robot , send_multi_media , size_warrning

    ID = message.from_user.id

    if (message.document.file_name.endswith("json")) and ((ID in ID_bot_admins) or (ID == ID_robot)) :

        if minig_links == 0 :

            minig_links = 1

            await message.reply_text("✅ Start The Job ...")

            json_file_path = await message.download()
            
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)    
            
            os.remove(json_file_path)

            for i in data.keys() :

                if len(data[i]["links"]) == 1 :
                    all_requests += 1
                else :
                    if send_multi_media :
                        all_requests += len(data[i]["links"]) * 2
                    else :
                        all_requests += len(data[i]["links"])

            time_start_download = time.time()

            await download_liks(data)

            await message.reply_text(f'''
Done ! ✅

total time: {int(time.time() - time_start_download)} Second

successfully download : {total_success}
                                     
failed download : {total_errors}
                                     
total requests : {all_requests}

oversize videos : {size_warrning}
''')
            
            minig_links = 0
            total_errors = 0
            total_success = 0
            all_requests = 0
            size_warrning = 0

        else :

            await message.reply_text("still doing the last job plz wait ...")

    elif (ID not in ID_bot_admins) :
        await message.reply_text("❌ you dont have access , only admins can to any shit !")

    elif not message.document.file_name.endswith("json") :
        await message.reply_text("❌ your file should be a json ...")


# _____________________________ function to send the links in way1_instagram channel  _____________________________

async def download_liks(data) :

    count_rest = 0

    global min_waiting_time_singl_media , max_waiting_time_singl_media , min_waiting_time_multi_media , max_waiting_time_multi_media , way1_instagram , total_errors , total_success , send_multi_media , all_requests , size_warrning , max_vedio_size

    for i in data.keys() :

        count_rest += 1

        if count_rest == 15 : # for download (send file in telegram) in 15 count we need to a littel rest
            await asyncio.sleep(10)
            count_rest = 0

        caption = data[i]["caption"]
        media_files = []
        first = 0

        for j in data[i]["links"] :

            if j[1] == "photo":

                await asyncio.sleep(random.randint(min_waiting_time_singl_media , max_waiting_time_singl_media))

                try :

                    await bot.send_photo(way1_instagram, photo= j[0], caption= caption)
                    total_success += 1

                except errors.FloodWait as e:

                    await asyncio.sleep(e.value)

                    try :

                        await bot.send_photo(way1_instagram, photo= j[0], caption= caption)
                        total_success += 1

                    except :
                        total_errors +=  1

                except :

                    total_errors +=  1

                if first == 0 :
                    media_files += [types.InputMediaPhoto(media=j[0], caption= caption)]

                else :
                    media_files += [types.InputMediaPhoto(media=j[0])]

                first = 1

            elif j[1] == "video":

                size = 0

                await asyncio.sleep(random.randint(min_waiting_time_singl_media , max_waiting_time_singl_media))

                try : 

                    response =  requests.head(j[0])

                    size = (int(response.headers.get('Content-Length', 0))  / (1024 * 1024))

                except :

                    await asyncio.sleep(2)

                    try :

                        response = requests.head(j[0])

                        size = (int(response.headers.get('Content-Length', 0))  / (1024 * 1024))

                    except :
                        pass

                if size > 0 :

                    if max_vedio_size > size :
    
                        try :

                            await bot.send_video(way1_instagram, video= j[0], caption= caption)
                            total_success += 1

                        except errors.FloodWait as e:

                            await asyncio.sleep(e.value)

                            try :

                                await bot.send_video(way1_instagram, video= j[0], caption= caption)
                                total_success += 1

                            except :
                                total_errors +=  1

                        except :

                            total_errors +=  1

                        if first == 0 :
                            media_files += [types.InputMediaVideo(media= j[0], caption= caption)]

                        else :
                            media_files += [types.InputMediaVideo(media=j[0] )]

                        first = 1

                    else :
                        size_warrning += 1

        if data[i]["type"] == "multi"  and send_multi_media:

            await asyncio.sleep(random.randint(min_waiting_time_multi_media , max_waiting_time_multi_media))

            try :

                await bot.send_media_group(way1_instagram, media=media_files)
                total_success += len(data[i]["links"])

            except errors.FloodWait as e:

                await asyncio.sleep(e.value)

                try :

                    await bot.send_media_group(way1_instagram, media=media_files)
                    total_success += 1

                except :
                    total_errors +=  1

            except :

                total_errors +=  1


bot.run()


