import os
import sys
import glob
import json
import shutil
import tarfile
import datetime
import subprocess

RESULT_DIR = 'result'
author = 'shigetoshi'


def get_move_list(root):
    move_list = []

    def get_json_list(root):
        return glob.glob('{}/**/*.json'.format(root), recursive=True)

    def get_extension(path):
        pos = path[:-5].rfind('.')
        return path[pos + 1:][:-5].lower()

    for json_file in get_json_list(root):
        if 'Photos from' not in json_file:
            continue
        with open(json_file) as j:
            try:
                json_obj = json.load(j)
                if 'photoTakenTime' in json_obj:
                    src = json_file
                    timestamp = int(json_obj['photoTakenTime']['timestamp'])
                    title = json_obj['title']
                    dt = datetime.datetime.fromtimestamp(
                        timestamp,
                        tz=datetime.timezone(datetime.timedelta(hours=9)))
                    date = str(dt.date()).replace('-', '')
                    time = str(dt.time()).replace(':', '')
                    dst = '{}/date={}/{}/{}-{}.{}.json'.format(
                        RESULT_DIR, date, author, date, time, title)
                    move_list.append((src, dst))
            except:
                print("[Error] Broken json: {}".format(json_file))
    return move_list


def untar(tar):
    with tarfile.open(tar) as t:
        t.extractall()


def check_duplicated(move_list):
    checker = {}
    for s, d in move_list:
        checker.setdefault(d, []).append(s)
    for a, b in checker.items():
        if len(b) > 1:
            print(a)
            print('  ' + '\n  '.join(b))


def execute_move(move_list):
    for m in move_list:
        if os.path.exists(m[0][:-5]):
            os.makedirs(os.path.dirname(m[1]), exist_ok=True)
            shutil.move(m[0], m[1])
            shutil.move(m[0][:-5], m[1][:-5])


#for tar in sys.argv[1:]:
#untar(tar)
root = 'Takeout'
move_list = get_move_list(root)
check_duplicated(move_list)
execute_move(move_list)
