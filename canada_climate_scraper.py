import requests, re, datetime
from bs4 import BeautifulSoup

class CanadaClimateScraper:
    def __init__(self):
        super().__init__()
    
    def scrape(self, city_en: str, city_zh: str):
        self.query1_url = 'https://climate.weather.gc.ca/climate_normals/station_select_1981_2010_e.html'
        self.query1_params = {
            'searchType': 'stnName',
            'txtStationName': city_en,
            'searchMethod': 'contains'
        }
        self.resp1 = requests.get(self.query1_url, params=self.query1_params)
        self.soup1 = BeautifulSoup(self.resp1.text, 'html.parser')
        self.flag = True
        for item in self.soup1.find_all('tr'):
            if '*' in item.text:
                self.location = item.find('a').text.title()
                self.link = item.find('a')['href']
                self.stnID = re.search(r'stnID=\d+', self.link).group()[6:]
                self.prov = item.find('td', {'class': 'text-right'}).text.strip()
                self.flag = False
                break
        
        if self.flag:
            self.item = self.soup1.find_all('tr')[2]
            self.location = self.item.find('a').text.title()
            self.link = self.item.find('a')['href']
            self.stnID = re.search(r'stnID=\d+', self.link).group()[6:]
            self.prov = self.item.find('td', {'class': 'text-right'}).text.strip()

        self.query2_url = 'https://climate.weather.gc.ca/climate_normals/results_1981_2010_e.html?'
        self.query2_params = {
            'searchType': 'stnName',
            'txtStationName': city_en,
            'searchMethod': 'contains',
            'txtCentralLatMin': 0,
            'txtCentralLatSec': 0,
            'txtCentralLongMin': 0,
            'txtCentralLongSec': 0,
            'stnID': self.stnID,
            'dispBack': 0
        }
        self.resp2 = requests.get(self.query2_url, params=self.query2_params)
        self.soup2 = BeautifulSoup(self.resp2.text, 'html.parser')
        self.panel = self.soup2.find('details', {'id': 'station-metadata'})
        for item in self.panel.find_all('div', {'class': 'row'}):
            if 'Climate' in item.text:
                self.climateID = item.find_all('div')[1].text.strip().split('\n')[1]
                break
        
        self.final_url = 'https://climate.weather.gc.ca/climate_normals/bulk_data_e.html'
        self.final_params = {
            "ffmt": "xml",
            "lang": "e",
            "yr": 1981,
            "stnID": self.stnID,
            "prov": self.prov,
            "climateID": self.climateID + '+++++++++++++',
            "submit": "Download+Data"
        }

        self.res_resp = requests.get(self.final_url, params=self.final_params)
        self.res_soup = BeautifulSoup(self.res_resp.text, 'lxml')
        
        res =  '{{Infobox Weather\n'
        res += '| location = {}（平均数据1981－2010年）\n'.format(city_zh)
        res += '| metric first = yes\n'
        res += '| single line = yes\n'
        try:
            res += '| Jan record high C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_max_temp_jan'})['value'])
            res += '| Feb record high C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_max_temp_feb'})['value'])
            res += '| Mar record high C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_max_temp_mar'})['value'])
            res += '| Apr record high C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_max_temp_apr'})['value'])
            res += '| May record high C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_max_temp_may'})['value'])
            res += '| Jun record high C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_max_temp_jun'})['value'])
            res += '| Jul record high C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_max_temp_jul'})['value'])
            res += '| Aug record high C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_max_temp_aug'})['value'])
            res += '| Sep record high C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_max_temp_sep'})['value'])
            res += '| Oct record high C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_max_temp_oct'})['value'])
            res += '| Nov record high C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_max_temp_nov'})['value'])
            res += '| Dec record high C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_max_temp_dec'})['value'])
            res += '| Jan record low C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_min_temp_jan'})['value'])
            res += '| Feb record low C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_min_temp_feb'})['value'])
            res += '| Mar record low C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_min_temp_mar'})['value'])
            res += '| Apr record low C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_min_temp_apr'})['value'])
            res += '| May record low C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_min_temp_may'})['value'])
            res += '| Jun record low C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_min_temp_jun'})['value'])
            res += '| Jul record low C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_min_temp_jul'})['value'])
            res += '| Aug record low C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_min_temp_aug'})['value'])
            res += '| Sep record low C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_min_temp_sep'})['value'])
            res += '| Oct record low C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_min_temp_oct'})['value'])
            res += '| Nov record low C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_min_temp_nov'})['value'])
            res += '| Dec record low C = {}\n'.format(self.res_soup.find('element', {'name': 'extr_min_temp_dec'})['value'])
        except:
            pass

        res += '| Jan high C = {}\n'.format(self.res_soup.find('element', {'name': 'max_temp_dly_jan'})['value'])
        res += '| Feb high C = {}\n'.format(self.res_soup.find('element', {'name': 'max_temp_dly_feb'})['value'])
        res += '| Mar high C = {}\n'.format(self.res_soup.find('element', {'name': 'max_temp_dly_mar'})['value'])
        res += '| Apr high C = {}\n'.format(self.res_soup.find('element', {'name': 'max_temp_dly_apr'})['value'])
        res += '| May high C = {}\n'.format(self.res_soup.find('element', {'name': 'max_temp_dly_may'})['value'])
        res += '| Jun high C = {}\n'.format(self.res_soup.find('element', {'name': 'max_temp_dly_jun'})['value'])
        res += '| Jul high C = {}\n'.format(self.res_soup.find('element', {'name': 'max_temp_dly_jul'})['value'])
        res += '| Aug high C = {}\n'.format(self.res_soup.find('element', {'name': 'max_temp_dly_aug'})['value'])
        res += '| Sep high C = {}\n'.format(self.res_soup.find('element', {'name': 'max_temp_dly_sep'})['value'])
        res += '| Oct high C = {}\n'.format(self.res_soup.find('element', {'name': 'max_temp_dly_oct'})['value'])
        res += '| Nov high C = {}\n'.format(self.res_soup.find('element', {'name': 'max_temp_dly_nov'})['value'])
        res += '| year high C = {}\n'.format(self.res_soup.find('element', {'name': 'max_temp_dly_yr'})['value'])
        res += '| Dec high C = {}\n'.format(self.res_soup.find('element', {'name': 'max_temp_dly_dec'})['value'])
        res += '| Jan low C = {}\n'.format(self.res_soup.find('element', {'name': 'min_temp_dly_jan'})['value'])
        res += '| Feb low C = {}\n'.format(self.res_soup.find('element', {'name': 'min_temp_dly_feb'})['value'])
        res += '| Mar low C = {}\n'.format(self.res_soup.find('element', {'name': 'min_temp_dly_mar'})['value'])
        res += '| Apr low C = {}\n'.format(self.res_soup.find('element', {'name': 'min_temp_dly_apr'})['value'])
        res += '| May low C = {}\n'.format(self.res_soup.find('element', {'name': 'min_temp_dly_may'})['value'])
        res += '| Jun low C = {}\n'.format(self.res_soup.find('element', {'name': 'min_temp_dly_jun'})['value'])
        res += '| Jul low C = {}\n'.format(self.res_soup.find('element', {'name': 'min_temp_dly_jul'})['value'])
        res += '| Aug low C = {}\n'.format(self.res_soup.find('element', {'name': 'min_temp_dly_aug'})['value'])
        res += '| Sep low C = {}\n'.format(self.res_soup.find('element', {'name': 'min_temp_dly_sep'})['value'])
        res += '| Oct low C = {}\n'.format(self.res_soup.find('element', {'name': 'min_temp_dly_oct'})['value'])
        res += '| Nov low C = {}\n'.format(self.res_soup.find('element', {'name': 'min_temp_dly_nov'})['value'])
        res += '| Dec low C = {}\n'.format(self.res_soup.find('element', {'name': 'min_temp_dly_dec'})['value'])
        res += '| year low C = {}\n'.format(self.res_soup.find('element', {'name': 'min_temp_dly_yr'})['value'])
        res += '| Jan mean C = {}\n'.format(self.res_soup.find('element', {'name': 'avg_temp_dly_jan'})['value'])
        res += '| Feb mean C = {}\n'.format(self.res_soup.find('element', {'name': 'avg_temp_dly_feb'})['value'])
        res += '| Mar mean C = {}\n'.format(self.res_soup.find('element', {'name': 'avg_temp_dly_mar'})['value'])
        res += '| Apr mean C = {}\n'.format(self.res_soup.find('element', {'name': 'avg_temp_dly_apr'})['value'])
        res += '| May mean C = {}\n'.format(self.res_soup.find('element', {'name': 'avg_temp_dly_may'})['value'])
        res += '| Jun mean C = {}\n'.format(self.res_soup.find('element', {'name': 'avg_temp_dly_jun'})['value'])
        res += '| Jul mean C = {}\n'.format(self.res_soup.find('element', {'name': 'avg_temp_dly_jul'})['value'])
        res += '| Aug mean C = {}\n'.format(self.res_soup.find('element', {'name': 'avg_temp_dly_aug'})['value'])
        res += '| Sep mean C = {}\n'.format(self.res_soup.find('element', {'name': 'avg_temp_dly_sep'})['value'])
        res += '| Oct mean C = {}\n'.format(self.res_soup.find('element', {'name': 'avg_temp_dly_oct'})['value'])
        res += '| Nov mean C = {}\n'.format(self.res_soup.find('element', {'name': 'avg_temp_dly_nov'})['value'])
        res += '| Dec mean C = {}\n'.format(self.res_soup.find('element', {'name': 'avg_temp_dly_dec'})['value'])
        res += '| year mean C = {}\n'.format(self.res_soup.find('element', {'name': 'avg_temp_dly_yr'})['value'])
        res += '| Jan rain mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_rnfl_jan'})['value'])
        res += '| Feb rain mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_rnfl_feb'})['value'])
        res += '| Mar rain mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_rnfl_mar'})['value'])
        res += '| Apr rain mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_rnfl_apr'})['value'])
        res += '| May rain mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_rnfl_may'})['value'])
        res += '| Jun rain mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_rnfl_jun'})['value'])
        res += '| Jul rain mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_rnfl_jul'})['value'])
        res += '| Aug rain mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_rnfl_aug'})['value'])
        res += '| Sep rain mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_rnfl_sep'})['value'])
        res += '| Oct rain mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_rnfl_oct'})['value'])
        res += '| Nov rain mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_rnfl_nov'})['value'])
        res += '| Dec rain mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_rnfl_dec'})['value'])
        res += '| year rain mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_rnfl_yr'})['value'])
        res += '| Jan snow cm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_snwfl_jan'})['value'])
        res += '| Feb snow cm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_snwfl_feb'})['value'])
        res += '| Mar snow cm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_snwfl_mar'})['value'])
        res += '| Apr snow cm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_snwfl_apr'})['value'])
        res += '| May snow cm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_snwfl_may'})['value'])
        res += '| Jun snow cm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_snwfl_jun'})['value'])
        res += '| Jul snow cm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_snwfl_jul'})['value'])
        res += '| Aug snow cm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_snwfl_aug'})['value'])
        res += '| Sep snow cm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_snwfl_sep'})['value'])
        res += '| Oct snow cm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_snwfl_oct'})['value'])
        res += '| Nov snow cm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_snwfl_nov'})['value'])
        res += '| Dec snow cm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_snwfl_dec'})['value'])
        res += '| year snow cm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_snwfl_yr'})['value'])
        res += '| Jan precipitation mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_pcpn_jan'})['value'])
        res += '| Feb precipitation mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_pcpn_feb'})['value'])
        res += '| Mar precipitation mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_pcpn_mar'})['value'])
        res += '| Apr precipitation mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_pcpn_apr'})['value'])
        res += '| May precipitation mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_pcpn_may'})['value'])
        res += '| Jun precipitation mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_pcpn_jun'})['value'])
        res += '| Jul precipitation mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_pcpn_jul'})['value'])
        res += '| Aug precipitation mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_pcpn_aug'})['value'])
        res += '| Sep precipitation mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_pcpn_sep'})['value'])
        res += '| Oct precipitation mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_pcpn_oct'})['value'])
        res += '| Nov precipitation mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_pcpn_nov'})['value'])
        res += '| Dec precipitation mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_pcpn_dec'})['value'])
        res += '| year precipitation mm = {}\n'.format(self.res_soup.find('element', {'name': 'avg_pcpn_yr'})['value'])
        try:
            res += '| Jan sun = {}\n'.format(self.res_soup.find('element', {'name': 'avg_total_br_sun_hrs_jan'})['value'])
            res += '| Feb sun = {}\n'.format(self.res_soup.find('element', {'name': 'avg_total_br_sun_hrs_feb'})['value'])
            res += '| Mar sun = {}\n'.format(self.res_soup.find('element', {'name': 'avg_total_br_sun_hrs_mar'})['value'])
            res += '| Apr sun = {}\n'.format(self.res_soup.find('element', {'name': 'avg_total_br_sun_hrs_apr'})['value'])
            res += '| May sun = {}\n'.format(self.res_soup.find('element', {'name': 'avg_total_br_sun_hrs_may'})['value'])
            res += '| Jun sun = {}\n'.format(self.res_soup.find('element', {'name': 'avg_total_br_sun_hrs_jun'})['value'])
            res += '| Jul sun = {}\n'.format(self.res_soup.find('element', {'name': 'avg_total_br_sun_hrs_jul'})['value'])
            res += '| Aug sun = {}\n'.format(self.res_soup.find('element', {'name': 'avg_total_br_sun_hrs_aug'})['value'])
            res += '| Sep sun = {}\n'.format(self.res_soup.find('element', {'name': 'avg_total_br_sun_hrs_sep'})['value'])
            res += '| Oct sun = {}\n'.format(self.res_soup.find('element', {'name': 'avg_total_br_sun_hrs_oct'})['value'])
            res += '| Nov sun = {}\n'.format(self.res_soup.find('element', {'name': 'avg_total_br_sun_hrs_nov'})['value'])
            res += '| Dec sun = {}\n'.format(self.res_soup.find('element', {'name': 'avg_total_br_sun_hrs_dec'})['value'])
            res += '| year sun = {}\n'.format(self.res_soup.find('element', {'name': 'avg_total_br_sun_hrs_yr'})['value'])
        except:
            pass

        res += '| source = [[加拿大环境与气候变化部]]<ref>{{'
        res += 'cite web|title=Canadian Climate Normals 1981-2010 Station Data - {}|url=https://climate.weather.gc.ca{}|work=[[加拿大环境与气候变化部]]|accessdate={}'.format(self.location, self.link, datetime.datetime.now().strftime('%Y-%m-%d'))
        res += '}}</ref>\n}}'

        with open('{}.txt'.format(city_en), 'w') as f:
            f.write(res)
