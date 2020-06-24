import shutil
import time
from merkletree import *

import os


def mirror(src_dir, dst_dir):
    src = merkletree(src_dir)
    dst = merkletree(dst_dir)

    changes_insertion = set(Difference(
        src, dst, src.root_hash, dst.root_hash, []))
    # new files and modified files

    # print('changes_insertion')
    # print(changes_insertion)

    changes_deletion = set(Difference(
        dst, src, dst.root_hash, src.root_hash, []))
    # deleted file and modified files

    # print('changes_deletion')
    # print(changes_deletion)

    changes_deletion.difference_update(
        changes_deletion.intersection(changes_insertion))

    for filename in changes_insertion:
        if os.path.isdir(os.path.join(dst_dir, filename)):
            shutil.rmtree(os.path.join(dst_dir, filename))
            #print("in directory deletion:",os.path.join(dst_dir, filename))

        if os.path.isfile(os.path.join(dst_dir, filename)):
            os.unlink(os.path.join(dst_dir, filename))
            #print("in file deletion:",os.path.join(dst_dir, filename))

        if os.path.isdir(os.path.join(src_dir, filename)) == True:
            if len(os.listdir(os.path.join(src_dir, filename))) == 0:
                os.mkdir(os.path.join(dst_dir, filename))
            else:
                shutil.copytree(os.path.join(src_dir, filename),
                                os.path.join(dst_dir, filename))

        if os.path.isfile(os.path.join(src_dir, filename)) == True:
            shutil.copy(os.path.join(src_dir, filename),
                        os.path.join(dst_dir, filename))

        #os.popen('copy '+ os.path.join(src_dir,filename)+ os.path.join(dst_dir, filename))

    for filename in changes_deletion:
        if os.path.isdir(os.path.join(dst_dir, filename)):
            shutil.rmtree(os.path.join(dst_dir, filename))
        if os.path.isfile(os.path.join(dst_dir, filename)):
            os.unlink(os.path.join(dst_dir, filename))

    time.sleep(1)


a_dir = r"C:\Users\USER\Desktop\a"
b_dir = r"C:\Users\USER\Desktop\b"


while True:
    try:
        mirror(a_dir, b_dir)
    except:
        pass
