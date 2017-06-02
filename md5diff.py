import base64
import os
import binascii
import re
import magic
import hashlib

scanDirectory = "./Files"

fw = open("./powershell", 'w')


def isBase64Regex(s):
    return (len(s) % 4 == 0) and re.match('^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$', s)


def isbase64(x):
    result = True
    try:
        base64.decodestring(x)
    except binascii.Error:
        result = False
    return result


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def includes_curlibraces(s):
    return re.match('^\{.*.\}$', s)


def containsflag(s, baseFolder):
    try:
        result = base64.b64decode(s)
        if is_ascii(result) and includes_curlibraces(result):
            if len(result) > 0:
                print(result + "," + baseFolder)
                fw.write(result + "," + baseFolder + "\n")
    except binascii.Error:
        print("Error")


def containsPowerShellScripts(s, baseFolder):
    try:
        if is_ascii(s) and len(s) > 0:
            if 'iex ([Text.Encoding]::ASCII.GetString' in s:
                print(s + "," + baseFolder)
                fw.write(s + "," + baseFolder + "\n")
    except binascii.Error:
        print("Error")


def generate_file_md5(rootdir, filename, blocksize=2 ** 20):
    m = hashlib.md5()
    with open(os.path.join(rootdir, filename), "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


for root, dirs, files in os.walk(scanDirectory, topdown=False):
    for name in files:
        try:
            filepath = root + "/" + name
            filetype = magic.from_file(filepath)

            if filetype == "empty" or filetype.__contains__("ASCII") or filetype.__contains__("UTF-8"):
                md5Generation = generate_file_md5(root, name)
                print(md5Generation + "," + filepath)
        except Exception:
            pass

            # fp = open("Files/DiffIEUser.txt", "r")
            # fp = open("abc.txt", "r")

            # for line in fp:
            #     nl = line.split(":")
            #     nameAll = nl[1:]
            #     name = ((nameAll[0].split("."))[0])
            #     #print nameAll
            #     try:
            #         decName = base64.decodestring(name)
            #         print decName
            #         #if "ag" in decName:
            #             #print name + "  - - - - >  " + decName
            #     except :
            #         pass
            # fp.close()
            #     #print (name)
