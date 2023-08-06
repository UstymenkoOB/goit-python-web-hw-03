from pathlib import Path
import threading
import os
import shutil

LIST_DIR = ["documents", "images", "audio", "video", "archives"]
images_ext = ['JPEG', 'PNG', 'JPG', 'SVG', 'BMP']
documents_ext = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']
audio_ext = ['MP3', 'OGG', 'WAV', 'AMR']
video_ext = ['AVI', 'MP4', 'MOV', 'MKV']
archives_ext = ['ZIP', 'GZ', 'TAR']
unknown_ext = []
images_list = []
documents_list = []
audio_list = []
video_list = []
archives_list = []
unknown_list = []

def normalize(name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    name_trans = ""
    for l in name:
        if ord(l) in TRANS:
            name_trans += TRANS[ord(l)]
        elif 'a' <= l <= 'z' or 'A' <= l <= 'Z' or '0' <= l <= '9' or l=="." or l==":" or l=="\\":
            name_trans += l
        else:
            name_trans += '_'
    return name_trans

def sort(path):
    p = Path(path)
    for i in p.iterdir():
        index = str(i).rfind("\\")
        name = str(i)[index+1:]
        if i.is_dir() and name not in LIST_DIR:
            thread = threading.Thread(target=sort, args=(i,))
            thread.start()
            thread.join()
        elif i.is_file():
            ext = i.suffix
            file_name = rename_file(str(i)) 
            if ext[1:].upper() in images_ext:
                images_list.append(file_name)
            elif ext[1:].upper() in documents_ext:
                documents_list.append(file_name)
            elif ext[1:].upper() in audio_ext:
                audio_list.append(file_name)
            elif ext[1:].upper() in video_ext:
                video_list.append(file_name)
            elif ext[1:].upper() in archives_ext:
                archives_list.append(file_name)
            else:
                if not ext[1:].upper() in unknown_ext:
                    unknown_ext.append(ext[1:].upper())
                unknown_list.append(file_name)


def rename_dir(path):
    p = Path(path)
    for i in p.iterdir():
        if i.is_dir():
            name = str(i)
            index = name.rfind("\\")
            path_dir = name[:index+1]
            name_new = normalize(name[index+1:])
            dir = path_dir+name_new
            os.rename(i, dir)
            rename_dir(dir)
    

def rename_file(file):
    index = file.rfind("\\")
    path_file = file[:index+1]
    name_new = normalize(file[index+1:])
    file_new = path_file+name_new
    os.rename(file, file_new)
    return file_new

def perenos(path):
    for el in LIST_DIR:
        p = Path(path) / el
        if not p.exists():
            os.mkdir(p)
        if el == "documents" and len(documents_list):
            for i in documents_list:
                index = i.rfind("\\")
                name = str(p)+"\\"+i[index+1:]
                os.rename(i, name)
        if el == "images" and len(images_list):
            for i in images_list:
                index = i.rfind("\\")
                name = str(p)+"\\"+i[index+1:]
                os.rename(i, name)
        if el == "audio" and len(audio_list):
            for i in audio_list:
                index = i.rfind("\\")
                name = str(p)+"\\"+i[index+1:]
                os.rename(i, name)
        if el == "video" and len(video_list):
            for i in video_list:
                index = i.rfind("\\")
                name = str(p)+"\\"+i[index+1:]
                os.rename(i, name)
        if el == "archives" and len(archives_list):
            for i in archives_list:
                index = i.rfind("\\")
                name_ext = str(p)+"\\"+i[index+1:]
                os.rename(i, name_ext)
                index = name_ext.rfind("\\")
                index_ext = name_ext.rfind(".")
                name_arc = name_ext[index+1:index_ext]
                fold = str(p)+'\\'+name_arc
                print(name_ext, fold, name_arc)
                shutil.unpack_archive(name_ext, fold)
                os.unlink(name_ext)


def del_empty_fold(path):
    for d in os.listdir(path):
        a = os.path.join(path, d)
        if os.path.isdir(a) and d not in LIST_DIR:
            del_empty_fold(a)
            if not os.listdir(a):
                os.rmdir(a)


def main(path):
    rename_dir(path)
    sort(path)
    perenos(path)
    del_empty_fold(path)


if __name__ == '__main__':
    main("c:\\motlokh")
