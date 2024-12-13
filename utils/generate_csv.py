import csv

from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

from utils.file_utils import get_media_file_path


def export_to_csv(data):
    try:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=sample.csv"
        response.write("\ufeff".encode())
        writer = csv.writer(response)
        for index, value in enumerate(data["headers"]):
            row_data = [str(i) for i in data["headers"]]
        writer.writerow(row_data)
        counter = 0
        for row_index, data_row_val in enumerate(data["data"]):
            row_data = [str(getattr(data_row_val, i)) for i in data["actual_heads"]]
            counter += 1
            row_data.insert(0, counter)
            writer.writerow(row_data)
        return response
    except Exception as e:
        raise e
