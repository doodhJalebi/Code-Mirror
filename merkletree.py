import os
import hashlib


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
        if os.path.isfile(path):
            try:
                openfile = open(path, "r", encoding="utf-8")
            except:
                return "Error! Unable to open", path
            while True:
                datachunk = openfile.read(8096)
                if not datachunk:
                    break
                hash.update(datachunk.encode("utf-8"))
            openfile.close()
        else:
            hash.update(data.encode("utf-8"))
        return hash.hexdigest()

    def getitems(self, dir):
        temp = []
        if dir != self.root:
            dir = os.path.join(self.root, dir)
            # check whether the specified path is an existing directory
        if os.path.isdir(dir):
            # a list containing the names of the entries in the directory
            lst = os.listdir(dir)
            for i in lst:
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


def Difference(MTa, MTb, aTophash, bTophash):
    if aTophash == bTophash:
        print("Both trees have the same merkle root hash")
    else:
        valA = MTa.merkletree[aTophash]
        childA = valA[1]
        valB = MTb.merkletree[bTophash]
        childB = valB[1]

        for hash, filename in childA.items():
            try:
                if childB[hash] == filename:
                    print("Unchanged: ", filename)
            except:
                print("Changed: ", filename)
                temp = MTa.merkletree[hash]
                if len(temp[1]) > 0:
                    differencehash = list(
                        set(childB.keys()) - set(childA.keys()))
                    Difference(MTa, MTb, hash, differencehash[0])

