from dataclasses import dataclass
import datetime
import random
import time
import pytz
import uuid
from fake_useragent import UserAgent
from faker import Faker
from faker.providers.internet import Provider
from typing import Union

fake = Faker()
UA = UserAgent()


class UseCounter:
    def __init__(self, obj, count_min, count_max) -> None:
        self.count = random.randint(count_min, count_max)
        self.obj = obj

    def __call__(self) -> Union[bool, any]:
        if self.count == 0:
            return False
        self.count -= 1
        return self.obj


class RandomURL:
    def __init__(self, pool: int = 20, mincount=5, maxcount=50) -> None:
        self.domains: list[UseCounter] = [
            UseCounter(self.mk_domain(), mincount, maxcount) for i in range(pool)
        ]
        self.pool = pool
        self.maxcount = maxcount
        self.mincount = mincount

    def mk_domain(self):
        url = fake.url()
        return url

    def __call__(self) -> str:
        i = random.randint(0, self.pool-1)
        domain = self.domains[i]()
        if domain == False:
            self.domains[i] = UseCounter(
                self.mk_domain(), self.mincount, self.maxcount)
            domain = self.domains[i]()
        url = domain + fake.uri_path()
        return url


class RandomUser:
    def __init__(self) -> None:
        self.e = self.uuid()
        self.f = UA.random
        self.locale = "ja"
        self.platform = "Win32"
        self.ua = UA.random

    def uuid(self):
        random_uuid = uuid.uuid4()
        uuid_string = str(random_uuid)
        return uuid_string

    def timestamp(self):
        random_days = random.randint(1, 20)
        random_datetime = datetime.datetime.now() - datetime.timedelta(days=random_days)
        random_hours = random.randint(1, 23)
        random_datetime += datetime.timedelta(hours=random_hours)
        japan_timezone = pytz.timezone('Asia/Tokyo')
        japan_datetime = japan_timezone.localize(random_datetime)
        random_datetime_string = japan_datetime.strftime(
            "%a %b %d %Y %H:%M:%S")
        return f"{random_datetime_string} GMT+0900 (日本標準時)"

    def __call__(self, url) -> dict:
        return {
            "timestamp": self.timestamp(),
            "e": self.e,
            "f": self.ua,
            "b": url,
            "locale": self.locale,
            "platform": self.platform
        }

    @property
    def header(self) -> dict:
        return {
            "User-Agent": self.ua,
            "Sec-Ch-Ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "Windows",
            "Sec-Fetch-Dest": "iframe",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            'Content-Type': 'application/json',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ja,en-US;q=0.9,en;q=0.8"
        }


@dataclass
class data:
    headers: dict
    data: dict


class RandomData:
    def __init__(self, userpool=20, urlpool=20, minuser=5, maxuser=50, minurl=5, maxurl=50) -> None:
        self.userpool = userpool
        self.minuser = minuser
        self.maxuser = maxuser
        self.url = RandomURL(urlpool, minurl, maxurl)
        self.users: list[RandomUser] = [
            UseCounter(RandomUser(), minuser, maxuser) for i in range(userpool)
        ]

    def __call__(self) -> data:
        i = random.randint(0, self.userpool-1)
        user: RandomUser = self.users[i]()
        if user == False:
            self.users[i] = UseCounter(
                RandomUser(), self.minuser, self.maxuser)
            user = self.users[i]()
        return data(
            headers=user.header,
            data=user(self.url())
        )
