#last lines
#by Kevin Yuan
def read_last_lines(filename, lines = 1):
    #print the last line(s) of a text file
    """
    Argument filename is the name of the file to print.
    Argument lines is the number of lines to print from last.
    """
    block_size = 1024
    block = ''
    nl_count = 0
    start = 0
    fsock = file(filename, 'rU')
    try:
        #seek to end
        fsock.seek(0, 2)
        #get seek position
        curpos = fsock.tell()
        # print curpos
        while(curpos > 0): #while not BOF
            #seek ahead block_size+the length of last read block
            curpos -= (block_size + len(block));
            if curpos < 0: curpos = 0
            fsock.seek(curpos)
            #read to end
            block = fsock.read()
            nl_count = block.count('\n')
            #if read enough(more)
            if nl_count >= lines: break
        #get the exact start position
        for n in range(nl_count-lines+1):
            start = block.find('\n', start)+1
    finally:       
        fsock.close()
    return block[start:]
   
if __name__ == '__main__':
    file_path=r'E:\DOC\Parallels\WinTools\zd_pazq\T0002\export\forwardp\SH000002.txt'
    dl=read_last_lines(file_path)
    file=open(file_path,'r')
    # file.seek(0, 2)
    # print file.readline()
    lastchar = file.readline()[-1]
    trailing_newline = (lastchar == "\n")
    print trailing_newline,lastchar
    print dl
    