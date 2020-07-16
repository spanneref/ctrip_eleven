# coding:utf-8
import requests
import datetime
from get_eleven2 import CtripWSClient


class CtripSpider(object):
    """携程酒店爬虫类"""

    def __init__(self):
        self.start_url = "https://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx"

        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            "referer": "https://hotels.ctrip.com/hotel/shanghai2",
            "cookie": """magicid=H8/t9huXb59N6RXPv4sx3xKKNGsG9HJrwqgB1Rl0UeHBaLSQv4yIN4/TI76Mhhde; _RSG=794v.38nA.DkR6unCgYfYA; _RDG=28b0ca71550a21286238d56a142807a8c9; _RGUID=df8ac480-fee4-4247-a8a9-8aa331e066ee; MKT_CKID=1594211759725.4e2p6.gj10; _ga=GA1.2.729163684.1594211760; _abtest_userid=3ba872c7-083c-4537-8010-63591dc0dbd5; Session=SmartLinkCode=U155952&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; librauuid=7Sm05cXO4FZMTcNAod; hoteluuid=mcqF2NdzAbmq2AT0; _gid=GA1.2.1239141853.1594604892; GUID=09031087210109863870; nfes_isSupportWebP=1; MKT_Pagesource=PC; MKT_OrderClick=ASID=4897155952&AID=4897&CSID=155952&OUID=index&CT=1594789306684&CURL=https%3A%2F%2Fwww.ctrip.com%2F%3Fsid%3D155952%26allianceid%3D4897%26ouid%3Dindex&VAL={"pc_vid":"1594211757909.2sv0yf"}; MKT_CKID_LMT=1594799685551; Union=SID=155952&AllianceID=4897&OUID=index; HotelDomesticVisitedHotels1=429173=0,0,4.5,2764,/200o1f000001ggx3c496B.jpg,&45900124=0,0,4.9,436,/2005180000013fsps9343.jpg,&2231618=0,0,4.8,3600,/200h0r000000hem7x1D5D.jpg,&1737627=0,0,4.8,452,/2005190000017e59e1AF6.jpg,&8019672=0,0,4.6,1357,/20071a000001908in0EC6.jpg,&31638714=0,0,4.8,1480,/200u14000000vsqa71E70.jpg,; _RF1=120.229.20.222; HotelCityID=1split%E5%8C%97%E4%BA%ACsplitBeijingsplit2020-7-16split2020-07-17split0; ASP.NET_SessionId=lxjxwm0rus4jlinojprjq44k; OID_ForOnlineHotel=15942117579092sv0yf1594873838698102032; _bfi=p1%3D102002%26p2%3D102002%26v1%3D160%26v2%3D159; _jzqco=%7C%7C%7C%7C1594799685719%7C1.84965262.1594211759741.1594874318486.1594880601493.1594874318486.1594880601493.undefined.0.0.109.109; __zpspc=9.17.1594880601.1594880601.1%232%7Cwww.baidu.com%7C%7C%7C%25E6%2590%25BA%25E7%25A8%258B%7C%23; appFloatCnt=74; _bfa=1.1594211757909.2sv0yf.1.1594880599168.1594885361758.19.161.153001; _bfs=1.1; hotelhst=2012709687"""
        }
        self.formdata = {
            "__VIEWSTATEGENERATOR": "DB1FBB6D",
            "cityName": "%E5%8C%97%E4%BA%AC",
            "RoomGuestCount": "1,1,0",
            "txtkeyword": "",
            "Resource": "",
            "Room": "",
            "Paymentterm": "",
            "BRev": "",
            "Minstate": "",
            "PromoteType": "",
            "PromoteDate": "",
            "operationtype": "NEWHOTELORDER",
            "PromoteStartDate": "",
            "PromoteEndDate": "",
            "OrderID": "",
            "RoomNum": "",
            "IsOnlyAirHotel": "F",
            "cityId": "1",
            "cityPY": "beijing",
            "cityCode": "010",
            "cityLat": "39.9105329229",
            "cityLng": "116.413784021",
            "positionArea": "",
            "positionId": "",
            "hotelposition": "",
            "keyword": "",
            "hotelId": "",
            "htlPageView": "0",
            "hotelType": "F",
            "hasPKGHotel": "F",
            "requestTravelMoney": "F",
            "isusergiftcard": "F",
            "useFG": "F",
            "HotelEquipment": "",
            "priceRange": "-2",
            "hotelBrandId": "",
            "promotion": "F",
            "prepay": "F",
            "IsCanReserve": "F",
            "k1": "",
            "k2": "",
            "CorpPayType": "",
            "viewType": "",
            "DealSale": "",
            "ulogin": "",
            "hidTestLat": "0%7C0",
            "AllHotelIds": "",
            "psid": "",
            "isfromlist": "T",
            "ubt_price_key": "htl_search_noresult_promotion",
            "showwindow": "",
            "defaultcoupon": "",
            "isHuaZhu": "False",
            "hotelPriceLow": "",
            "unBookHotelTraceCode": "",
            "showTipFlg": "",
            "traceAdContextId": "",
            "allianceid": "0",
            "sid": "0",
            "pyramidHotels": "",
            "hotelIds": "",
            "markType": "0",
            "zone": "",
            "location": "",
            "type": "",
            "brand": "",
            "group": "",
            "feature": "",
            "equip": "",
            "bed": "",
            "breakfast": "",
            "other": "",
            "star": "",
            "sl": "",
            "s": "",
            "l": "",
            "price": "",
            "a": "0",
            "keywordLat": "",
            "keywordLon": "",
            "contrast": "0",
            "PaymentType": "",
            "CtripService": "",
            "promotionf": "",
            "allpoint": "",
            "page_id_forlog": "102002",
            "contyped": "0",
            "productcode": "",
            "orderby": "3",
            "ordertype": "0",
            "page": "1",
        }

    def get_full_data(self):
        """获取eleven,完善FormData"""
        ws = CtripWSClient('ws://127.0.0.1:8080/')
        ws.connect()
        eleven = ws.get_eleven()
        date = datetime.datetime.now()
        current_date = date.strftime('%Y-%m-%d')
        tomorrow_date = date + datetime.timedelta(days=1)
        self.formdata['eleven'] = eleven
        self.formdata['StartTime'] = current_date
        self.formdata['DepTime'] = tomorrow_date
        self.formdata['checkIn'] = current_date
        self.formdata['checkOut'] = tomorrow_date

    def parse_url(self):
        """请求数据"""
        response = requests.post(url=self.start_url, headers=self.headers, data=self.formdata)
        # print(response.text)
        print(response.status_code)
        return response

    def save_data(self, data):
        """保存数据"""
        with open('./ctrip_hotel.json', 'w') as f:
            f.write(data)

    def run(self):
        # 首先获取eleven参数，并完善formdata
        self.get_full_data()
        res = self.parse_url()
        self.save_data(res.content)


if __name__ == '__main__':
    try:
        ctrip = CtripSpider()
        ctrip.run()
    except Exception as e:
        print(e)
