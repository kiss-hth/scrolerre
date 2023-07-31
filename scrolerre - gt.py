# url="https://scrolller.com/r/ResidentEvilHentai"
import json
import os.path
import re
import time

import requests
from bs4 import BeautifulSoup

from tqdm import tqdm


def down_from_url(url, dst):
    response = requests.get(url, stream=True)  # (1)
    file_size = int(response.headers['content-length'])  # (2)
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)  # (3)
    else:
        first_byte = 0
    if first_byte >= file_size:  # (4)
        return True

    header = {"Range": f"bytes={first_byte}-{file_size}"}

    size = 0
    pbar = tqdm(total=file_size, initial=first_byte, unit='B', unit_scale=True, desc=dst)
    req = requests.get(url, headers=header, stream=True)
    with open(dst, 'ab') as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                size += len(chunk)
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return file_size == size



def main(href):
    headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
    try:
        res=requests.get(href,headers=headers)
    except:
        time.sleep(5)
        res=requests.get(href,headers=headers)
    # print(res.text)

    pages=re.findall('<script>window.scrolllerConfig="(.*?)"</script>',res.text)[0]
    pages=pages.replace('\\','')
    # print(pages)
    pages = json.loads(pages)
    # print(pages)
    # print(pages['item']['mediaSources'])
    print(pages['item']['mediaSources'][-1].get('url'))
    vurl=pages['item']['mediaSources'][-1].get('url')
    if vurl.endswith('.jpg')or vurl.endswith('png'):
        filename = "P/"
        if not os.path.exists(filename):
            os.mkdir(filename)
        media_url=vurl
    else:
        filename = "V/"
        if not os.path.exists(filename):
            os.mkdir(filename)
        # video_url="https://static.scrolller.com/proton/ElaborateFickleHornbill.mp4"
        video_url=f"https://static.scrolller.com/proton/{vurl.split('/')[-1]}"
        if vurl.startswith("https://static.scrolller.com/"):
            video_url=vurl
        # print(video_url)
        media_url=video_url
    meida_name=media_url.split('/')[-1]
    times=0
    while times<10:
        times=times+1
        try:
            te=down_from_url(media_url,filename+meida_name)
        except:
            time.sleep(10)
            te=down_from_url(media_url,filename+meida_name)
        if te:
            print(meida_name+"下载完成")
            break

if __name__ == '__main__':

    post_url = "https://api.scrolller.com/api/v2/graphql"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
    # 不中用的json
    # body={"query":" query AffiliateQuery( $url: String! $isNsfw: Boolean! ) { getAffiliateItems( url: $url isNsfw: $isNsfw ){ id siteName adUrl buttonText brandLogoUrl adPriority viewableImpressionUrl mediaSources { url width height isOptimized } } } ",
    #       "variables":{"url":"/r/ResidentEvilHentai","isNsfw":False},
    #       "authorization":None}
    # 测试iterator
    # body={"query":" query SubredditQuery( $url: String! $filter: SubredditPostFilter $iterator: String ) { getSubreddit(url: $url) { children( limit: 50 iterator: $iterator filter: $filter disabledHosts: null ) { iterator items { __typename id url title subredditId subredditTitle subredditUrl redditPath isNsfw albumUrl hasAudio fullLengthSource gfycatSource redgifsSource ownerAvatar username displayName isPaid tags isFavorite mediaSources { url width height isOptimized } blurredMediaSources { url width height isOptimized } } } } }",
    #       "variables":{"url":"/r/ResidentEvilHentai","null":None,"hostsDown":None},
    #       "authorization":None}

    body = {
        "query": " query SubredditQuery( $url: String! $filter: SubredditPostFilter $iterator: String ) { getSubreddit(url: $url) { children( limit: 50 iterator: $iterator filter: $filter disabledHosts: null ) { iterator items { __typename id url title subredditId subredditTitle subredditUrl redditPath isNsfw albumUrl hasAudio fullLengthSource gfycatSource redgifsSource ownerAvatar username displayName isPaid tags isFavorite mediaSources { url width height isOptimized } blurredMediaSources { url width height isOptimized } } } } }",
        "variables": {"url": "/r/ResidentEvilHentai", "null": None, "hostsDown": None},
        "authorization": None}
    resp = requests.post(post_url, json=body)
    # print(resp.text)
    page = json.loads(resp.text)
    items = page['data']['getSubreddit']['children']['items']
    for item in items:
        # print(item.get('url'))
        href = "https://scrolller.com" + item.get('url')
        print(href)
        # href="https://scrolller.com/sheva-amp-daemon-girls-baronstrap-resident-evil-3wmjrd15xi"
        main(href)
        # break


