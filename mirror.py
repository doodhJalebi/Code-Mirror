import shutil
import time
from merkletree import *

import os


def mirror(src_dir, dst_dir):
    src = merkletree(src_dir)
    dst = merkletree(dst_dir)
    #creates a merkletree each for both source and destination directory

    changes_insertion = set(Difference(
        src, dst, src.root_hash, dst.root_hash, []))
    '''
    changes_insertion contains the path of files/folders relative to the
    base directory for those files/folders that require modification or 
    insertion into the destination folder.
    '''

    changes_deletion = set(Difference(
        dst, src, dst.root_hash, src.root_hash, []))
    changes_deletion.difference_update(
        changes_deletion.intersection(changes_insertion))

    '''
    changes_deletion contained the path of files/folders relative to the
    base directory for those files/folders that require anti-modification
    (relative to the source dir) or deletion into the destination folder.

    To get rid of anti-modifications we remove the intersection of two sets
    since modification and anti-modification both are represented by same paths.
    '''

    

    for filename in changes_insertion:
        if os.path.isdir(os.path.join(dst_dir, filename)):
            shutil.rmtree(os.path.join(dst_dir, filename))
            #Removing outdated folders from dst

        if os.path.isfile(os.path.join(dst_dir, filename)):
            os.unlink(os.path.join(dst_dir, filename))
            #Removing outdated files from dst

        if os.path.isdir(os.path.join(src_dir, filename)) == True:
            if len(os.listdir(os.path.join(src_dir, filename))) == 0:
                os.mkdir(os.path.join(dst_dir, filename))
                #if folder that needs to be added is empty
                #create empty directory

            else:
                shutil.copytree(os.path.join(src_dir, filename),
                                os.path.join(dst_dir, filename))
                #else copy folder from src to dst folder

        if os.path.isfile(os.path.join(src_dir, filename)) == True:
            shutil.copy(os.path.join(src_dir, filename),
                        os.path.join(dst_dir, filename))
            #copy the updated file from src to dst folder
        
    for filename in changes_deletion:
        if os.path.isdir(os.path.join(dst_dir, filename)):
            shutil.rmtree(os.path.join(dst_dir, filename))
            #removing folders from dst that need to be deleted

        if os.path.isfile(os.path.join(dst_dir, filename)):
            os.unlink(os.path.join(dst_dir, filename))
            #removing files from dst that need to be deleted

    time.sleep(1)


a_dir = r"C:\Users\DELL 5559\Desktop\a"
b_dir = r"C:\Users\DELL 5559\Desktop\b"


while True:
    try:
        mirror(a_dir, b_dir)
    except:
        pass
