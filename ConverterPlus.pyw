from PyQt5 import QtWidgets, QtCore
import sys, form.ui_converterPlus


class ConverterPlus(QtWidgets.QWidget):
    '''
    Класс описывает конвертер

    легенда:
        ln_round - поле "округливание"(кол-во знаков после запитой)
        гр. Величины:
            ln_vals_inp - исходная(ые) величина(ы)
            ln_vals_out - конвертируемая(ые) величина(ы)
        гр. Числа:
            ln_nums_inp - исходное(ые) число(а)
            ln_nums_out - конвертируемое(ые) число(а)
        кнопки:
            btn_conv - конвертация
            btn_clear - сброс
    '''
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = form.ui_converterPlus.Ui_Form()
        self.ui.setupUi(self)
        self.setting()

    def setting(self):
        self.show()
        self.setWindowTitle('Converte+')
        # сигналы
        self.ui.btn_conv.pressed.connect(self.convert)
        self.ui.btn_clear.pressed.connect(self.clear)
        self.ui.btn_values.pressed.connect(self.display_values)
        self.ui.btn_hotKeys.pressed.connect(self.display_hotKeys)

    def display_hotKeys(self):
        text = '''
        Enter - конвертировать
        Ctrl - сброс
        Esc - закрыть приложение
        F2 - поддерживаемые величины
        F3 - горячие клавиши
        '''
        message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.NoIcon,
                                        "Горячие клавиши",
                                        text)
        message.exec()

    def display_values(self):
        text = '''
        Расстояние: см, м, км

        Время: с, мин, ч

        Так-же поддерживаются производные величины(например: км/ч, м/с)
        '''
        message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.NoIcon,
                                        "Поддерживаемые величины",
                                        text)
        message.exec()

    def convert(self):
        dct = {
                "см": {"см":1, "м":1/100, "км":1/100_000},
                "м": {"см":100, "м":1, "км":1/1000},
                "км": {"см":100_000, "м":1000, "км":1},

                "с": {"с":1, "мин":1/60, "ч":1/3600},
                "мин": {"с":60, "мин":1, "ч":1/60},
                "ч": {"с":3600, "мин":60, "ч":1}
                }
        # получение данных с компонентов
        rnd = self.ui.sbox_round.value()
        numsInp = self.ui.ln_num_inp.text().split()
        valsInp = self.ui.ln_val_inp.text().split()
        valsOut = self.ui.ln_val_out.text().split()
        numsOut = []
        # длины входных и выходных величин
        lenValsInp = len(valsInp)
        lenValsOut = len(valsOut)

        for idxNum in range(len(numsInp)):
            try:
                # индексы входных и выходных величин
                x = (lambda: 0 if lenValsInp == 1 else idxNum)()
                z = (lambda: 0 if lenValsOut == 1 else idxNum)()
                # величина - производная от 2х величин? (пример: м/с, км/ч)
                if '/' in valsInp[x]:
                    multInp = valsInp[x].split('/')
                    multOut = valsOut[z].split('/')
                    k = (dct[multInp[0]][multOut[0]] /
                         dct[multInp[1]][multOut[1]])
                else:
                    k = dct[valsInp[x]][valsOut[z]]
                # конвертация и добавление в список
                number = float(numsInp[idxNum]) * k
                numsOut.append(str(round(number, rnd)))
            except IndexError:
                numsOut.clear()
                numsOut.append("Не правильный ввод!!!")
                break
            except KeyError as err:
                numsOut.clear()
                numsOut.append(f'Неправильная величина: {str(err)}')
                break
        # вывод на экран
        self.ui.ln_num_out.setText('; '.join(numsOut))

    def clear(self):
        self.ui.ln_num_inp.clear()
        self.ui.ln_num_out.clear()
        self.ui.ln_val_inp.clear()
        self.ui.ln_val_out.clear()

    def keyPressEvent(self, event):
        # Enter - конвертировать
        if event.key() == QtCore.Qt.Key_Return:
            self.ui.btn_conv.click()
        # Ctrl - сброс
        elif event.key() == QtCore.Qt.Key_Control:
            self.ui.btn_clear.click()
        # Esc - закрыть приложение
        elif event.key() == QtCore.Qt.Key_Escape:
            self.close()
        # F2 - поддерживаемые величины
        elif event.key() == QtCore.Qt.Key_F2:
            self.ui.btn_values.click()
        # F3 - горячие клавиши
        elif event.key() == QtCore.Qt.Key_F3:
            self.ui.btn_hotKeys.click()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = ConverterPlus()
    sys.exit(app.exec())