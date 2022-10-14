import pandas as pd
import numpy as np
import os

#Список всех файлов в рабочей папке
def list_files_in_dir_and_subdir(work_path):
    file_list = []
    all_list = os.listdir(work_path)
    all_list = [os.path.normpath(os.path.join(work_path, var)) for var in all_list]
    tmp_list = []
    while all_list:
        for path in all_list:
            if os.path.isfile(path):
                file_list.append(os.path.normpath(path))
                pass
            else:
                subdir_list = os.listdir(path)
                subdir_list = [os.path.normpath(os.path.join(path, var)) for var in subdir_list]
                tmp_list.extend(subdir_list)
                pass
        all_list = tmp_list
        tmp_list = []
    return file_list

#Обрезает начало и конец файла от лишних знаков
def cut_file(file_source):
    file_string_arr = []
    file = open(file_source, 'r')
    for line in file:
        pos = line.find(':')
        part1 = line[pos + 2:]
        pos2 = part1.find(';')
        part2 = part1[:pos2 - 1]
        file_string_arr.append(part2)
    file.close()
    with open("delete_duplicates\Work_data\Balanced_data.txt", "w") as new_file:
        new_file.write("\n".join(file_string_arr))
    return "delete_duplicates\Work_data\Balanced_data.txt"

# Delete dublicates with pandas
def delete_dubl(balance_data_file):
    df_state = pd.read_fwf(balance_data_file)
    precise_frames = df_state.drop_duplicates(keep = 'first')
    np.savetxt(r'delete_duplicates\Work_data\data_temp.txt', precise_frames, fmt='%s')
    return('delete_duplicates\Work_data\data_temp.txt')
    

#Make work file with good data
def make_work_file(temp_file, work_file):
    new_lines = []
    file = open(temp_file, 'r')
    lines = file.readlines()
    file.close()
    for line in lines:
        new_lines.append(' '.join([word for word in line.split() if word != 'nan']))
    f = open(work_file, 'w')
    for line in new_lines:
        f.write("{}\n".format(line))
    f.close()
    return 0

# Make new not ambigious work files path
def make_file_path(list_file):
    list_new_file = []
    for num, obj in enumerate(list_file):
        pos = obj.find('Data')
        part = obj[pos + 4:]
        pos2 = part.find('.')
        part2 = part[:pos2]
        list_new_file.append("delete_duplicates\Work_data" + part2 + "_" + str(num) + '.txt')
    return list_new_file

list_dir_and_file = list_files_in_dir_and_subdir("delete_duplicates\Data")
print("Найдено файлов: ", list_dir_and_file)

list_work_files = make_file_path(list_dir_and_file)

for num, file_path in enumerate(list_dir_and_file):
    if ".txt" in file_path:  # os.path.isfile(file_path):
        print("Обработка файла: ", file_path)

        file = open(file_path, "r")
        file_lines_str = "".join(file.readlines())
        print("Всего строк в файле:", len(file_lines_str.split("\n")))
        
        make_work_file(delete_dubl(cut_file(file_path)), list_work_files[num])

temp_list = os.listdir("delete_duplicates\Work_data")

for i in range(len(list_dir_and_file) ):
    if ("delete_duplicates\Work_data\\" + temp_list[i]) not in list_work_files:
        os.remove("delete_duplicates\Work_data\\" + temp_list[i])
os.remove("delete_duplicates\Work_data\\data_temp.txt")

print("DONE!")
