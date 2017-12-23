from multiprocessing import Pool
import time,operate
from get_info import get_latest_build
if __name__ == '__main__':
    #edit the target_ver or edit build_number
    target_ver = 'FCS8.2.X.0'
    build_number = get_latest_build(target_ver)
    
    #build_number = 62657
    if not bld:
        print "build not found,please check t_ver;"
    else:
        print 'target build:'+str(bld)
    part = 0
    
    devs =['10.10.10.10','20.20.20.20']
    begin =time.time()

    pool = Pool()
    for dev in devs:
        print dev
        pool.apply_async(operate.upgrade,args=(dev,build_number,str(part)))

    pool.close()
    pool.join()
    print time.time()-begin
