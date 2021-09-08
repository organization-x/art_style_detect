import os

class Masterlist:
    def __init__(self):
        self.cwd = os.getcwd()
        lists = [os.path.join(self.cwd, "trains.txt"), os.path.join(self.cwd, "valids.txt"), os.path.join(self.cwd, "tests.txt")]
        
        self.dirpaths = ["train", "valid", "test"]      #paths (names if same dir) of image folders

        self.filepaths = {self.dirpaths[i]:lists[i] for i in range(len(self.dirpaths))}
        print(self.filepaths)

    def crt_list(self, dirpath):
        full_path = os.path.join(self.cwd, dirpath)
        for subdir, _, files in os.walk(full_path):
            for f in files:
                if f.endswith("jpg"):
                    with open(self.filepaths[dirpath], 'a') as master:
                        master.write(os.path.join(subdir, f) + "\n")  #results in extra empty line at end of file - does that work?

    def crt_lists(self):
        for dirpath in self.dirpaths:
            self.crt_list(dirpath)

if __name__ == "__main__":
    master = Masterlist()
    master.crt_lists()
    print("done")