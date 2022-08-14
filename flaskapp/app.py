from flask import Flask , render_template
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

links3=[]
result_l = []

def read_file(file_name):
    with open(file_name, 'r') as f:
        file = f.readlines()
        file = file[1]
        file = file[2:-3]
        file = file.split('\', \'')
        return file

@app.route("/")
def root():
    links3=[]
    result_l=[]
    l=[]
    l.extend(read_file('kamry') + read_file('fordResult'))
    # l= list(range(8))
    # for i in lis:
    #     print(i)
    #     input("next")
    return render_template('index1.html', loop=l)

def get_url (url):
    '''
    get url function to get the url of the post
    '''
    sess = requests.Session()
    r = sess.get(url)
    return r

def get_url2 (url):
    '''
    takes url and changes the language to english 
    get url function to get the url of the post
    '''
    
    change = re.search('/ar/', url)
    if change :
        url = url.replace('/ar/', '/en/')
    sess = requests.Session()
    r = sess.get(url)
    return r

def soup_url(url):
    """
    get specifications from url
    get api from each link of the search links (links3) and get the specification
    """
    r= get_url(url)
    soup = BeautifulSoup(r.text , "html.parser")
    spec = soup.select('.customP.overflowHidden>ul>li')
    return [(BeautifulSoup(str(i),'html.parser').get_text().replace("\n" , '').replace("\s ","")) for i in spec]

def soup_url2(url,css_class):
    """
    get api from each link of the search links (links3) and get the specification
    """
    r= get_url2(url)
    soup = BeautifulSoup(r.text , "html.parser")
    spec = soup.select(css_class)
    # print(spec)
    return spec

def get_images (api_url):
    '''
    This function takes a api url and returns a list of all the images on the page.
    '''
    url= 'https://jo.opensooq.com/ar'
    sess = requests.Session()
    r = sess.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    csrf_token = soup.select_one('meta[name="csrf-token"]')['content']
    header = {
        'X-CSRF-Token' : csrf_token,
        'X-Requested-With': 'XMLHttpRequest',
    }
    api_url = api_url
    r = sess.get(api_url , headers=header)
    response = requests.post(api_url
                             , headers=header)
    response.text
    soup = BeautifulSoup(response.text , "html.parser")
    all_imgs = soup.find_all('img', src=True)
    all_imgs = [i['src'] for i in all_imgs if '1024x0' in i['src']]
    # print(f"there is {len(all_imgs)} image")
    return all_imgs
    

def page_c(url):
    '''
    عد كل الصفحات في البحث 
    takes a url and returns a list of all the pages in the search
    '''
    count = 1 
    while True :   
        res = get_url2(url.format(count))
        mark = soup_url2(url.format(count), "span.mr15")[0]
        mark=re.findall("\d{1,100}", BeautifulSoup(str(mark),'html.parser').get_text())
        links3.extend(page_links(res))
#         print(f'''count ------------------>{count}
# list length------------->{len(links3)}
# mark ------------------->{mark} 
# url -------------------->{url.format(count)} 
# ---------------------------------------''')
        # breakpoint("page_c")
        
        if mark[1] == mark[2] :
            # print (f"there is {count} page/s")
            return count
        count += 1
        
def page_links(r):
    """
    عد كل الروابط في صفحة البحث و تجميعها في مصفوفة links3 و ترجعها للمصفوفة الرئيسية
    counts all the links in a page
    """
    soup = BeautifulSoup(r.text , "html.parser")
    links = soup.select("h2.fRight>a",href = True)
    links2 = ['https://jo.opensooq.com'+i['href'] for i in links]
    change = re.search('/en/', links2[0])
#     print(f'''change is {change}
# first link is {links2[0]}''')
    if change :
        links2 = [i.replace('/en/','/ar/') for i in links2]
    # print(links2 , len(links2))
    # input("press enter to continue")
    # breakpoint()
    # exit
    return links2

    
