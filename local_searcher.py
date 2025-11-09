import requests , instaloader , time  , sqlite3 , os
from datetime import datetime, timedelta  
import json
from pyrogram import Client

# ⚠️⚠️ warning : connect to a perfect vpn if you ara in iran

# _____________________________ basic data __________________________________


time_start = time.time()

search_hours = 170 # hours
max_search_count = 20 # count of the last posts

max_vedio_size = 20 # MB
max_caption_size = 100 # put === 0 if you dont want any caption

max_try_for_links = 3
max_try_for_username = 3
max_count_untime = 4 # for more efficency

file_name_save_first_links = "links.json"
totall_file_name = "result.json"


send_auto_to_bot = True
chat_id_to_send = 5507957134
bot = Client("bot", api_id='22901108', api_hash='0e94c7511deb3550372f2dc18a562770', bot_token="7210735611:AAFc8uFasnL_3QhdwUIPjB1QyIO7kmUx7jk")

# # _____________________________ data base __________________________________


def create_table_Channel(conn): 
    
    cursor = conn.cursor()

    columns = {

        "links" : [

            ("link", "INTIGER", True),

        ] , 
    }

    for i in columns.keys() :

        create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {i} (
                {", ".join("`"+col[0]+"` "+col[1]+" PRIMARY KEY" if col[2] else "`"+col[0]+"` "+col[1] for col in columns[i])}
            );
        """
        cursor.execute(create_table_sql)

    conn.commit()
    cursor.close()

def get_databases_used_links(conn):


    links = []

    cursor = conn.cursor()
    cursor.execute("SELECT link FROM links WHERE link IS NOT NULL")
    links_list = cursor.fetchall()
    cursor.close()

    for i in links_list :
        links+=[i[0]]

    return links

def  add_link_to_databse(conn , new_link) :

    try : 
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO links VALUES(?);", [new_link])
        cursor.close()
        conn.commit()
    except :
        pass

conn = sqlite3.connect("database.db") # connect to the database
create_table_Channel(conn) # create tabel for database if that is not exist
databases_used_links =  get_databases_used_links(conn)

# _____________________________ help functions __________________________________

def load() :

    L = instaloader.Instaloader()

    if os.path.exists("session"):

        L.load_session_from_file("ufeabbjz2024" , "session")

    else:
        L.login("ufeabbjz2024", "Amir#amir#123456")
        L.save_session_to_file("session")
    
    return L

def following_users_func() :

    # L = load()

    # try : # just for test the session
    #     profile = instaloader.Profile.from_username(L.context, L.test_login())
    # except :
    #     L.login( "ufeabbjz2024", "Amir#amir#123456")
    #     L.save_session_to_file("session")
    #     profile = instaloader.Profile.from_username(L.context, L.test_login())

    # following_users = []
    # for x in profile.get_followees():
    #     following_users += [x.username]  

    # print(following_users)

    following_users = ["memeclub.fa"  , "shiri.meme"  , "the.faunos"  , "nab_meme" , "animationizm" , "dsdmemer" , "saul_meme"  , "nemaxt"  ,  "froopy_lands"  , "haj.mime" , "amir_hangoverr" , "darya.meme" , "fullmemevideos" , "ganj.meme" , "sno.memer" , "meme.ology.ir" , "abgosht_meme" , "mestr_cheshmak" , "_portalmeme_" ,  "gigaa.meme" , "mixxhoodmeme" , "nameasar" , "nimatekido" , "darghuztv" , "jiz_meme" , "cuzn0"  , "memezaghasemi"  , "_rexmeme_"  , "challento"  , "night.club_meme"  , "meme.ahi"  , "sargon.meme"  , "zeus._meme" , "gungmeme" , "templar.meme" , "tiltoons" , "memecadeh" , "persian__meme_" , "only.commente"  , "neptune__meme"  , "sinaserpent"  , "tonixmeme" , "tanz__kilip" , "bi__rabt" , "goldenarashmc" ,  "kharposht_karkoshte" ,  "jeffrypour" ,  "roodebor_82" ,  "shabake.17" ,  "tv.mez" ,  "goloboll" ,  "matarzzak" ,  "fun_laugh_110" ,  "memesss_land" ,  "toxicmemefarsi" ,  "gungmeme" ,  "poison.msm" ,  "brozzmeme_" ,  "amirmeme_" ] 

    return following_users

def get_last_links(usernames , used_links) :

    global conn , max_try_for_username , max_search_count , max_try_for_links , max_count_untime , search_hours , file_name_save_first_links , databases_used_links

    data = dict()

    hours = datetime.utcnow() - timedelta(hours=search_hours)

    adnis_useranme = 0

    F = load()

    print(f"total usernames : {len(usernames)}")

    for username in usernames:

        adnis_useranme +=  1

        time_start_search = time.time()

        if (username not in data.keys()) and (username != "amirmoradi_2004") :

            for i in range(max_try_for_username) :

                
                # profile = instaloader.Profile.from_username(F.context, username)
                # sucssusfult_try = True
                # break

                try : 

                    profile = instaloader.Profile.from_username(F.context, username)


                    count = 0
                    recent_posts = []
                    count_untime = 0

                    for o in range(max_try_for_username) :

                        try :

                            for post in profile.get_posts():

                                if (count > max_search_count) or (count_untime >= max_count_untime) :
                                    break

                                else :

                                    count += 1

                                    new_link = f"https://www.instagram.com/p/{post.shortcode}/"

                                    if (post.date_utc > hours ) and (new_link not in databases_used_links) and (new_link not in used_links) :

                                        recent_posts += [new_link]

                                    else :
                                        count_untime += 1

                            break

                        except instaloader.exceptions.ConnectionException :

                            count = 0
                            recent_posts = []
                            count_untime = 0

                            print("🔴🔴There is connection Error🔴🔴")
                            
                        data.update({username : recent_posts})

                    
                    print(f"{adnis_useranme} - {username}" , " || " , f"links : {len(recent_posts)}" , f"- time : {int(time.time() - time_start_search)}")

                    break

                except :
                    time.sleep(1)
                    print(f"🔴 lose to connect to {username} for get the last links - try : {i}")

            else :
                print(f"⚠️⚠️⚠️ Faild username : {username} ⚠️⚠️⚠️")

        time.sleep(1)

    if data :

        with open(file_name_save_first_links , 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return True

    else :
        return False
    
def download_and_send(url , H) :

    time.sleep(0.5)

    global max_vedio_size , max_caption_size

    secssusfuly_try = False

    for i in range(max_try_for_links) :
    
        try:
            post = instaloader.Post.from_shortcode(H.context, url.split("/")[-2])
            secssusfuly_try = True
            break

        except :
            print(f"🟡 lose to download  {url} - try : {i}")
            time.sleep(2)
    
    if secssusfuly_try :

        caption = f"{url}\n\n"

        if post.caption and max_caption_size != 0:

            if len(post.caption) > max_caption_size :
                caption += post.caption[:max_caption_size]

            elif 0 < len(post.caption) < max_caption_size:
                caption += post.caption

        if post.typename == 'GraphImage':

            z =  {"caption" : caption , "links": [[post.url , "photo"]] , "type" : "single"}
        
        elif post.typename == 'GraphVideo' and post.video_url:
 
            z =  {"caption" : caption , "links" : [[post.video_url , "video" ]], "type" : "single"}

        elif post.typename == 'GraphSidecar':

            media_files = []

            for x in post.get_sidecar_nodes():

                if x.is_video:
 
                    media_files += [[x.video_url , "video" ]]

                else:

                    media_files += [[x.display_url , "photo" ]]

            z = {"caption" : caption , "links" : media_files , "type" : "multi"}

        else :
            print("⚠️⚠️⚠️⚠️ unknow typr of post :) >>>>>>>>>>>>>>>>>>>>>> {post.typename}")
            return False
            
        return z
        
    else :
        return False
    
def calucatur() :

    global file_name_save_first_links , databases_used_links

    result = dict()

    with open(file_name_save_first_links  , 'r', encoding='utf-8') as file:
        data = json.load(file)    


    now_count = 0 

    H = load() # H = instaloader.Instaloader() 

    for i in data.keys() :

        now_count += 1
        count_s = 0

        r_time = time.time()

        for j in data[i] :

            if j not in databases_used_links :

                x = download_and_send(j)

                if x != False:

                    count_s += 1
                    result.update({j : x})
        
        if len(data[i]) > 0 :
            print(f"{now_count} - {i}" , " || " , f"totall links : {len(data[i])}" , "———" , f"secssusfuly : {count_s} , time : {int(time.time() - r_time)}")

        time.sleep(2)

    return result


# _____________________________ start job ! __________________________________


following_users = following_users_func()

get_links = get_last_links(following_users , databases_used_links) 

# result = calucatur()

# if result : # we got the downloadabel link for send in instagram
    
#     for i in result.keys():
#         add_link_to_databse(conn , i)

#     with open(totall_file_name, 'w', encoding='utf-8') as f:
#         json.dump(result, f, ensure_ascii=False, indent=4)

#     print("finished !")
#     print(time.time() - time_start)

#     # _____________________________ send file to user  __________________________________

#     if send_auto_to_bot :

#         with bot:
#             bot.send_document(chat_id=chat_id_to_send, document=totall_file_name)


