def swapFileData():
    file1 = input('Enter the name of first file: \t')
    file2 = input('Enter the name of second file: \t')
    with open(file1) as f:
        a = f.read()
    with open(file2) as f:
        b = f.read()
    with open(file2, 'w') as f:
        f.write(a)
    with open(file1, 'w') as f:
        f.write(b)
swapFileData()