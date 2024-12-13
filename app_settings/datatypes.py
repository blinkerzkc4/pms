from typing import TypedDict


class SettingJsonDict(TypedDict):
    value_type: str
    code: str
    name: str
    name_eng: str
    use_in_report: bool
    delete_this: bool
