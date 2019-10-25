import urllib2 
import sys,os.path
from bs4 import BeautifulSoup

APPEND_TEXT = {".jsp":"<%--NO I18N--%>",".java":"//No I18N",".js":"//No I18N"}

def findLineNumbers(link):
    html_content = urllib2.urlopen(link).read()
    parsed_html = BeautifulSoup(html_content,features="html.parser")

    table_list = parsed_html.body.find_all("table")
    file_name_list = []
    line_numbers = {}
    for table in table_list[1:]:
        file_name_list.append(table.font.b.text)
        line_number = []
        for row in table.findAll('tr')[2:]:
            line_number.append(row.findAll('td')[1].font.text)
            print(row)
            print(row.findAll('th'))
        line_numbers[table.font.b.text] = line_number
    return line_numbers,file_name_list

def findFileExtension(file_name):
    return os.path.splitext(file_name)[1]


argumentList = sys.argv 
if(len(argumentList)<3):
    print("OOOps, Usage : AutoI18n.py link folder_path_to_git_root_folder")
else:
    link = argumentList[1]
    source_path = argumentList[2]
    line_numbers,file_name_list = findLineNumbers(link)
    
    print("Parsing started")
    print("===============")
    print("file name list = "+str(file_name_list))
    print("===============")
    print("line number list = "+str(line_numbers))
    print("===============")
    print("Parsing ended")
    for fi in file_name_list:
        file_extension  = findFileExtension(fi)
        print("File path = "+ source_path+"/"+fi)
        print("I18n started")
        try:
            file_lines = []
            with open(source_path+"/"+fi, "r") as file: 
                file_lines = file.readlines()
            for line_number in line_numbers[fi]:
                file_lines[int(line_number)-1] = file_lines[int(line_number)-1].replace('\n', '') + APPEND_TEXT[file_extension] + '\n'
            with open(source_path+"/"+fi, "w") as file:
                file.writelines(file_lines)
                print("I18n ended")
                print("===============")      
        except IOError:
            print("Could not open file = "+fi+" ,Aborting operation!!!!")
            sys.exit()


        
    


