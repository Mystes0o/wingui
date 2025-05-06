import configparser

def read_ini(file_path):
    """
    读取INI文件
    :param file_path: INI文件路径
    :return: configparser.ConfigParser 对象
    """
    config = configparser.ConfigParser()
    config.read(file_path, encoding='utf-8')
    return config

def modify_ini(config, section, key, value):
    """
    修改INI文件内容
    :param config: configparser.ConfigParser 对象
    :param section: 需要修改的节（section）
    :param key: 需要修改的键（key）
    :param value: 新的值
    """
    if not config.has_section(section):
        config.add_section(section)  # 如果节不存在，则创建
    config.set(section, key, value)

def save_ini(config, file_path):
    """
    保存INI文件
    :param config: configparser.ConfigParser 对象
    :param file_path: 保存的文件路径
    """
    with open(file_path, 'w', encoding='utf-8') as configfile:
        config.write(configfile)

def main(ini_file):
    # 读取INI文件
    config = read_ini(ini_file)

    # 打印原始内容
    print("原始内容：")
    for section in config.sections():
        print(f"[{section}]")
        for key, value in config.items(section):
            print(f"{key} = {value}")

    # 修改内容
    modify_ini(config, 'Section1', 'key1', 'new_value1')  # 修改现有键值
    modify_ini(config, 'Section2', 'key2', 'value2')     # 添加新节和键值

    # 保存修改后的INI文件
    save_ini(config, ini_file)

    # 打印修改后的内容
    print("\n修改后内容：")
    for section in config.sections():
        print(f"[{section}]")
        for key, value in config.items(section):
            print(f"{key} = {value}")

if __name__ == "__main__":
    ere = read_ini(r"C:\Users\admini\AppData\Local\EaseUS\RecExperts\EreOptionsSettings.ini")
    print(ere.sections())