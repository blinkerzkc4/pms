"""
-- Created by Bikash Saud
-- Created on 2023-06-27
"""
from datetime import datetime

import nepali_datetime

from utils.nepali_nums import english_nums, nepali_nums, num_list


def ad_to_bs(ad_date=None, lang="np"):
    try:
        if not ad_date:
            ad_date = datetime.now().date()

        np_date = nepali_datetime.date.from_datetime_date(ad_date)
        nepali_date = ""
        if lang == "np":
            for num in str(np_date):
                if num in num_list:
                    num = nepali_nums(num)
                nepali_date += num
        return nepali_date
    except Exception as e:
        print(f"exception: {e}")
        return None


def bs_to_ad(bs_date):
    bs_date = english_nums(bs_date)
    year, month, day = bs_date.split("/")
    try:
        nepali_datetime.date.fromordinal
        ad_date = nepali_datetime.date(
            year=int(year), month=int(month), day=int(day)
        ).to_datetime_date()
        return ad_date
    except Exception as e:
        print(f"exception: {e}")
        return None
