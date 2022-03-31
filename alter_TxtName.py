import os,re

for file_name in os.listdir('./content_txt'):

    b=re.sub(r"[#%&/\\^`|]",'',file_name.replace('.txt','').replace('  ','').replace('-',' '))+'.txt'
    os.rename(f'./content_txt/{file_name}',f'./content_txt/{b}')
