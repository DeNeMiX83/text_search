from window.template.main import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFileDialog, QInputDialog
import os
import re
from services import levenstein

colors = {0: 'violet', 1: 'red', 2: 'green', 3: 'blue', 4: 'orange', 5: 'magenta', 6: 'darkCyan', 7: 'darkMagenta', 8: 'gray', 9: 'darkRed'}

class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.initUI()
        self.show()

    def initUI(self):
        ...
        # # Кнопка добавления заметки
        self.btn_import.clicked.connect(self.import_file)
        self.btn_search.clicked.connect(self.search)
        # # Кнопка удаления всех заметок
        # self.DeleteAllBt.clicked.connect(self.delete_all)
        # # Кнопка удаления выбранного уведомления
        # self.DeleteBt.clicked.connect(self.clear_event)
        # # Кнопка создания таблицы
        # self.bnt_create_week_table.clicked.connect(self.create_table)
        # # Кнопка востановления графика недели из таблицы
        # self.btn_load_week_table.clicked.connect(self.load_table)
        # # Кнопка создающая окно о комбинация клавишь
        # self.btn_combo_info.clicked.connect(self.combo_info)
        # # Распарсим базу данных note и впишем все добавленные до этого заметки

    def import_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Выберите файл', '', '(*.txt)')[0]
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                text = f.read()
                self.text_input.setPlainText(text)
        print('import')


    def search(self):
        value, ok = QInputDialog.getText(self, 'Поиск', 'Введите текст для поиска:')
        if not ok:
            return
        self.show_top(value)

    def show_top(self, word_search):
        text = self.text_input.toPlainText()
        words = re.findall(r'\w+', text)
        top = dict()
        for word in words:
            word = word.lower()
            if word not in top:
                top[word] = [word, 1, levenstein(word_search, word)]
                continue
            value = top[word]
            value[1] += 1
            top[word] = value
        
        top = sorted(top.values(), key=lambda x: x[-1])[:10][::-1]
        top_text = ''
        for i in range(len(top)):
            top_text += f'<font color={colors[i]}>{top[i][0]}</font> - {top[i][1]}<br>'
        self.text_top.setPlainText('')
        self.text_top.appendHtml(top_text)

        for n, word in enumerate(top):
            text = re.sub(r'\b'+word[0]+r'\b', f'<font color={colors[n]}>{word[0]}</font>', text)
            text = re.sub(r'\b'+word[0].capitalize()+r'\b', f'<font color={colors[n]}>{word[0].capitalize()}</font>', text)
        self.text_input.setPlainText('')
        self.text_input.appendHtml(text)
        # self.text_top.setPlainText(result)