#from proxy_manager_g4 import ProxyManager
#from proxy_manager_g4.consts import PROTOCOL_HTTPS
from bs4 import BeautifulSoup
import requests
from random import randint
from threading import Thread
import mysql.connector
from proxy_checking import ProxyChecker
from datetime import datetime

class proxys():
    def __init__(self, padet, proxythreading, uid, proxyfiyat, proxyparabirimi):
        self.veritabani()
        self.threading(proxythreading, padet, uid, proxyfiyat, proxyparabirimi)

    def GetProxy(self):
        url = 'https://free-proxy-list.net/'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        div = soup.find('div', class_='table-responsive')
        tbody = div.find("tbody")
        proxies = tbody.find_all("tr")
        proxy = proxies[randint(0, len(proxies) - 1)]

        proxy_ip = proxy.find_all("td")[0].get_text()
        proxy_port = proxy.find_all("td")[1].get_text()

        return proxy_ip + ":" + proxy_port

    def proxycreating(self,padet, threadsayi, uid, proxyfiyat, proxyparabirimi):
        while True:
            self.count = int(padet)
            for i in range(1, 100000000):
                if i == self.count:
                    print(f"Adet : {self.count} Proxy Üretilip Kontrol Edilmiştir.")
                    break
                    break

                else:
                    try:
                        # proxy_manager = ProxyManager(protocol=PROTOCOL_HTTPS, anonymity=True)
                        # proxy = proxy_manager.get_random()

                        proxy = self.GetProxy()
                        checker = ProxyChecker()
                        r = checker.check_proxy(f'{proxy}')
                        print(r['status'])
                        if r['status'] == True:
                            print(f"{i}. Thread: {threadsayi} Uid : {uid} Proxy : {proxy}")
                            self.veritabani(islem='Ekle', uid=uid, proxy=proxy, pfiyat=proxyfiyat, pparabirimi=proxyparabirimi)
                        elif r['status'] == False:
                            print(f"Thread: {threadsayi} uid : {uid} Proxy : {proxy} HATALI!")
                    except:
                        print(f"Thread: {threadsayi} uid : {uid} Proxy : {proxy} HATALI!")

    def threading(self, pthreading, padet, uid, proxyfiyat, proxyparabirimi):
        for i in range(1, int(pthreading) + 1):
            t1 = Thread(target=self.proxycreating, args=(padet, i, uid, proxyfiyat, proxyparabirimi))
            t1.start()

    def veritabani(self, islem=None, uid=None, proxy=None, pfiyat=None, pparabirimi=None):
        self.db = mysql.connector.connect(
            host="localhost",
            user="barron4335",
            password="1968Hram",
            database="dwebsite"
        )
        self.cursor = self.db.cursor(dictionary=True)
        if islem == 'Ekle':
            sql = "SELECT * FROM proxies WHERE proxy_adress = '"+str(proxy)+"'"
            self.cursor.execute(sql)
            sproxy = self.cursor.fetchall()

            if sproxy:
                print("Daha önce veritabanına kayıt edilmiştir.")
            else:
                durum = 1
                bugun = datetime.now()
                tarih = f"{bugun.year}-{bugun.month}-{bugun.day} {bugun.hour}:{bugun.minute}:{bugun.second}"
                sql1 = 'INSERT INTO proxies SET user_id=%s, proxy_title=%s, proxy_content=%s, proxy_adress=%s, proxy_activate=%s, proxy_create_date=%s, proxy_update_date=%s, proxy_fiyat=%s, proxy_para_birimi=%s, proxy_url=%s'
                self.cursor.execute(sql1, (str(uid), str(proxy), str(proxy), str(proxy), durum, tarih, tarih, pfiyat, pparabirimi, str(proxy),))
                self.db.commit()
                print(f"Proxy: {proxy} veritabanına eklendi.")

proxys(padet=200, proxythreading=5, uid=2, proxyfiyat=2, proxyparabirimi='USD')