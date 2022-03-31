from fastapi import APIRouter,Depends,Request,Response
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.templating import Jinja2Templates
import config,datetime,os,random,json


application = APIRouter()

templates = Jinja2Templates(directory='./templates')
'------------------------------------------------------------------------'
#关键字文件
f_category=open('./keyword.txt','r',encoding='utf-8').readlines()
f_category_list=[category.replace('\n','') for category in f_category]
#文章文件
f_title_list=os.listdir('./content_txt')
#tf_idf文件
f_tf_idf=open('./tf_idf_data.json','r',encoding='utf-8').read()
f_tf_idf_dict=json.loads(f_tf_idf)
'------------------------------------------------------------------------'
@application.get('/favicon.ico')
def favicon():
    return None

@application.get('/robots.txt')
def robots():
    f = open('./static/robots.txt', 'r',encoding='utf-8')
    content = f.read()
    f.close()
    return HTMLResponse(content=content, status_code=200)

#站点地图
@application.get('/sitemap.xml')
def sitemap(request:Request):
    domain='https://{}/'.format(request.headers.get("host"))
    date = datetime.datetime.now()
    res_1 = ''' 
            <urlset
            xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">'''
    res_1 += '<url><loc>{}</loc >'.format(domain)
    res_1 += '<lastmod>{}</lastmod>'.format(date.strftime("%Y-%m-%d")) + '<changefreq>always</changefreq>' + '<priority>1.0</priority></url>'
    for f_category in f_category_list:
        res_1 += '<url><loc>{}</loc>'.format(domain+f_category.replace(' ', '-'))
        res_1 += '<lastmod>{}</lastmod>'.format(date.strftime("%Y-%m-%d"))+'<changefreq>always</changefreq>'+'<priority>1.0</priority></url>'
    for f_title in f_title_list[:config.SITEMAP_COUNT]:
        res_1 += '<url><loc>{}</loc>'.format(domain + random.choice(f_category_list).replace(' ','-')+'/'+f_title.replace(' ','-').replace('.txt',''))
        res_1 += '<lastmod>{}</lastmod>'.format(date.strftime("%Y-%m-%d"))+'<changefreq>always</changefreq>'+'<priority>1.0</priority></url>'
    res_1 += '</urlset>'
    return Response(content=res_1, media_type='application/xml')
'------------------------------------------------------------------------'

'主页------------------------------------------------------------------------'
@application.get('/')
def index(request:Request):
    host = request.headers.get("host")
    # 主页分类数据
    random.shuffle(f_category_list)
    category_list = f_category_list[:config.INDEX_CATEGORY_COUNT]
    #  主页内容数据
    index_data_list = []
    random.shuffle(f_title_list)
    try:
        for txt_name in f_title_list[:config.INDEX_DATA_COUNT]:
            data_dict = {'title': txt_name.replace('.txt', '')}
            content = __open_file__(txt_name)
            data_dict['description'] = content[0:config.DESCRIPTION]
            index_data_list.append(data_dict)
    except Exception:
        pass
    return templates.TemplateResponse(
        'index.html', {
            "request": request,
            'code': 200,
            'msg': '成功',
            'data': {'index_data_list': index_data_list, 'category_list': category_list, 'host': host,
                     'time': datetime.datetime.now().strftime("%Y-%m-%d")}
        })

'分类页------------------------------------------------------------------------'
@application.get('/{category}')
def category(request:Request,category:str):
    category = category.replace('-', ' ')
    host = request.headers.get("host")
    if '127.0.0.1' in host:host = '127.0.0.1'
    category_f_path = f'{config.CATEGORY_CACHE_PATH}/{host}/{category}'
    if config.CATEGORY_CACHE_ENABLED and os.path.exists(f'{category_f_path}/{category}.html'):
        # 返回缓存
        f = open(f'{category_f_path}/{category}.html', 'rb')
        content = f.read()
        f.close()
        return HTMLResponse(content=content, status_code=200)
    else:
        if category in f_category_list:
            category_res=__CategoryResponse__(request,category,host)
        else:
            #当分类页分类乱入
            random_category=random.choice(f_category_list)
            category_res=__CategoryResponse__(request,random_category,host)
        if config.CATEGORY_CACHE_ENABLED:#存缓存
            if not os.path.exists(category_f_path):
                os.makedirs(category_f_path)
            file_cache_category = open(f'{category_f_path}/{category}.html', 'w+', encoding='utf-8')
            file_cache_category.write(category_res.body.decode('utf-8'))
            file_cache_category.close()
        return category_res

