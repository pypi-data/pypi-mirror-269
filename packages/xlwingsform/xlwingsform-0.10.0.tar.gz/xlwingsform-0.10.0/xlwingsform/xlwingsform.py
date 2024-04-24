import xlwings as xw


def test():
    print("テスト")

class Worksheet:
    def __init__(self, ws) -> None:
        self.ws = ws

    def get_values(self, range_name):
        return self.ws.range(range_name).value

    def set_values(self, range_name, values):
        print(range_name, values)
        self.ws.range(range_name).value = values


class Workbook:
    def __init__(self, path, dst_sheets, template_sheet_name) -> None:
        self.template_sheet_name = template_sheet_name
        self.dst_sheets = dst_sheets
        self.wb = xw.Book(path)

    def save(self, path):
        self.wb.save(path)

    def get_sheet_or_create(self, item_num_per_sheet):
        if self.dst_sheets[item_num_per_sheet] not in self.wb.sheet_names:
            print("シートがありません。作成します。")
            self.wb.sheets[self.template_sheet_name].copy(name=self.dst_sheets[item_num_per_sheet])

        return Worksheet(self.wb.sheets[self.dst_sheets[item_num_per_sheet]])
