# 博客网站生成器3.0(tf-idf版)

## 1.简介:
        手动上传文章及关键字,根据tf-idf算法自动生成博客页面并缓存在本地
        技术栈:
		语言:Python3.9
		框架:FastApi
		服务:uvicorn
		前端模板引擎:jinja2
## 2.运行:
        1.上传文章TXT文件:
            以文章标题为文件名,将所有TXT文件上传到'content_txt'文件夹里,编码为:utf-8
        2.修复文章文件名
            上传文件后,运行'alter_TxtName.py',将修复文件名特殊符号
        3.上传关键字
            将所有关键字放到'keyword.txt'里,不能有特殊字符,编码为:utf-8
        4.根据tf-idf算法,将最匹配关键的文章进行排序
            运行'9_tf-idf.py',排序结果保存在:'tf_idf_data.json'
        5.清理缓存
            删除'cache'文件夹里所有文件
        6.设置主页,分类页,详情页数据,缓存及其他
            在'config.py'里设置
        7.搭建环境
            pip install fastapi
            pip install uvicorn
            pip install jinja2
            pip install fastapi
        8.运行程序
            main.py

## 3.模板数据
        详见'templates'下html文件