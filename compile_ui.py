import os
import subprocess
import logging

logging.basicConfig(level=logging.INFO)

UI_SOURCE_DIR = os.path.join("res", "ui")
PY_OUTPUT_DIR = os.path.join("src", "generated")

def compile_ui_to_py(filenames: list[str]):
    """Компиляция .ui в python код"""
    
    for filename in filenames:
        if filename.endswith(".ui"):
            ui_path = os.path.join(UI_SOURCE_DIR, filename)
            
            py_filename = os.path.splitext(filename)[0] + ".py"
            py_path = os.path.join(PY_OUTPUT_DIR, py_filename)
            
            logging.info(f"Компилируем: {filename} -> generated/{py_filename}")

            try:
                subprocess.run(['pyuic5', ui_path, '-o', py_path], check=True)
            except subprocess.CalledProcessError as e:
                logging.error(f"Ошибка: Не удалось скомпилировать {filename}")
            except FileNotFoundError:
                logging.error(f"ОШИБКА: pyuic5 не найден. Проверьте установку PyQt5")

                              
            logging.info(f"Файл {filename} скомпилирован")

def main(filenames: list[str]=[]):
    """Главная функция"""
    
    if not os.path.exists(UI_SOURCE_DIR):
        logging.error(f"Ошибка: Директория {UI_SOURCE_DIR} не найдена")
        return
    
    os.makedirs(PY_OUTPUT_DIR, exist_ok=True)
    
    logging.info(f"Ищем .ui файлы в '{UI_SOURCE_DIR}'")
    
    # Если список пустой, то компилируются все файлы
    if filenames:
        compile_ui_to_py(filenames)
    else:        
        compile_ui_to_py(os.listdir(UI_SOURCE_DIR))
        
if __name__ == "__main__":
    main(['mainWindow.ui'])
    logging.info("Компиляция завершена")