def __CategoryResponse__(request,category,host):
    # 分类数据
    random.shuffle(f_category_list)
    category_list = f_category_list[:config.CATEGORY_CATEGORY_COUNT]
    # 内容数据
    category_data_list = []
    for txt_name in f_tf_idf_dict[category][:config.CATEGORY_DATA_COUNT]:
        data_dict = {'title': txt_name.replace('.txt', '')}
        f_data = __open_file__(txt_name)
        data_dict['description'] = f_data[0:config.DESCRIPTION]
        category_data_list.append(data_dict)
    # 返回模板
    category_res = templates.TemplateResponse(
        'category.html', {
            "request": request,
            'code': 200,
            'msg': '成功',
            'data': {'category_data_list': category_data_list, 'category': category,
                     'category_list': category_list,
                     'host': host, 'time': datetime.datetime.now().strftime("%Y-%m-%d")}
        })
    return category_res

'详情页------------------------------------------------------------------------'
@application.get('/{category}/{title}')
def info(request:Request,category:str,title:str):
    host = request.headers.get("host")
    if '127.0.0.1' in host:host = '127.0.0.1'
    title = title.replace('-', ' ') + '.txt'
    category = category.replace('-', ' ')
    info_f_path = f'{config.INFO_CACHE_PATH}/{host}/{category}'
    if config.INFO_CACHE_ENABLED and os.path.exists(f'{info_f_path}/{title.replace(".txt","")}.html'):
        # 返回缓存
        f = open(f'{info_f_path}/{title.replace(".txt","")}.html', 'rb')
        content = f.read()
        f.close()
        return HTMLResponse(content=content, status_code=200)
    else:
        if title in f_title_list:#如果标题在
            info_res=__InfoResponse__(request,category,title,host)
        elif title not in f_title_list and category in f_category_list:#如果标题不在分类在
            random_title=random.choice(f_tf_idf_dict[category])
            info_res = __InfoResponse__(request, category,random_title,host)
        else:
            random_category=random.choice(f_category_list)
            random_title = random.choice(f_title_list)
            info_res = __InfoResponse__(request, random_category,random_title,host)
        if config.INFO_CACHE_ENABLED:# 存缓存
            # try:
            if not os.path.exists(info_f_path):
                os.makedirs(info_f_path)
            file_cache_category = open(f'{info_f_path}/{title.replace(".txt","")}.html', 'w+', encoding='utf-8')
            file_cache_category.write(info_res.body.decode('utf-8'))
            file_cache_category.close()
            # except Exception as e:
            #     print(f'缓存创建失败:{category}/{source},信息:{e}')
        return info_res

def __InfoResponse__(request,category:str,title:str,host):
    # 分类列表数据
    random.shuffle(f_category_list)
    category_list = f_category_list[:config.INFO_CATEGORY_COUNT]
    # 详情页数据
    content = __open_file__(title)
    info_data = {'title': title.replace('.txt', ''), 'content': content}
    # 详情页同分类其他数据
    other_info_data_list = []
    try:
        for txt_name in f_tf_idf_dict[category]:
            if txt_name == title:
                continue
            data_dict = {'title': txt_name.replace('.txt', '')}
            content = __open_file__(txt_name)
            data_dict['description'] = content[0:config.DESCRIPTION]
            other_info_data_list.append(data_dict)
            if len(other_info_data_list) == config.INFO_OTHER_DATA_COUNT:break
    except Exception:pass
    info_res = templates.TemplateResponse(
        'info.html', {
            "request": request,
            'code': 200,
            'msg': '成功',
            'data': {'info_data': info_data,
                     'category': category, 'category_list': category_list,
                     'time': datetime.datetime.now().strftime("%Y-%m-%d"),
                     'other_info_data_list': other_info_data_list,
                     'host': host,
                     }
        })
    return info_res

def __open_file__(txt_name):
    f=open(f'./content_txt/{txt_name}','r',encoding='utf-8')
    f_data=f.read()
    f.close()
    return f_data