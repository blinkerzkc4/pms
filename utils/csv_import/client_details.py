import pandas as pd


class ClientDetails:
    cols_to_use = [
        "client_id",
        "code",
        "Address Maping Code",
    ]

    def __init__(self, path):
        self.path = path
        self.data = self.get_client_details()

    def get_client_details_by_address_mapping_code(self, address_mapping_code):
        return self.data[self.data["address_mapping_code"] == address_mapping_code]

    def get_client_details(self):
        data = pd.read_csv(self.path, usecols=self.cols_to_use)
        data.rename(
            columns={"Address Maping Code": "address_mapping_code"}, inplace=True
        )
        data["address_mapping_code"] = data["address_mapping_code"].apply(
            lambda x: str(int(x)) if not pd.isna(x) else ""
        )
        return data

    def test(self):
        print(self.data.head())
        print(self.data.dtypes)
        print(self.get_client_details_by_address_mapping_code(2593))

    @classmethod
    def create(cls):
        return cls("data/users/client_details.csv")


def main():
    client_details = ClientDetails.create()
    client_details.test()


if __name__ == "__main__":
    main()
