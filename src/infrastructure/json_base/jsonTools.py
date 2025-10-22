import json

from exceptions.missingDatesError import MissingDatesError

from infrastructure.json_base.jsonBase import JsonBase

# from jsonBase import JsonBase # для тестов

class JsonTools():
    """Инструментарий к json"""

    def __init__(self):
        self.jbase = JsonBase()

        if self.jbase.base["current_account_id"] not in self.jbase.base["accounts"]:
            if len(self.jbase.base["accounts"]) > 0:
                self.set_current_account_id(list(self.jbase.base["accounts"].keys())[0])
            else:
                self.set_current_account_id("")
            self.jbase._save()
        
    def create_account(self, name: str):
        """Создаёт новый учёт"""

        account_id = str(len(self.jbase.base["accounts"]))

        self.jbase.base["accounts"][account_id] = {
                    "name": name,
                    "dates": { }
        }
        self.set_current_account_id(account_id)

    def edit_account_name(self, account_id: str, new_name: str) -> bool:
        """Изменяет имя учётки"""

        if account_id in self.jbase.base["accounts"]:
            self.jbase.base["accounts"][account_id]["name"] = new_name
            return True
        return False
    
    def del_account(self, account_id: str) -> bool:
        """Удаляет учёт"""

        if account_id in self.jbase.base["accounts"]:
            del self.jbase.base["accounts"][account_id]

            if self.jbase.base["current_account_id"] == account_id:
                if len(self.jbase.base["accounts"]) > 0:
                    self.set_current_account_id(list(self.jbase.base["accounts"].keys())[0])
                    return True
                else:
                    self.set_current_account_id("")
                    return True
            return True

        return False

    def set_current_account_id(self, account_id: str) -> bool:
        """Устанавливает id текущей учётки"""

        if account_id in self.jbase.base["accounts"]:
            if self.jbase.base["current_account_id"] != account_id:
                self.jbase.base["current_account_id"] = account_id
                return True
        elif account_id == "":
            self.jbase.base["current_account_id"] = ""
            return False

    def set_info_date(self, account_id: str, date: str, weight: str, weather: str = "") -> bool:
        """Устанавливает вес даты в учётку"""
        
        if account_id in self.jbase.base["accounts"]:
            self.jbase.base["accounts"][account_id]["dates"][date] = {
                "weight": weight,
                "weather": weather
            }
            return True
        return False

    def get_current_account_id(self) -> str:
        """Возвращает id текущей учётки"""

        if self.jbase.base["current_account_id"] in self.jbase.base["accounts"]:
            return self.jbase.base["current_account_id"]
        return ""

    def get_account_name(self, account_id: str) -> str:
        """Возвращает имя учётки по id"""

        if len(self.jbase.base["accounts"]) > 0:
            if account_id in self.jbase.base["accounts"]:
                return self.jbase.base["accounts"][account_id]["name"]
        return "Создайте новый учёт с помощью '+'!"
    
    def get_account(self, account_id: str) -> dict["name": str, "weight": int, "weather": str]:
        """Возвращает данные аккаунта по id"""

        if account_id in self.jbase.base["accounts"]:
            return self.jbase.base["accounts"][account_id]

    def get_accounts(self) -> dict[str: dict]:
        """Возвращает словарь всех учёток"""

        if len(self.jbase.base["accounts"]) > 0:
            return self.jbase.base["accounts"]
        return {}

    def get_weight_date(self, account_id: str, date: str) -> str:
        """Возвращает вес даты в учётке"""

        if account_id in self.jbase.base["accounts"] and date in self.jbase.base["accounts"][account_id]["dates"]:
            return self.jbase.base["accounts"][account_id]["dates"][date]["weight"]
        return "0"

    def get_dates_account_id(self, account_id: str) -> list:
        """Возвращает все даты текущей учётки"""
        try:
            return list(self.jbase.base["accounts"][account_id]["dates"].keys())
        except KeyError:
            raise MissingDatesError("Отсутствуют даты")
    
    def get_weight_account_id(self, account_id: str) -> list:
        """Возвращает все веса текущей учётки"""

        weight_account_id = list()

        for info_date in self.jbase.base["accounts"][account_id]["dates"].values():
            weight_account_id.append(info_date["weight"])

        return weight_account_id

    def sort_date_base(self):
        """Сортирует все даты базы данных"""

        for account_id in self.jbase.base["accounts"].keys():

            sorted_data = dict(sorted(self.jbase.base["accounts"][account_id]["dates"].items()))
            self.jbase.base["accounts"][account_id]["dates"] = sorted_data

    def sync_data(self, data: str):
        """Синхранизация полученных данных с нынешними"""

        data = json.loads(data)

        if data and self.jbase.base["accounts"]:
            for account_id, account_data in data['accounts'].items():
                for date, date_data in account_data["dates"].items():
                    if account_id in self.jbase.base["accounts"]:
                        if not (date in self.jbase.base["accounts"][account_id]["dates"]):
                            self.jbase.base["accounts"][account_id]["dates"][date] = date_data

        self.sort_date_base()

        self.jbase._save()  


# js = JsonTools()

# js.create_account("Admin")
# js.set_weight_date(0, "26.05.2009", "99.99")

# print(js.get_account_name("0"))
# print(js.get_account_name("10009"))

# print(js.edit_name_account("0", "Привет, Мир!!!"))

# print(js.del_account("0"))

# js.jb._save()