import os
# Operating system library
# To interface with the underlying operating system that Python is running on
import hashlib
# Python Library for generating secure hash


class merkletree:
    def __init__(self, root_directory):
        
        self.root = root_directory
        # root directory of the merkel tree folder
        
        self.merkletree = {}
        # MT is a dict containing hash of the respective files (as key) and the list conatining file name and its childrens dict (as value)
        # Starting with files (childrens) and their respective hash, it later compiles the hash for the folder (parent) using children hashes (previous keys)
        
        self.hashes = dict()
        # { filename -> key : hash -> value}
        
        self.root_hash = ''
        # merkle root hash /  hash of the folder in the given root directory
        
        self.MerkleTree()

    def buildMT(self): # For generating merkel-tree dict
        
        for filename, hash in self.hashes.items():
            items = self.getitems(filename)
            # list of files that exists in the filename folder
            list = {}
            # {hash : filename}
            temp = []
            temp.append(filename)
            
            for x in items:
                # x -> name of file within the given folder
                if filename == self.root:
                    list[self.hashes[x]] = x
                else:
                    list[self.hashes[os.path.join(filename, x)]] = os.path.join(
                        filename, x)
            temp.append(list)
            # temp is a list of  -> [filename , its dict of its child (file/es as values) and their hashes as keys if any exists]
            self.merkletree[hash] = temp
            
        self.root_hash = self.hashes[self.root]
        

    def MerkleTree(self):
        self.HashList(self.root)
        self.buildMT()

    def hasher(self, data): # for generating hashes and encoding the data
        hash = hashlib.md5() # Hash Function
        path = os.path.join(self.root, data)
        if os.path.isfile(path):
            try:
                openfile = open(path, "r", encoding="utf-8")
            except:
                return "Error! Unable to open", path
            while True:
                datachunk = openfile.read(8096)
                # It reads chunks of the file into memory
                # Anything above 1: means file is line buffered (say 8k.. ie: 8096, or higher) it does ^^
                if not datachunk:
                    break
                hash.update(datachunk.encode("utf-8"))
                # Converts the datachunk ( -> string) into bytes to be acceptable by hash function
            openfile.close()
        else:
            hash.update(data.encode("utf-8"))
        return hash.hexdigest() # Returns the encoded data in hexadecimal format

    def getitems(self, dir):
        temp = []
        if dir != self.root:
            dir = os.path.join(self.root, dir)
        if os.path.isdir(dir):
            # if specified directory/path is an existing directory...
            lst = os.listdir(dir)
            # ... it'll make a list containing the names of the entries (file/es) in the directory given by path
            for i in lst:
                temp.append(i)
            temp.sort()
        return temp
        #  It returns sorted list of file/s that exists in the folder whose directory is given

    def childHL(self, root_directory):
        files = self.getitems(root_directory)
        # Lists of files that exists in the given root directory
        if not files:
            self.hashes[root_directory] = ''
            return
        for file in files:
            filepath = os.path.join(root_directory, file)
            if os.path.isdir(filepath):
            # if path is valid and the file exists in the given dir..
                self.childHL(file)
                # checking for further children of file (if any)
                subfiles = self.getitems(file)
                # subfile -> list of subfiles that exists in the given file
                temp = ''
            # making the dictionary of filename and its respective hash
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
        # Lists of files that exists in the given root directory
        if not files:
            self.hashes[root_directory] = ''
            return
        temp = ''
        for subfiles in files:
            temp += self.hashes[subfiles]
        self.hashes[root_directory] = self.hasher(temp)
        # self.hashes -> dict { hash as key : filename as values }
        # hashes (keys) of children files are alloted first then using those hashes
        # folder name (parent) is hashed


def Difference(MTa, MTb, aTophash, bTophash): #MTa -> primary folder, MTb -> secondary folder
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
                print("Changed: ", os.path.join(MTa.root, filename))
                temp = MTa.merkletree[hash]
                if len(temp[1]) > 0:
                    differencehash = list(
                        set(childB.keys()) - set(childA.keys()))
                    # continue finding changes that are changed (have diff hash) after one file (if there exist any)
                    Difference(MTa, MTb, hash, differencehash[0])



