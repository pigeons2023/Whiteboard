from httpx import get as httpx_get
import easygui as eg
import os
import json
from sys import exit

try:
    with open("local.json",'r',encoding='utf-8') as f:
        local_data = json.load(f)
        version = local_data['version']
except : 
    exit(0)

cdn_url = 'https://fg.pigeonserver.xyz/https://raw.githubusercontent.com/pigeons2023/Whiteboard/main/v.json'
# version = '0.6'
def check_update() -> int :
    try:
        if os.path.exists("Whiteboard_New.exe"):
            try:
                os.remove("Whiteboard_New.exe")
            except: pass
        data = httpx_get(url=cdn_url)
        version_new = data.json()['version']
        if version_new != version :
            choose = eg.buttonbox("检测到新版本，是否更新？",title='',choices=('NO','YES'))
            print("new version found")
            # if os.path.exists("updata.vbs"):
            #         try:
            #             os.remove("updata.vbs")
            #         except: pass
            # if not os.path.exists("updata.vbs"):
            #     try:
            #         with open("updata.vbs",'w',encoding='utf-8') as f:
            #             f.write(upgrade_vbs)
            #     except: pass
            if choose == 'YES':
                print("user allowed download")
                d_url = data.json()['download_url']
                download = httpx_get(url=d_url)
                with open("Whiteboard_New.exe","wb") as f :
                    f.write(download.content)
                # if os.path.exists("Whiteboard_New.exe"):
                #     try:
                #         os.system("cmd.exe /c start updata.vbs")
                #     except: pass
            else:
                print("cancel")
        else:
            print("no new version")
    except: pass

    if os.path.exists("Whiteboard_New.exe"):
        try:
            os.system("taskkill /f /im Whiteboard.exe")
            os.remove("Whiteboard.exe")
            os.rename("Whiteboard_New.exe","Whiteboard.exe")
            os.system("cmd.exe /c start Whiteboard.exe")
            # with open("local.json",'r',encoding='utf-8') as f:
            #     local_data = json.load(f)
            
            local_data['version'] = version_new
            os.remove('local.json')
            with open('local.json','w',encoding='utf-8') as f:
                json.dump(local_data,f)
        except: pass
    else: pass

check_update()

