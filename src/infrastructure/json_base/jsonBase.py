import json
import os

from exceptions.jsonFormatError import JsonFormatError

PATH = os.path.join("data", "jsonbase.json")

class JsonBase:
    """Класс хранитель json"""
    def __init__(self):
        self.path: str = PATH
        self.base = {
            "accounts": {},
            "current_account_id": ""
        }

        self._updateBase()

    def _updateBase(self):
        """Инициализирует базу"""

        try:
            with open(self.path) as jfile:
                self.base: dict = json.load(jfile)

        except json.decoder.JSONDecodeError:
            raise JsonFormatError("Невалидный формат json")
        
        except FileNotFoundError:
            with open(self.path, "w") as jfile:
                json.dump(self.base, 
                      jfile,
                      ensure_ascii=False, # сохраняет русские буквы
                      indent=4) # отступы в 4 пробела

    def _save(self):
        """Сохраняет json"""

        with open(self.path, "w") as jfile:
            json.dump(self.base, 
                      jfile,
                      ensure_ascii=False, # сохраняет русские буквы
                      indent=4) # отступы в 4 пробела
            
        self._updateBase()
 
    