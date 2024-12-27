import json

# 打开名为 city.json 的文件并读取其中的内容
with open('city.json', 'r', encoding='utf-8') as file:
    json_data = file.read()

# 使用 json.loads() 方法将 JSON 字符串加载为 Python 字典
data = json.loads(json_data)

# 提取所有 subLevelModelList 中的 code 值
sublevel_codes = []
for city in data['zpData']['cityList']:
    if city['subLevelModelList']:
        for sublevel in city['subLevelModelList']:
            sublevel_codes.append(sublevel['code'])

# 打印提取的 subLevelModelList 中的 code 值
print("提取的 subLevelModelList 中的 code 值：", sublevel_codes)

# 写入到名为 city.txt 的文件，并在写入的时候换行
with open('city.txt', 'w', encoding='utf-8', newline='\n') as file:
    file.write(str(sublevel_codes))
    file.write('\n')


