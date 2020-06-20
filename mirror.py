import shutil
import time
from merkletree import merkletree
from merkletree import Difference
import os


def mirror(src_dir,dst_dir):
    src=merkletree(src_dir)
    dst=merkletree(dst_dir)
    changes=Difference(src,dst,src.root_hash,dst.root_hash)
    for filename in changes:
        if os.path.isdir(os.path.join(dst_dir,filename)):
            shutil.rmtree(os.path.join(dst_dir, filename))
            #print("in directory deletion:",os.path.join(dst_dir, filename))
        if os.path.isfile(os.path.join(dst_dir,filename)):
            os.unlink(os.path.join(dst_dir, filename))
            #print("in file deletion:",os.path.join(dst_dir, filename))
        if os.path.isdir(os.path.join(src_dir,filename))==True:
            shutil.copytree(os.path.join(src_dir,filename), os.path.join(dst_dir, filename))
        if os.path.isfile(os.path.join(src_dir,filename))==True:
            shutil.copy(os.path.join(src_dir,filename), os.path.join(dst_dir, filename))
        
        #os.popen('copy '+ os.path.join(src_dir,filename)+ os.path.join(dst_dir, filename))
    time.sleep(1)
    

a_dir=r"C:\Users\DELL 5559\Desktop\a"
b_dir=r"C:\Users\DELL 5559\Desktop\b"
a = merkletree(a_dir)
b = merkletree(b_dir)
print(a.merkletree)
print(a.root_hash)
print('-----------------------------')
print(b.merkletree)
print(Difference(a, b, a.root_hash, b.root_hash))

while True:
    change_list=[]
    mirror(a_dir,b_dir)

