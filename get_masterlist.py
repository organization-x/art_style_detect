import os

def crt_list(dirs, cwd):
    for d in dirs:
        d = os.path.join(cwd, d)
        for subdir, _, files in d:
            for f in files:
                with open(masterlist, 'a') as master:
                    master.write(os.path.join(subdir, f) + "\n")

if __name__ == "__main__":
    cwd = os.getcwd()
    train_list = os.path.join(cwd, "trains.txt")
    valid_list = os.path.join(cwd, "valids.txt")
    test_list = os.path.join(cwd, "tests.txt")
    crt_list(["train", "validate", "test"], cwd)
    print("done")