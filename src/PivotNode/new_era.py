import serial

def hexShow(argv):        #十六进制显示 方法1
    try:
        result = ''  
        hLen = len(argv)  
        for i in range(hLen):  
         hvol = argv[i]
         hhex = '%02x'%hvol  
         result += hhex+' '  
        print('hexShow:',result)
    except:
        pass
    return result


def find_pumps(ser,tot_range=10):
    pumps = []
    cmd_raw = '%iADR\x0D'
    for i in range(tot_range):
        cmd = (cmd_raw%i).encode("raw_unicode_escape")
        ser.write(cmd)
        output = ser.readline().decode()
        if len(output)>0:
            pumps.append(i)
    return pumps

def run_all(ser):
    cmd_raw = '*RUN\x0D'
    cmd = cmd_raw.encode("raw_unicode_escape")
    ser.write(cmd)
    output = ser.readline().decode("raw_unicode_escape")
    if '?' in output: print(cmd_raw.strip()+' from run_all not understood')

def stop_all(ser):
    cmd_raw = '*STP\x0D'
    cmd = cmd_raw.encode("ascii")
    ser.write(cmd)
    output = ser.readline().decode("raw_unicode_escape")
    if '?' in output: print(cmd_raw.strip()+' from stop_all not understood')
    # print(type(output),output)

def stop_pump(ser,pump):
    cmd_raw = '%iSTP\x0D'%pump
    cmd = cmd_raw.encode("raw_unicode_escape")
    ser.write(cmd)
    output = ser.readline().decode("raw_unicode_escape")
    if '?' in output: print(cmd_raw.strip()+' from stop_pump not understood')

    cmd_raw = '%iRAT0UH\x0D'%pump
    cmd = cmd_raw.encode("raw_unicode_escape")
    ser.write(cmd)
    output = ser.readline().decode("raw_unicode_escape")
    if '?' in output: print(cmd_raw.strip()+' from stop_pump not understood')

def set_rates(ser,rate):
    cmd_raw = ''
    for pump in rate:
        flowrate = float(rate[pump])
        direction = 'INF'
        if flowrate<0: direction = 'WDR'
        frcmd_raw = '%iDIR%s\x0D'%(pump,direction)
        frcmd = frcmd_raw.encode("raw_unicode_escape")
        ser.write(frcmd)
        output = ser.readline().decode("raw_unicode_escape")
        if '?' in output: print(frcmd_raw.strip()+' from set_rate not understood')
        fr = abs(flowrate)
                
        if fr<5000:
            cmd_raw += str(pump)+'RAT'+str(fr)[:5]+'UH*'
        else:
            fr = fr/1000.0
            cmd_raw += str(pump)+'RAT'+str(fr)[:5]+'MH*'
    cmd_raw += '\x0D'
    cmd = cmd_raw.encode("raw_unicode_escape")
    ser.write(cmd)
    output = ser.readline().decode("raw_unicode_escape")
    if '?' in output: print(cmd.strip()+' from set_rates not understood')

def get_rate(ser,pump):
    #get direction
    cmd_raw = '%iDIR\x0D'%pump
    cmd = cmd_raw.encode("raw_unicode_escape")
    ser.write(cmd)
    output = ser.readline().decode("raw_unicode_escape")
    sign = ''
    if output[4:7]=='WDR':
        sign = '-'
    cmd_raw = '%iRAT\x0D'%pump
    cmd = cmd_raw.encode("raw_unicode_escape")
    ser.write(cmd)
    output = ser.readline().decode("raw_unicode_escape")
    if '?' in output: print(cmd_raw.strip()+' from get_rate not understood')
    units = output[-3:-1]
    if units=='MH':
        rate = str(float(output[4:-3])*1000)
    if units=='UH':
        rate = output[4:-3]
    return sign+rate

def get_rates(ser,pumps):
    rates = dict((p,get_rate(ser,p).split('.')[0]) for p in pumps)
    return rates

def set_diameter(ser,pump,dia):
    cmd_raw = '%iDIA%s\x0D'%(pump,dia)
    cmd = cmd_raw.encode("raw_unicode_escape")
    ser.write(cmd)
    output = ser.readline().decode("raw_unicode_escape")
    if '?' in output: print(cmd_raw.strip()+' from set_diameter not understood')

    
def get_diameter(ser,pump):
    cmd_raw = '%iDIA\x0D'%pump
    cmd = cmd_raw.encode("raw_unicode_escape")
    ser.write(cmd)
    output = ser.readline().decode("raw_unicode_escape")
    if '?' in output: print(cmd_raw.strip()+' from get_diameter not understood')
    dia = output[4:-1]
    return dia

def prime(ser,pump):
    # set infuse direction
    cmd_raw = '%iDIRINF\x0D'%pump
    cmd = cmd_raw.encode("raw_unicode_escape")
    ser.write(cmd)
    output = ser.readline().decode("raw_unicode_escape")
    if '?' in output: print(cmd_raw.strip()+' from prime not understood')

    # set rate
    cmd_raw = '%iRAT10.0MH\x0D'%pump
    cmd = cmd_raw.encode("raw_unicode_escape")
    ser.write(cmd)
    output = ser.readline().decode("raw_unicode_escape")
    if '?' in output: print(cmd_raw.strip()+' from prime not understood')

    # run
    cmd_raw = '%iRUN\x0D'%pump
    cmd = cmd_raw.encode("raw_unicode_escape")
    ser.write(cmd)
    output = ser.readline().decode("raw_unicode_escape")
    if '?' in output: print(cmd.strip()+' from prime not understood')





#ser = serial.Serial('COM3',19200)
#print ser.name       # check which port was really used
#print ser.isOpen()
#ser.close()
#pumps = find_pumps(ser)
#rates = get_rates(ser,pumps)
