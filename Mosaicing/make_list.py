import os

def list_all_files(rootdir):

    _files = []
    lst = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(lst)):
           path = os.path.join(rootdir,lst[i])
           if os.path.isdir(path):
              _files.extend(list_all_files(path))
           if os.path.isfile(path):
              spt = path.split('.')
              if spt[-1] == 'jpg' or spt[-1] == 'jpeg' or spt[-1] == 'png' or spt[-1]=='JPEG':
                  _files.append(path)
                  f = open('record.txt','a')
                  f.writelines(str(path)+" \n")
                  f.close()
                  print(str(path))
                  
    return _files

root = './Dataset'

_file_s = list_all_files(root)

# for i in _file_s:
#     f = open('record.txt','a')
#     f.writelines(str(i)+' \n')
#     f.close()
#     print(str(i))
