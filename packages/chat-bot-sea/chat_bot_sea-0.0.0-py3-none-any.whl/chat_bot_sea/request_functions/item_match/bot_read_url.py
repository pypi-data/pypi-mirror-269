import re
from core_pro import Drive


def read_url(user_message: str):
    pattern = 'https://drive.google.com/(.*)'
    lst_file = re.findall(pattern, user_message)
    print(lst_file)
    lst_file_id = [i.split('/')[-1] for i in lst_file]
    for u in lst_file_id:
        save_path = Drive().drive_download(u, '')
        print(save_path)
