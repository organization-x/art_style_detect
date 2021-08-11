import os

def crt_master(dirs):
    masterlist = os.path.join(os.getcwd, "masterlist.txt")
    for d in dirs:
        d = os.path.join(os.getcwd, d)
        for subdir, _, files in d:
            for f in files:
                with open(masterlist, 'a') as master:
                    master.write(os.path.join(subdir, f) + "\n")

if __name__ == "__main__":
    crt_master(["train", "validate", "test"])
    print("done")