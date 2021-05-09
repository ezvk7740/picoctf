import subprocess

debug = False

if debug:
    process = subprocess.run(["sha256sum"], stdout=subprocess.PIPE, text=True, input = "\"hello\"")
    print(process.stdout.strip().split(" ")[0])
else:
    out = set()
    fdata = "e7ae6cfee91a324590df7b048dcc9802b7389c1b0d996d474d61c4cbb1253455"
    with open('rockyou.txt', 'rb') as f:
    #    print(f.readlines()[0].strip().decode("utf-8"))
        for files in f.readlines():
            try:
                file_string = files.strip().decode("utf-8")
                print(file_string)
                process = subprocess.run(["sha256sum"], stdout=subprocess.PIPE, text=True, input = "\"" + file_string + "\"")
                output = process.stdout.strip().split(" ")[0]
                if output == fdata:
                    out.add(file_string)
            except:
                pass
        print(out)



