#-*- coding=utf8-*-
from ssh_device import Paramiko_cient
import get_info
from get_info import get_image_str
import time
def upgrade(device,target_build,partition=0):
    client = Paramiko_cient(device, 'config.ini')
    target_build = str(target_build)
    status = client.connect()
    if str(status) == "timed out":
        print "%s connection time out"%device
    result = client.run('show version')
    model, version, build = get_info.get_ver(result)
    result = client.run('show image version')
    boot_build = get_info.check_build(result)
    print '%s model:%s,version:%s,build:%s,boot build:%s'%(device,model, version, build, boot_build)

    if model == 'MC-VA-US':
        dev_model = 'VMC'
    elif model == 'MM-VA':
        dev_model = 'MM'
    else:
        dev_model = str(int(model) / 100) + "xx"


    if target_build == boot_build:
        print "%s boot version is %s,no need to upgrade" % (device,target_build)

    else:
        img = get_image_str(dev_model,target_build)
        upgrade_cmd = 'copy ftp: 10.1.1.41 anonymous %s system: partition %s' % (
        img, partition)

        result = client.run_cmd(upgrade_cmd)

        result = client.run('show image version')
        build = get_info.check_build(result)
        print build,target_build
        if build == target_build:
            print "%s download success"%device
        else:
            print "%s download failed"%device

    client.close()




