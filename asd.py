import requests
from bs4 import BeautifulSoup

class scrape():
    def __init__(self , url):
        self.url = url
        # self.main(url)
        
    def get_url ( url):
        '''
        get url function to get the url of the post
        '''
        sess = requests.Session()
        r = sess.get(url)
        return r

    def soup_url( url):
        """
        get api from each link of the search links (links3) and get the specification
        """
        r= get_url(url)
        soup = BeautifulSoup(r.text , "html.parser")
        spec = soup.select('.customP.overflowHidden>ul>li')
        return filter( None, [print(BeautifulSoup(str(i)).get_text().replace("\n" , '').replace("\s ","")) for i in spec])

    def get_images ( api_url):
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
        response = requests.post('https://jo.opensooq.com/ar/post/render-gallery', params=params, cookies=cookies, headers=headers, data=data)
        response.text
        soup = BeautifulSoup(response.text , "html.parser")
        all_imgs = soup.find_all('img', src=True)
        print(f"there is {len(all_imgs)} image")
        print(*[i['src'] for i in all_imgs if '1024x0' in i['src']] , sep='\n')
        

    def page_c( self):
        '''
        عد كل الصفحات في البحث 
        takes a url and returns a list of all the pages in the search
        '''
        count = 1 
        while True :   
            res = requests.get(url.format(count))
            links3.extend(self.page_l(res))
            if 'لم يتم العثور على نتائج' in res.text :
                print (f"there is {count} pages")
                return count
            count += 1
    @classmethod     
    def page_l( r):
        """
        عد كل الروابط في صفحة البحث و تجميعها في مصفوفة links3 و ترجعها للمصفوفة الرئيسية
        counts all the links in a page
        """
        soup = BeautifulSoup(r.text , "html.parser")
        links = soup.select("h2.fRight>a",href = True)
        links2 = ['https://jo.opensooq.com'+i['href'] for i in links]
        return links2

    def get_api_url( url):
        """
        get api page from url link
        """
        r=get_url(url)
        r_t=r.text
        api_url = re.search("(?!galleryUrl)*.{12}render-gallery\?id=\d{2,20}", r_t)
        api_url = str(api_url.group(0).replace("\\", ""))
        api_url = f'https://jo.opensooq.com/{api_url}'
        return api_url  
            

    def main(url):
        url = str(url)+"&page={}"
        print(self.page_c(url))
        x=0
        for i in links3:
            x+=1
            print(f'{x}- {i}')
            #print images here 
            api= get_api_url(i)
    #         print("apiurl is :"+ api)
            get_images(api)
            soup_url(i)

    '''
    result should be like this :
    title
    specifications 
    images 
    '''

if __name__ == "__main__":
    links3=[]
    # url = str(input("url :"))
    # url example
    # https://jo.opensooq.com/ar/find?cat_id=1775&term=%D9%81%D9%88%D8%B1%D8%AF+%D9%81%D9%8A%D9%88%D8%AC%D9%86+%D9%81%D9%8A+%D8%B3%D9%8A%D8%A7%D8%B1%D8%A7%D8%AA+%D9%84%D9%84%D8%A8%D9%8A%D8%B9&scid=&neighborhood_id=&have_images=&allposts=&onlyPremiumAds=&onlyDonation=&onlyPrice=&onlyUrgent=&onlyShops=&onlyMemberships=&onlyBuynow=&memberId=&sort=record_posted_date.desc")
    url = "https://jo.opensooq.com/ar/find?cat_id=1775&term=%D9%81%D9%88%D8%B1%D8%AF+%D9%81%D9%8A%D9%88%D8%AC%D9%86+%D9%81%D9%8A+%D8%B3%D9%8A%D8%A7%D8%B1%D8%A7%D8%AA+%D9%84%D9%84%D8%A8%D9%8A%D8%B9&scid=&neighborhood_id=&have_images=&allposts=&onlyPremiumAds=&onlyDonation=&onlyPrice=&onlyUrgent=&onlyShops=&onlyMemberships=&onlyBuynow=&memberId=&sort=record_posted_date.desc"
    # s=scrape(url)
    # print(scrape.get_url(url).text)
    scrape.page_c(url)
    # s = scrape
    