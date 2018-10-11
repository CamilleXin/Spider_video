import requests
from bs4 import BeautifulSoup
import re
from fontTools.ttLib import TTFont


class MaoYan(object):
    def __init__(self):
        self.url = 'https://maoyan.com/films/1203437'
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "cookie": "__mta=214880808.1539074790418.1539152718429.1539154074286.8; uuid_n_v=v1; uuid=CCFDBDE0CB9F11E8B2EA6B5A928BA8176BC1B00CF46047FABB68DFA9472C3D13; _lxsdk_cuid=16658018cfbc8-0b6a83e0bfdcf6-8383268-e1000-16658018cfcc8; _lxsdk=CCFDBDE0CB9F11E8B2EA6B5A928BA8176BC1B00CF46047FABB68DFA9472C3D13; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; __mta=214880808.1539074790418.1539074792850.1539131818372.3; _csrf=3c7ff9068727856d68a5cbbfa0817409a7824edf1622a544fea19d00a54eff50; _lxsdk_s=1665ca6a5d4-788-c73-ef7%7C%7C4",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
        }

    # 发送请求获得响应
    def get_html(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def get_movieName(self, html):
        soup = BeautifulSoup(html, "lxml")
        movieName = soup.find_all('h3')[0].text
        return movieName

    # 创建 self.font 属性
    def create_font(self, font_file):
        url = 'http:' + font_file
        new_file = self.get_html(url)
        with open('maoyan.woff', 'wb') as f:
            f.write(new_file)
        baseFont = TTFont('base.otf')
        maoyanFont = TTFont('maoyan.woff')
        uniList = maoyanFont['cmap'].tables[0].ttFont.getGlyphOrder()
        self.numList = []
        baseNumList = ['.', '3', '5', '1', '2', '7', '0', '6', '9', '8', '4']
        baseUniCode = ['x', 'uniE64B', 'uniE183', 'uniED06', 'uniE1AC', 'uniEA2D', 'uniEBF8',
                       'uniE831', 'uniF654', 'uniF25B', 'uniE3EB']
        self.maoyanUnicode = []
        for i in range(1, 12):
            maoyanGlyph = maoyanFont['glyf'][uniList[i]]
            for j in range(11):
                baseGlyph = baseFont['glyf'][baseUniCode[j]]
                if maoyanGlyph == baseGlyph:
                    self.maoyanUnicode.append(uniList[i])
                    self.numList.append(baseNumList[j])
                    break

    # 把获取到的数据用字体对应起来，得到真实数据
    def modify_data(self, data):
        for number, code in enumerate(self.maoyanUnicode):
            gly = code.replace('uni', '&#x').lower() + ';'
            if gly in data:
                data = data.replace(gly, str(self.numList[self.maoyanUnicode.index(code)]))
        return data

    def start_crawl(self):
        html = self.get_html(self.url).decode('utf-8')
        movieName = self.get_movieName(html)

        # 正则匹配字体文件
        font_file = re.findall(r"url\('(//.*.woff)'\) format\('woff'\)", html)[0]
        self.create_font(font_file)

        # 正则匹配累计票房
        ticket_number = ''.join(
            re.findall(r'''<span class="stonefont">(.*?)</span><span class="unit">(亿)</span>''', html)[0])
        ticket_number = self.modify_data(ticket_number)
        print(movieName, '累计票房: %s' % ticket_number)


if __name__ == '__main__':
    maoyan = MaoYan()
    maoyan.start_crawl()
