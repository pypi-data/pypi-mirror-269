from bs4 import BeautifulSoup

from . import *
from .Logga import *
from .funcs import *


class PeneParser:
    def __init__(self, driver):
        self.driver = driver
        #
    def parse_mods_from_html(self, htmldata):
        def parse_html(htmldata):
            log(f'PeneParser.parse_mods_from_html.parse_html:{ln()}: parsing html')
            soup = BeautifulSoup(htmldata, 'html.parser')
            all_rows = soup.find_all('tr')

            us_raw = []
            for row in all_rows:
                td = row.find_all('td')
                for d in td:

                    if 'class' in d.attrs.keys():
                        if 'ProfilListnshown' in d.attrs['class']:
                            us_raw.append(row)
            if len(us_raw) > 0:
                log(f'PeneParser.parse_mods_from_html.parse_html:{ln()}: html parsed')
                return us_raw[0]
            ''
        def extract_users(raw_html):
            log(f'PeneParser.parse_mods_from_html.extract_users:{ln()}: extracting users')
            all_divs = raw_html.find_all('div')
            raw_us = []
            user_content = []
            for div in all_divs:
                raw = div.text.replace('\n', '')
                raw = raw.replace(' ', '')
                user_content.append(raw)
                username = raw[0].split(',')[0]
                dlog(raw)
                dlog(username)
                #wait(99999)
                if raw[:8] == 'Angelegt':
                    raw_us.append(user_content)
                    user_content = []

            log(f'PeneParser.parse_mods_from_html.extract_users:{ln()}: users extracted')
            return raw_us
            ''
        def clean_users(raw_users):
            def clean_user(user):
                log(f'PeneParser.parse_mods_from_html.clean_users.clean_user:{ln()}: cleaning user')
                cl_user = {}

                indicator = len(user)
                

                log(f'PeneParser.parse_mods_from_html.clean_users.clean_user:{ln()}: user cleaned')
                return cl_user
                ''
            ''''''
            log(f'PeneParser.parse_mods_from_html.clean_users:{ln()}: cleaning users')
            cleaned_users = []
            for user in raw_users:
                cleaned_user = clean_user(user)
                if cleaned_user:
                    cleaned_users.append(cleaned_user)
            log(f'PeneParser.parse_mods_from_html.clean_users:{ln()}: users cleaned')
            return cleaned_users
            ''
        ''''''
        raw_html = parse_html(htmldata)

        if raw_html:
            raw_users = extract_users(raw_html)

            if raw_users:
                users = clean_users(raw_users)

                if users:
                    return users
    
    def parse_users_from_html(self, htmldata):
        raw_html = self.parse_html(htmldata)

        if raw_html:
            raw_users = self.extract_users(raw_html)

            if raw_users:
                users = self.clean_users(raw_users)

                if users:
                    return users
    ''
    def parse_html(self, htmldata):
        log(f'PeneParser.parse_html:{ln()}: parsing html')
        soup = BeautifulSoup(htmldata, 'html.parser')
        all_rows = soup.find_all('tr')

        us_raw = []
        for row in all_rows:
            td = row.find_all('td')
            for d in td:

                if 'class' in d.attrs.keys():
                    if 'ProfilListshown' in d.attrs['class']:
                        us_raw.append(row)
        if len(us_raw) > 0:
            log(f'PeneParser.parse_html:{ln()}: html parsed')
            return us_raw[0]
        ''
    def extract_users(self, raw_html):
        log(f'PeneParser.extract_users:{ln()}: extracting users')
        all_divs = raw_html.find_all('div')
        raw_us = []
        user_content = []
        for div in all_divs:
            raw = div.text.replace('\n', '')
            raw = raw.replace(' ', '')
            user_content.append(raw)
            if raw[:8] == 'Angelegt':
                raw_us.append(user_content)
                user_content = []

        log(f'PeneParser.extract_users:{ln()}: users extracted')
        return raw_us
        ''
    def clean_users(self, raw_users):
        def clean_user(user):
            log(f'PeneParser.clean_users.clean_user:{ln()}: cleaning user')
            cl_user = {}

            indicator = len(user)
            if indicator == 22:
                cl_user['member_since'] = user[21].split(':')[-1][1:]
            elif indicator == 21:
                cl_user['member_since'] = user[20].split(':')[-1][1:]
            else:
                return
            """=============================================================="""
            cl_user['name'] = user[1].split(',')[0]
            cl_user['points_bought'] = user[1].split(',')[1].split('/')[0]
            cl_user['customer_type'] = user[1].split(',')[1].split('/')[1]
            cl_user['points_now'] = user[1].split(',')[1].split('/')[2]
            cl_user['id'] = user[4][:-1]
            cl_user['gender'] = user[6].split(',')[0][3:]
            cl_user['zip'] = user[8].split(',')[1].split('(')[1].split(')')[0]
            """=============================================================="""
            cl_user['height'] = user[10].split(',')[1][:-1]

            log(f'PeneParser.clean_users.clean_user:{ln()}: user cleaned')
            return cl_user
            ''
        ''''''
        log(f'PeneParser.clean_users:{ln()}: cleaning users')
        cleaned_users = []
        for user in raw_users:
            try:
                cleaned_user = clean_user(user)
                if cleaned_user:
                    cleaned_users.append(cleaned_user)
            except Exception as e:
                continue
        log(f'PeneParser.clean_users:{ln()}: users cleaned')
        return cleaned_users
        ''

    
