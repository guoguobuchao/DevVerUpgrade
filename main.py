from multiprocessing import Pool
import time,operate
from get_info import get_latest_build
if __name__ == '__main__':
    t_ver = 'FCS8.2.X.0'
    bld = get_latest_build(t_ver)
    #bld = 62657
    if not bld:
        print "build not found,please check t_ver;"
    else:
        print 'target build:'+str(bld)
    part = 0
    devices =['10.65.255.115','10.65.255.116','10.65.255.114','10.65.5.225']
    devs =['10.65.5.227','10.65.255.118']
    begin =time.time()

    pool = Pool()
    for dev in devices:
        print dev
        pool.apply_async(operate.upgrade,args=(dev,bld,str(part)))

    pool.close()
    pool.join()
    print time.time()-begin