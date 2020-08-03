import requests
import csv
from lxml import etree


def create_csv():
    '''
    创建 csv
    :return:
    '''
    with open('../data/menu.csv','w+',newline='',encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(['name','foods','score','kind'])


def get_url():
    '''
    构造 urls
    :return: urls
    '''
    urls = []
    # 家常菜
    url1 = ['https://www.xiachufang.com/category/40076/?page={}'.format(str(i))
            for i in range(1,26)]
    # 快手菜
    url2 = ['https://www.xiachufang.com/category/40077/?page={}'.format(str(i))
            for i in range(1, 26)]
    # 下饭菜
    url3 = ['https://www.xiachufang.com/category/40078/?page={}'.format(str(i))
            for i in range(1, 26)]
    # 早餐
    url4 = ['https://www.xiachufang.com/category/40071/?page={}'.format(str(i))
            for i in range(1, 26)]
    # 鱼
    url5 = ['https://www.xiachufang.com/category/957/?page={}'.format(str(i))
            for i in range(1, 26)]
    # 鸡蛋
    url6 = ['https://www.xiachufang.com/category/394/?page={}'.format(str(i))
            for i in range(1, 26)]
    # 汤羹
    url7 = ['https://www.xiachufang.com/category/20130/?page={}'.format(str(i))
            for i in range(1, 26)]
    # 烘焙
    url8 = ['https://www.xiachufang.com/category/51761/?page={}'.format(str(i))
            for i in range(1, 26)]
    # 主食
    url9 = ['https://www.xiachufang.com/category/51490/?page={}'.format(str(i))
            for i in range(1, 26)]
    # 面
    url10 = ['https://www.xiachufang.com/category/20133/?page={}'.format(str(i))
            for i in range(1, 26)]
    # 素食
    url11 = ['https://www.xiachufang.com/special/vegetarian/?page={}'.format(str(i))
            for i in range(1, 11)]
    urls = url1 + url2 + url3 + url4 + url5 + url6 + url7 + url8 + url9 + url10 + url11

    return urls


def get_html(url):
    '''
    请求获取 html
    :param url:
    :return: html
    '''
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    return response.text


def get_infos(html):
    '''
    提取数据
    :param html:
    :return: 提取后的数据 infos
    '''
    html = etree.HTML(html)
    infos = []
    # 种类
    try:
        kind = html.xpath('//h1[@class="page-title"]/text()')[0]
    except:
        kind = html.xpath('//h1[@class="page-title mb0"]/text()')[0]

    label = html.xpath('//ul[@class="list"]/li')[:20]
    for l in label:
        # 菜名
        name = l.xpath('./div/div/p[1]/a/text()')[0]
        name = name.replace(' ','').replace('\n','')
        # 食材
        food = l.xpath('./div/div/p[2]')[0]
        food = food.xpath('string(.)')
        food = food.replace(' ','').replace('\n','')
        # 评分
        score = l.xpath('./div/div/p[3]/span[1]/text()')[0]

        infos.append([name,food,score,kind])

    return infos


def write_to_csv(infos):
    '''
    写入 csv
    :param infos:
    :return:
    '''
    with open('../data/menu.csv','a+',newline='',encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerows(infos)


if __name__ == '__main__':
    create_csv()
    urls = get_url()
    for url in urls:
        html = get_html(url)
        infos = get_infos(html)
        write_to_csv(infos)
