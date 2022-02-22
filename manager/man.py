import argparse
import requests
import wget
import os
from zipfile import ZipFile
import shutil
import json

MODEL_STORAGE_SERVER = 'https://raw.githubusercontent.com/YainsidaeSpeechSynthesis/model-lists/master/lists.json'
DIR = r'C:/YainTTS/models'

def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

def delete_old(code):
    for filename in next(os.walk(DIR))[1]:
        if code in filename.split("-")[0]:
            shutil.rmtree(os.path.join(DIR, filename))

def get_my_model_ver(code):
    for filename in next(os.walk(DIR))[1]:
        if code in filename.split("-")[0]:
            return "-".join(filename.split("-")[1:])
    
def update_model(meta, code):
    # make folders of DIR when not exist
    if os.path.isdir(DIR):
        os.makedirs(DIR)
    print("버전 확인중...")
    for i in meta:
        if i.get("code") == code:
            latest_version = i.get("latest_version")
            if latest_version == get_my_model_ver(code):
                print(f"{i.get('name')}은/는 최신 버전입니다.")
                continue
            for j in i.get("versions"):
                if j.get("version") == latest_version:
                    print(f"확인 완료")
                    delete_old(code)
                    print(f"버전 {latest_version} 다운로드 중...")
                    wget.download(j.get("download_url"), out="C:\YainTTS\models\\" + code + "-" + j.get("version") + ".zip")
                    print()
                    # unzip file
                    with ZipFile("C:\YainTTS\models\\" + code + "-" + j.get("version") + ".zip", 'r') as zipObj:
                        # Extract all the contents of zip file in current directory
                        zipObj.extractall("C:\YainTTS\models\\" + code + "-" + j.get("version"))
                    
                    print(f"{i.get('name')} 업데이트 완료")
                    os.remove("C:\YainTTS\models\\" + code + "-" + j.get("version") + ".zip")
def update_recent_model():
    try:
        data = requests.get(MODEL_STORAGE_SERVER).json()
    except Exception as e:
        print("서버 접속 에러")
        return
    print("""
인물 선택

[1] 전부""")
    for i in range(len(data)):
        print(f"[{i+2}] {data[i].get('name')}")
    
    com = input("> ")
    if com == "1":
        for i in data:
            update_model(data, i.get('code'))
    else:
        try:
            com_num = int(com)-2
        except:
            print("잘못된 입력입니다.")
            return
        if com_num-2 <= len(data):
            update_model(data, data[com_num-2].get('code'))
        else:
            print("잘못된 입력입니다.")
def select_person():
    models = next(os.walk(DIR))[1]
    for i in range(len(models)):
        with open(os.path.join(DIR,models[i],"conf.json"), "r", encoding="utf8") as f:
            out = json.loads(f.read())
            print("[{}] {}".format(i+1, out.get("name")))
    com = input("> ")
    try:
        com = int(com)
    except:
        print("잘못된 입력입니다.")
        return
    if com-1 <= len(models):
        os.environ['TTS_MODEL_FILE']="/".join([DIR,models[com-1],'glowtts-v2/best_model.pth.tar'])
        os.environ['TTS_MODEL_CONFIG']="/".join([DIR,models[com-1],'glowtts-v2/config.json'])
        os.environ['VOCODER_MODEL_FILE']="/".join([DIR,models[com-1],'hifigan-v2/best_model.pth.tar'])
        os.environ['VOCODER_MODEL_CONFIG']="/".join([DIR,models[com-1],'hifigan-v2/config.json'])
        os.system("server.exe")
    else:
        print("잘못된 입력입니다.")
    # Set environment variables
    # os.environ['API_USER'] = 'username'
    # os.environ['API_PASSWORD'] = 'secret'

def run_man(args):
    print("""
야인 TTS 모델 관리자

1) 인물 선택
2) 기본 최신 업데이트

    """)
    com = input("> ")
    if com == "1":
        select_person()
    elif com == "2":
        update_recent_model()
    else:
        print("잘못된 입력입니다.")
        
def main():
    parser = argparse.ArgumentParser(description='Update the database')
    parser.add_argument('-u', '--update', action='store_true', help='Update the database')
    args = parser.parse_args()

    run_man(args)

if __name__ == '__main__':
    main()