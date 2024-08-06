import json
import time

import op_json
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPalette, QColor, QIcon


class RequestThread(QThread):
    result_signal = pyqtSignal(str)

    def __init__(self, url, header, timeout):
        super(RequestThread, self).__init__()
        self.url = url
        self.header = header
        self.timeout = timeout

    def run(self):
        try:
            response = requests.get(self.url, headers=self.header, timeout=self.timeout)
            self.result_signal.emit(response.text)
        except requests.exceptions.RequestException as e:
            self.result_signal.emit(f"Error: {str(e)}")
            return None


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        op_json.test_dir()
        # self.setStyleSheet("border: 2px solid blue;")  # 2px 宽的蓝色边框
        # self.setStyleSheet("border: 2px solid green; border-radius: 10px;")  # 2 像素宽的绿色边框，10 像素的圆角
        self.setWindowTitle("CountTime")
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(15, 20, 35))  # 设置为红色，您可以更改颜色值
        self.setPalette(palette)
        self.setWindowIcon(QIcon("./pic/clock.svg"))

        # 线程状态位，只允许一个线程运行。
        self.running = False

        # 新增列表项
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("background-color: rgba(0, 0, 0, 0); font-family: '宋体'; font-size: 16px; color:white;")

        # 添加一些项目到列表
        items = op_json.get_list()
        items.remove("bv_list")
        for item in items:
            self.list_widget.addItem(item)
        # 连接信号和槽
        self.list_widget.itemClicked.connect(self.print_data)
        self.list_widget.setFixedWidth(130)

        # 新增功能按钮
        self.Download_Button = QPushButton("下载")
        self.Download_Button.setStyleSheet("background-color: rgba(94, 97, 109); font-family: '宋体'; font-size: 16px;color:white;")
        self.Download_Button.clicked.connect(self.start_request)
        self.Parse_Button = QPushButton("计算")
        self.Parse_Button.setStyleSheet("background-color: rgba(94, 97, 109); font-family: '宋体'; font-size: 16px;color:white;")
        self.Parse_Button.clicked.connect(self.Parse_action)
        self.Clear_Button = QPushButton("清空")
        self.Clear_Button.setStyleSheet("background-color: rgba(94, 97, 109); font-family: '宋体'; font-size: 16px;color:white;")
        self.Clear_Button.clicked.connect(self.clear_action)
        self.Delete_Button = QPushButton("删除")
        self.Delete_Button.setStyleSheet("background-color: rgba(94, 97, 109); font-family: '宋体'; font-size: 16px;color:white;")
        self.Delete_Button.clicked.connect(self.dele_action)


        # 设置标签和输入框
        label1 = QLabel("BV:")
        label1.setStyleSheet("font-family: '宋体'; font-size: 16px; color:white;")
        label2 = QLabel("Start:")
        label2.setStyleSheet("font-family: '宋体'; font-size: 16px; color:white;")
        label3 = QLabel("End:")
        label3.setStyleSheet("font-family: '宋体'; font-size: 16px; color:white;")
        self.Bv_edit = QLineEdit()
        self.Start_edit = QLineEdit()
        self.End_edit = QLineEdit()

        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        grid_layout.addWidget(label1, 0, 0)
        grid_layout.addWidget(label2, 1, 0)
        grid_layout.addWidget(label3, 2, 0)
        grid_layout.addWidget(self.Bv_edit, 0, 1)
        grid_layout.addWidget(self.Start_edit, 1, 1)
        grid_layout.addWidget(self.End_edit, 2, 1)
        grid_layout.addWidget(self.Download_Button, 0, 2)
        grid_layout.addWidget(self.Parse_Button, 1, 2)
        grid_layout.addWidget(self.Clear_Button, 2, 2)

        # 新增label
        self.Result_title = QLabel("结果：")
        self.Result_title.setContentsMargins(0, 0, 0, 0)
        self.Result_title.setStyleSheet("font-family: '宋体'; font-size: 16px; color:white;")
        self.Range_title = QLabel("范围：")
        self.Range_title.setContentsMargins(0, 0, 0, 0)
        self.Range_title.setStyleSheet("font-family: '宋体'; font-size: 16px; color:white;")
        self.Tip_title = QLabel("提示：")
        self.Tip_title.setContentsMargins(0, 0, 0, 0)
        self.Tip_title.setStyleSheet("font-family: '宋体'; font-size: 16px; color:white;")
        self.Range_label = QLabel()
        self.Range_label.setContentsMargins(0, 0, 140, 0)
        self.Range_label.setStyleSheet("font-family: '宋体'; font-size: 16px; color:white;")
        self.Result_label = QLabel()
        self.Result_label.setContentsMargins(0, 0, 115, 0)
        self.Result_label.setStyleSheet("font-family: '宋体'; font-size: 16px; color:white;")
        self.Tip_label = QLabel()
        # self.Tip_label.setAlignment(Qt.AlignCenter)
        self.Tip_label.setContentsMargins(0, 0, 20, 0)
        self.Tip_label.setStyleSheet("font-family: '宋体'; font-size: 16px; color:white;")


        # 水平布局
        H1_layout = QHBoxLayout()
        H1_layout.addWidget(self.Range_title)
        H1_layout.addWidget(self.Range_label)
        H2_layout = QHBoxLayout()
        H2_layout.addWidget(self.Result_title)
        H2_layout.addWidget(self.Result_label)
        H3_layout = QHBoxLayout()
        H3_layout.addWidget(self.Tip_title)
        H3_layout.addWidget(self.Tip_label)

        # 垂直布局，设置结果展示label
        v_layout = QVBoxLayout()
        v_layout.addLayout(grid_layout)
        v_layout.addLayout(H1_layout)
        v_layout.addLayout(H2_layout)
        v_layout.addLayout(H3_layout)
        v_layout.addSpacing(5)

        # 垂直布局，列表和删除键
        v2_layout = QVBoxLayout()
        v2_layout.addWidget(self.list_widget)
        v2_layout.addWidget(self.Delete_Button)

        # 创建一个水平布局，并将列表添加到左侧
        h_layout = QHBoxLayout()
        h_layout.addLayout(v2_layout)
        h_layout.addLayout(v_layout)

        # 创建一个中心部件，并设置布局
        central_widget = QWidget()
        central_widget.setLayout(h_layout)
        # central_widget.setLayout(Layout)
        self.setCentralWidget(central_widget)
        self.setFixedSize(440, 205)

    def print_data(self, item):
        name_list = op_json.get_list()
        name_list.remove("bv_list")
        if item.text() in name_list:
            # print(op_json.open_json(item.text())["title"])
            data = op_json.open_json(item.text())
            self.Bv_edit.setText(data["bv"])
            self.Range_label.setText(" 1~~{}".format(str(len(data["duration_list"]))))
            self.Result_label.clear()
            self.Tip_label.clear()
        else:
            pass

    def Parse_action(self):
        bv = self.Bv_edit.text()
        start = self.Start_edit.text()
        end = self.End_edit.text()
        bv_list = op_json.get_bv_list()

        if bv == "":
            self.Tip_label.setText("bv不能为空！       ")
            return
        elif bv not in bv_list.keys():
            self.Tip_label.setText("bv不在库，先下载！    ")
            return None
        elif start == "" or not start.isdigit() or int(start) <= 0:
            self.Tip_label.setText("start>0|整数|不为空|       ")
            return
        elif (end == "" or not end.isdigit()) or int(end) < int(start) or int(end) <= 0:
            self.Tip_label.setText("end>star|整数|end>0|不为空|  ")
            return
        else:
            data = op_json.open_json(bv_list[bv])
            if int(end) > len(data["duration_list"]):
                self.Tip_label.setText("End超出索引范围！   ")
                return None
            elif int(start) > len(data["duration_list"]):
                self.Tip_label.setText("Start超出索引范围！   ")
                return None
            # print("在库")

        self.count_time(data, int(start), int(end))

    def count_time(self, data, start, end):
        time = 0
        for i in range(start, end+1):
            time += data["duration_list"][i-1]

        hour = time // 3600
        minute = (time % 3600) // 60
        self.Result_label.setText("总计{}时{}分".format(hour, minute))
        self.Tip_label.clear()

    def clear_action(self):
        self.Bv_edit.clear()
        self.Start_edit.clear()
        self.End_edit.clear()
        self.Range_label.clear()
        self.Result_label.clear()
        self.Tip_label.setText("已清空！       ")

    def dele_action(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            row = self.list_widget.row(current_item)
            self.list_widget.takeItem(row)
            op_json.delete_bv(op_json.open_json(current_item.text())["bv"])
            op_json.delete_json(current_item.text())
            self.Tip_label.setText("删除成功！      ")

    def download_action(self, response):
        self.running = False
        if response[:5] == "Error":
            self.Tip_label.setText("下载失败，请检查网络！")
            return None
        row_data = json.loads(response)
        if row_data["code"] != 0:
            self.Tip_label.setText("请检查bv是否正确！  ")
            return None
        self.Tip_label.setText("下载完成！")
        data = op_json.parse_json(row_data)

        op_json.save_json(data["title"], data)
        op_json.save_bv(data["bv"], data["title"])
        self.list_widget.addItem(data["title"])

    def start_request(self):

        url = "https://api.bilibili.com/x/web-interface/view?bvid={}"
        header = {
            "User-Agent": \
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 "
                "Safari/537.36 Edg/127.0.0.0"
        }

        bv = self.Bv_edit.text()
        bv_list = op_json.get_bv_list().keys()

        if bv == "":
            self.Tip_label.setText("请填写bv!")
            return None
        elif bv not in bv_list and not self.running:
            self.Tip_label.setText("开始下载！")
            self.running = True
            self.thread = RequestThread(url.format(bv), header, 30)
            self.thread.result_signal.connect(self.download_action)
            self.thread.start()
        elif self.running == True:
            self.Tip_label.setText("请等待下载。。。   ")
        else:
            self.Tip_label.setText("在库，不用下载！      ")


if __name__ == "__main__":

    time.sleep(2)
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
