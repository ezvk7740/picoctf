import subprocess
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
import hashlib

def check_hash(fstring):
    fdata = "e7ae6cfee91a324590df7b048dcc9802b7389c1b0d996d474d61c4cbb1253455"
    try:
        file_string = fstring
        hash_obj = hashlib.sha256(file_string)
        out = hash_obj.hexdigest()
        if out == fdata:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def fread():
    with open('rockyou.txt', 'rb') as f:
        return f.readlines()

def hashsearch(debug=False):
    if debug:
        process = subprocess.run(["sha256sum"],
                                stdout=subprocess.PIPE,
                                text=True,
                                input = "\"hello\"")
        print(process.stdout.strip().split(" ")[0])
        print(fread())
    else:
        f = fread()
        with ProcessPoolExecutor() as executor:
            count = 0
            for string, output in tqdm(zip(f, executor.map(check_hash, f))):
                if output:
                    print('matched: {0}'.format(string.strip().decode("utf-8")))
                else:
                    count += 1
            print("non-matches {0}".format(count))

if __name__ == "__main__":
    hashsearch(False)
    # answer: uwillnevafindout, runtime: 32 minutes