def get_api_url(url):
    """
    get api page from url link
    """
    r=get_url(url)
    r_t=r.text
    api_url = re.search("(?!galleryUrl)*.{12}render-gallery\?id=\d{2,20}", r_t)
    api_url = str(api_url.group(0).replace("\\", ""))
    api_url = f'https://jo.opensooq.com{api_url}'
    return api_url  
        

def main(url):
    url = str(url)+"&page={}"
    # print(page_c(url))
    page_c(url)
    x=0
    # print(f'''
    # links -----------------------> {links3}
    # ''')
    for i in links3:
        x+=1
        # print(f'{x}- {i}')
        #print images here 
        api= get_api_url(i)
#         print("apiurl is :"+ api)
        get_images(api)
        soup_url(i)
        number = [f'link = {i}']
        # with get_images(api) as all_images:
        #     images = [f'<img src="{i}" >' for i in all_images]
        images = [f"{i}" for i in get_images(api)]
        spec=soup_url(i)
        result_l.extend(number+images+spec)
        return result_l
    # return result_l
        # print('result starts from here \n-------------------------------' , result_l)
        # print(type(number ))
        # print( type(images))
        # print( type(spec))
#         print(f'''-----------------
# there is {links3}
# api is {api}
# image links {get_images(api)} 
# specifications {soup_url(i)}
# ----------------------''')
    return result_l
        # breakpoint()
        # input("press enter to continue")

'''
result should be like this :
title
specifications 
images 
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(debug=True, use_reloader=True)
    # global links3 ,result_l 
    # links3 =[]
    # result_l=[]
#     url = str(input("url :"))
    # url example
    # https://jo.opensooq.com/ar/find?cat_id=1775&term=%D9%81%D9%88%D8%B1%D8%AF+%D9%81%D9%8A%D9%88%D8%AC%D9%86+%D9%81%D9%8A+%D8%B3%D9%8A%D8%A7%D8%B1%D8%A7%D8%AA+%D9%84%D9%84%D8%A8%D9%8A%D8%B9&scid=&neighborhood_id=&have_images=&allposts=&onlyPremiumAds=&onlyDonation=&onlyPrice=&onlyUrgent=&onlyShops=&onlyMemberships=&onlyBuynow=&memberId=&sort=record_posted_date.desc")
    # url = "https://jo.opensooq.com/ar/find?cat_id=1775&term=%D9%81%D9%88%D8%B1%D8%AF+%D9%81%D9%8A%D9%88%D8%AC%D9%86+%D9%81%D9%8A+%D8%B3%D9%8A%D8%A7%D8%B1%D8%A7%D8%AA+%D9%84%D9%84%D8%A8%D9%8A%D8%B9&scid=&neighborhood_id=&have_images=&allposts=&onlyPremiumAds=&onlyDonation=&onlyPrice=&onlyUrgent=&onlyShops=&onlyMemberships=&onlyBuynow=&memberId=&sort=record_posted_date.desc"
    # url="https://jo.opensooq.com/ar/find?have_images=&allposts=&onlyPremiumAds=&onlyDonation=&onlyPrice=&onlyUrgent=&onlyShops=&onlyMemberships=&onlyBuynow=&memberId=&sort=record_posted_date.desc&term=%D9%81%D9%88%D8%B1%D8%AF+%D9%81%D9%8A%D9%88%D8%AC%D9%86+2019+%D9%81%D8%AD%D8%B5+%D9%83%D8%A7%D9%85%D9%84+%D8%AC%D9%85%D8%B1%D9%83+%D8%AC%D8%AF%D9%8A%D8%AF&cat_id=&scid=&city="
    # main(url)
    # result_l = main(url)
    # print(type(result_l), len(result_l))
    # l = read_file('kamry') 
    # read_file('./kamry')
    
    # l =[read_file('kamry') ]
    # for i in lis:
    #     print(i)
    #     input("next")
    # return render_template('hello.html', name=name)