to_nepali_hash = {
    "0": "०",
    "9": "९",
    "8": "८",
    "7": "७",
    "6": "६",
    "5": "५",
    "4": "४",
    "3": "३",
    "2": "२",
    "1": "१",
}
to_english_hash = {
    "०": "0",
    "९": "9",
    "८": "8",
    "७": "7",
    "६": "6",
    "५": "5",
    "४": "4",
    "३": "3",
    "२": "2",
    "१": "1",
}

num_list = ["0", "1", "2", "9", "8", "7", "6", "5", "4", "3"]


def english_nums(num):
    if not num:
        return num
    num = str(num)
    num_arr = [to_english_hash.get(value, value) for value in list(num)]
    return "".join(num_arr)


def nepali_nums(num):
    if not num:
        return num
    num = str(num)
    if all([value not in num for value in num_list]):
        return num
    num_arr = [to_nepali_hash.get(value, value) for value in list(num)]
    return "".join(num_arr)


def to_nepali_string(date):
    date_sp = date.split("-")
    nepali_year = str(date_sp[0])
    nepali_month = str(date_sp[1])
    nepali_day = str(date_sp[2])

    # Define a mapping from Arabic numerals to Nepali digits
    nepali_digits = ["०", "१", "२", "३", "४", "५", "६", "७", "८", "९"]

    # Convert numeric parts to Nepali digits
    nepali_year = "".join([nepali_digits[int(digit)] for digit in nepali_year])
    nepali_month = "".join([nepali_digits[int(digit)] for digit in nepali_month])
    nepali_day = "".join([nepali_digits[int(digit)] for digit in nepali_day])
