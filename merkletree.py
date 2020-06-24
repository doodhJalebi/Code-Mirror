import os
import hashlib
import time


class merkletree:
    def __init__(self, root_directory):
        self.root = root_directory  # root directory of the mt folder
        self.merkletree = {}
        self.hashes = dict()  # key: filename \\ value: hash
        self.root_hash = ''  # merkle root hash
        self.MerkleTree()

    def buildMT(self):
        for filename, hash in self.hashes.items():
            items = self.getitems(filename)
            list = {}
            temp = []
            temp.append(filename)
            for x in items:
                if filename == self.root:
                    list[self.hashes[x]] = x
                else:
                    list[self.hashes[os.path.join(filename, x)]] = os.path.join(
                        filename, x)
            temp.append(list)
            self.merkletree[hash] = temp
        self.root_hash = self.hashes[self.root]

    def MerkleTree(self):
        self.HashList(self.root)
        self.buildMT()

    def hasher(self, data):
        hash = hashlib.md5()
        path = os.path.join(self.root, data)
        hash_object = hashlib.md5(data.encode("utf-8"))
        if os.path.isfile(path):
            try:
                openfile = open(path, "r", encoding="utf-8")
            except:
                return "Error! Unable to open", path
            while True:
                datachunk = openfile.read(8096)
                if not datachunk:
                    break
                hash.update(datachunk.encode())
            openfile.close()
        else:
            hash.update(data.encode())
        return hash.hexdigest()+hash_object.hexdigest()

    def getitems(self, dir):
        temp = []
        if dir != self.root:
            dir = os.path.join(self.root, dir)
            # check whether the specified path is an existing directory
        if os.path.isdir(dir):
            # a list containing the names of the entries in the directory
            lst = os.listdir(dir)
            for i in lst:
                if i != "__pycache__":
                    temp.append(i)
            temp.sort()
        return temp

    def childHL(self, root_directory):
        files = self.getitems(root_directory)
        if not files:
            self.hashes[root_directory] = ''
            return
        for file in files:
            filepath = os.path.join(root_directory, file)
            if os.path.isdir(filepath):
                self.childHL(file)
                subfiles = self.getitems(file)
                temp = ''
                for subfile in subfiles:
                    temp += self.hashes[os.path.join(file, subfile)]
                if root_directory == self.root:
                    self.hashes[file] = self.hasher(temp)
                else:
                    self.hashes[filepath] = self.hasher(temp)
            else:
                if root_directory == self.root:
                    self.hashes[file] = self.hasher(file)
                else:
                    self.hashes[filepath] = self.hasher(filepath)

    def HashList(self, root_directory):
        self.childHL(root_directory)
        files = self.getitems(root_directory)
        if not files:
            self.hashes[root_directory] = ''
            return
        temp = ''
        for subfiles in files:
            temp += self.hashes[subfiles]
        self.hashes[root_directory] = self.hasher(temp)

# change_list = []


# MTa -> primary folder, MTb -> secondary folder
def Difference(MTa, MTb, aTophash, bTophash, change_list: list):
    # Will compare the two Merkel Tree and their root hash to check if they contain same content or not
    if aTophash == bTophash:
        # if hashes of both files are same
        print("Both trees have the same merkle root hash")
    else:
        # checking if contents of both files are same or changed
        valA = MTa.merkletree[aTophash]
        # valA -> ['location of folder MTa', {hash of its children file/es : filename }] each key:value pair for each file
        childA = valA[1]
        # childA -> dict containing hash (as key) and filename (as value) of childrens of a (files that exists in folder MTa)
        valB = MTb.merkletree[bTophash]
        childB = valB[1]

        for hash, filename in childA.items():
            # comparing children dictionary of MTa with that of MTb to compare
            try:
                # if hash of particular file a in childA has the same filename as value in ChildB[hash]
                # continue the matching until any difference noticed
                if childB[hash] == filename:
                    print("Unchanged: ", os.path.join(MTa.root, filename))
            except:
                # else print the filename where changes have occured
                if (os.path.isdir(os.path.join(MTb.root, filename)) == False) or (os.path.isdir(os.path.join(MTa.root, filename)) == False):
                    change_list.append(filename)
                # print("Changed: ", filename)
                # print(change_list)
                #print(os.path.isdir(os.path.join(MTb.root, filename)))
                # print(os.path.isdir(os.path.join(MTa.root,filename)))
                temp = MTa.merkletree[hash]
                if len(temp[1]) > 0:
                    differencehash = list(
                        set(childB.keys()) - set(childA.keys()))
                    # continue finding changes that are changed (have diff hash) after one file (if there exist any)
                    if differencehash != []:
                        Difference(MTa, MTb, hash,
                                   differencehash[0], change_list)
    # print(change_list)
    return change_list


a_dir = r"C:\Users\USER\Desktop\a"
b_dir = r"C:\Users\USER\Desktop\b"

a = merkletree(a_dir)
b = merkletree(b_dir)
print(a.merkletree)
