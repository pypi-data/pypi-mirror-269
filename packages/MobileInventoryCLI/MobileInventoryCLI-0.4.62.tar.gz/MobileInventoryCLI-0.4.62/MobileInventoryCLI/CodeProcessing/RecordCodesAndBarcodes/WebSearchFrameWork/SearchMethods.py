from bs4 import BeautifulSoup as bs
import requests



upc="842595106596"
def get_product_go_upc(self,upc):
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

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(get_product_go_upc(None,upc=sys.argv[1]))
    else:
        print(f"please provide a upc via arg1, i.e. python3 ./{sys.argv[0]} $UPC")
