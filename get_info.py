import re
import urllib, urllib2


def get_ver(param):
    mod_pattern = re.compile(r'MODEL: Aruba(.*?)\)')
    ver_pattern =   re.compile(r'Version (.*?)\n')
    build_pattern = re.compile(r'build (.*?)\)')

    model = mod_pattern.findall(param)
    version = ver_pattern.findall(param)
    build   = build_pattern.findall(param)
    return model[0] if model else None,version[0] if version else None,build[0] if build else None


def check_build(param):
    pattern = re.compile(r'Partition.*?0:(\d).*?Default boot')
    default_boot = pattern.findall(param)

    partition =  default_boot[0]

    build_pattern = re.compile(r'Build number.*?(\d+)')
    build = build_pattern.findall(param)
    return build[int(partition)]


def get_image_str(model,build):
    if not model:
        return 'No model input'
    url="http://speedy.arubanetworks.com/cgi-bin/re/find_images.html?build="+str(build)
    try:
        req=urllib2.Request(url)
        resp = urllib2.urlopen(req)
    except urllib2.URLError,e:
        print "Page not found,reason:%s\n%s" %(e.reason,url)
        return None
    else:

        res = re.compile(
            '(ArubaOS_'+model+'.*?'+str(build)+')',
            )
        image = res.findall(resp.read())

        return image[0] if image else 'Build %s image not found'%str(build)


def get_latest_build(version):
    url = "http://speedy.arubanetworks.com/cgi-bin/re/build_info_mysql.html"

    para = {
        'codeline': version,
    }
    postData = urllib.urlencode(para)

    try:
        req = urllib2.Request(url,postData)
        resp = urllib2.urlopen(req)
    except  urllib2.URLError,e:
        print "Page not found,reason:%s\n%s " %(e.reason,url)
        return None
    else:
        print version
        res = re.compile('color="green">P</font>.*?\n'
                         '.*?re_'+version+'_(\d{5}).*?\n'
                         '.*?\n'
                         '.*?_opt</a>')

        total_item = res.findall(resp.read())
        return total_item[0] if total_item else None


