import requests as rq
import json
import os

dir_path = "./data/"
url = "https://api.bilibili.com/x/web-interface/view?bvid={}"
header = {
    "User-Agent": \
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 "
        "Safari/537.36 Edg/127.0.0.0"
}

temp_data = {'bv': 'BV1iD4y1D7C8', 'title': 'Python-GUI编程-pyqt5最新详细教程', 'duration_list': [576, 613, 376, 1551, 1094, 430, 1308, 324, 1437, 827, 487, 354, 1086, 1337, 687, 916, 850, 1389, 837, 377, 511, 1023, 619, 2154, 489, 1373, 131, 756, 282, 445, 284, 1143, 1101, 318, 1744, 664, 797, 516, 705, 286, 383, 840, 1221, 1348, 283, 1009, 1656, 442, 721, 462, 636, 389, 417, 365, 325, 849, 531, 420, 454, 261, 214, 681, 134, 550, 400, 242, 347, 1222, 844, 695, 585, 141, 401, 958, 389, 295, 394, 578, 1022, 658, 422, 1298, 448, 511, 1314, 127, 227, 872]}


def test_dir():
    bv_list_path = os.path.join(dir_path, "bv_list.json")
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    if not os.path.exists(bv_list_path):
        print("创建json成功！")
        with open(bv_list_path, "w") as f:
            json.dump({}, f, indent=4)
    else:
        pass

# 根据BV下载网络数据
def get_json(bv):
    return rq.get(url.format(bv), headers=header).json()


# 保存json数据到本地
def save_json(name, data):
    path = os.path.join(dir_path, f"{name}.json")
    if os.path.exists(path):
        return True     # 文件已存在
    else:
        with open(path, "w") as f:
            json.dump(data, f)
    return None


# 打开数据文件
def open_json(name):
    path = os.path.join(dir_path, f"{name}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
            return data
    else:
        return False    # 文件不存在



# 获取data目录下所有json文件名
def get_list() -> list:
    file_names = [file.split('.')[0] for file in os.listdir(dir_path)]
    return file_names


# 解析json，去掉冗余数据
def parse_json(data) -> json:
    duration_list = [i["duration"] for i in data["data"]["pages"]]
    json_data = {
        "bv": data["data"]["bvid"],
        "title": data["data"]["title"],
        "duration_list": duration_list
    }
    return json_data


# 删除json文件
def delete_json(name):
    if os.path.exists(os.path.join(dir_path, f"{name}.json")):
        os.remove(os.path.join(dir_path, f"{name}.json"))
        return True
    else:
        return False


def save_bv(bv, title):
    file_path = os.path.join(dir_path, "bv_list.json")
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    data[bv] = title
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def get_bv_list():
    file_path = os.path.join(dir_path, "bv_list.json")
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def delete_bv(bv):
    file_path = os.path.join(dir_path, "bv_list.json")
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    del data[bv]
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


# print(parse_json(get_json("BV1iD4y1D7C8")))
# save_json(temp_data["title"], temp_data)

# delete_json("Python-GUI编程-pyqt5最新详细教程（一）")
# print(open_json("Python-GUI编程-pyqt5最新详细教程"))
# print(get_list())
# print(open_bv())
# save_bv("BV1iD4y1D7C8", "Python-GUI编程-pyqt5最新详细教程")
# delete_bv("BV1iD4y1D7C8")

# test_dir()