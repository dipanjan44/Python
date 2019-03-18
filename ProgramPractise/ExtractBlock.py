import os

parent_dir = "/Users/dipanjan/Desktop/test_folder"
out_file = "result.txt"
file_map = {}
file_list = os.listdir(parent_dir)
file_counter = 0
with open(out_file, 'w+', encoding="utf8", errors='ignore') as result:
    result.write("<Firmware vector>" + "\n")
    for subdir, dirs, files in os.walk(parent_dir):
        for file in files:
            file_path = subdir + os.sep + file
            print(file_path)
            block = ""
            found = False
            for line in open(file_path, encoding="utf8", errors='ignore'):
                if found:
                    if "id=" in line:
                        updated_line = line.replace(line.split(' ')[1], "id=" + str(file_counter))
                        block += updated_line + ' ' + "\n"
                    else:
                        block += line
                    if line.strip() == "</block>":
                        break
                else:
                    if line.strip() == "<block>":
                        found = True
                        block = "<block>" + "\n"
            result.write(block)
            print(block)
            file_counter = file_counter + 1
    result.write("</Firmware Vector>")
