from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from io import BytesIO

#limited, so not an option
def get_product_go_upc(self,upc):
    print(upc)
    try:
        response=requests.get(f"https://go-upc.com/search?q={upc}")
        if response.status_code == 200:
            soup=bs(response.text,"html.parser")
            left_col=soup.find_all("div",{"class":"left-column"})
            if len(left_col) < 1:
                return None
            else:
                return left_col
    except Exception as e:
        print(e)
        print(repr(e))
        return None


def processData(data):
    if data:
        name=''
        img_url=''
        upc=''
        category=''
        for i in data:
            name=i.find("h1",{"class":"product-name"}).text
            img_url=i.find("img")['src']
            
            t=i.find_all("table")
            for st in t:    
                table=pd.read_html(BytesIO(str(st).encode()))
                for t in table:
                    for row in t.itertuples():
                        if row._1 == "UPC":
                            upc=row._2
                        if row._1 == "Category":
                            category=row._2
        return {
            'name':name,
            'img_url':img_url,
            'upc':upc,
            'tags':category}
                


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        a=get_product_go_upc(None,upc=sys.argv[1])
        print(a)
        processData(a)
        #print(a)
    else:
        print(f"please provide a upc via arg1, i.e. python3 ./{sys.argv[0]} $UPC")
