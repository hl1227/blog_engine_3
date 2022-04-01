import os,re

for file_name in os.listdir('./content_txt'):

    b=re.sub(r"[#%&/\\^`|]",'',file_name.replace('.txt','').replace('  ','').replace('-',' ').replace('\xa0','').replace('\t','').replace('\r','').replace('\u3000',''))+'.txt'
    os.rename(f'./content_txt/{file_name}',f'./content_txt/{b}')
