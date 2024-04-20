import os

def get_file_list(file_dir):
    files = os.listdir(file_dir)
    files_num = len(files)
    return files, files_num

def generate_txt(target_path, txt_name=r'./output.txt'):
    f = open(txt_name, "w")
    files, files_num = get_file_list(target_path)
    index_count = 0
    count = 0
    for file in files:
        index_count = index_count + 1
        if count == files_num - 1:
            f.write(os.path.join(target_path, str(file)))
            break
        if index_count >= 0:
            f.write(os.path.join(target_path, str(file)) + "\n")
            count = count + 1
    f.close()

def read_file_from_txt(txt_path):
    files = []
    for line in open(txt_path, "r"):
        files.append(line.strip())
    return files

if __name__ == "__main__":
    file_dir = r"D:\PythonProject\pyzjrPyPi\pyzjr\data"
    generate_txt(file_dir)
    print(read_file_from_txt("./output.txt"))