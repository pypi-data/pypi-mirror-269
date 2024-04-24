from core_pro import Drive
import re

# url = 'https://drive.google.com/file/d/1SU-YjuibMc1xO4KzDdVTSlODhLHrFXlx/view?pli=1'
# url = '1ROTEkIcnzvsVHRxL97LtloEFT2fDa7Qz'
# url = '1vrcncbs1YGy9rWLBG3s35-mGpcUB8-A7'
# url = 'https://drive.google.com/file/d/1ROTEkIcnzvsVHRxL97LtloEFT2fDa7Qz/view?usp=sharing'
# Drive().get_file_info(url)
# Drive().drive_download(url, '')

text = """
nonFSS item (database): https://drive.google.com/drive/u/0/folders/1vrcncbs1YGy9rWLBG3s35-mGpcUB8-A7
FSS item (query): https://drive.google.com/drive/u/0/folders/1vrcncbs1YGy9rWLBG3s35-mGpcUB8-A7
"""
pattern = 'https://drive.google.com/(.*)'
lst_file = re.findall(pattern, text)
lst_file_id = [i.split('/')[-1] for i in lst_file]
Drive().get_file_info(lst_file_id[0])