class PeneParserOld:
    def parse_users_from_html(self, raw_html):
        users_html = self.step1(raw_html)
        users_raw = self.step2(users_html)
        
        users_cleaned = []
        for user in users_raw:
            user_cleaned = self.step3(user)
            if user_cleaned:
                users_cleaned.append(user_cleaned)
        return users_cleaned
        ''
    ''''''
    def step1(self, htmldata) -> list:
        """filter user elements from raw html
            return: list user_data: html elements
        """
        soup = BeautifulSoup(htmldata, 'html.parser')
        all_rows = soup.find_all('tr')
        us_raw = []
        for row in all_rows:
            td = row.find_all('td')
            for d in td:

                if 'class' in d.attrs.keys():
                    if 'ProfilListshown' in d.attrs['class']:
                        us_raw.append(row)
        us = us_raw[0]
        return us
        ''
    ''
    def step2(self, us_ht) -> list:
        """filter out user data from user_html
            return: list user_data: raw user_data
        """
        all_divs = us_ht.find_all('div')
        us_raw = []
        user_content = []
        for div in all_divs:
            raw = div.text.replace('\n', '')
            raw = raw.replace(' ', '')
            user_content.append(raw)
            if raw[:8] == 'Angelegt':
                us_raw.append(user_content)
                user_content = []

        return us_raw
        ''
    ''
    def step3(self, us) -> dict:
        """clean single user
            return: dict single user_data: clean user_data_dict
        """
        cl_user = {}

        indicator = len(us)
        if indicator == 22:
            cl_user['member_since'] = us[21].split(':')[-1][1:]
        elif indicator == 21:
            cl_user['member_since'] = us[20].split(':')[-1][1:]
        else:
            print_log(f"ERROR: cleaning user_data_raw: unknown legth: {len(us)}", level='ERROR')
            return
        """=============================================================="""
        cl_user['name'] = us[1].split(',')[0]
        cl_user['points_bought'] = us[1].split(',')[1].split('/')[0]
        cl_user['customer_type'] = us[1].split(',')[1].split('/')[1]
        cl_user['points_now'] = us[1].split(',')[1].split('/')[2]
        """=============================================================="""
        cl_user['job'] = us[3][:-1]
        cl_user['id'] = us[4][:-1]
        cl_user['Bin'] = us[6].split(',')[0][3:]
        cl_user['Suche'] = us[6].split(',')[1][5:]
        cl_user['partner'] = us[7][2:]
        """=============================================================="""
        cl_user['country'] = us[8].split(',')[0]
        cl_user['region'] = us[8].split(',')[1].split('(')[0]
        cl_user['zip'] = us[8].split(',')[1].split('(')[1].split(')')[0]
        """=============================================================="""
        cl_user['status'] = us[10].split(',')[0]
        cl_user['height'] = us[10].split(',')[1][:-1]
        cl_user['member_since'] = us[20].split(':')[-1][1:]
        cl_user['contacted'] = us[13]
        cl_user['online'] = us[18]

        return cl_user
        ''
    ''
''''''