import numpy as np
import time
import random as rd
import hug
import os
cmd_cur_id = rd.randint(9,999999)
api = hug.get(on_invalid=hug.redirect.not_found)
html = hug.get(output=hug.output_format.html)

suffix_output = hug.output_format.suffix({
    '.js': hug.output_format.text,
    '.html':hug.output_format.html,
    '.css':hug.output_format.file,
    '.png':hug.output_format.png_image,
    '.gif':hug.output_format.file
    })


def set_p(pid):
    with open('p.io','w') as p:
        p.write(str(pid))
        p.write('\n')

def get_r(cid):
    result_a = None
    with open('r.io','r') as r:
        lines = r.readlines()
        print(lines)
        cmd_id = lines[0][:-1]
        print(cmd_id)
        if cid == cmd_id:
            raw_result = lines[1][:-1]
            result = raw_result[1:-1].split('  ')
            ai = []
            for rs in result:
                ai.append(float(rs))
            result_a = np.array(ai)
            print(result_a)
    return result_a

@hug.get()
def predict():
    global cmd_cur_id
    cls_dict = {
            0 : '游摊小贩',
            1 : '垃圾堆积',
            2 : '车占人行道',
            3 : '餐饮占道'

            }
    cmd_cur_id = cmd_cur_id + 1
    set_p(cmd_cur_id)
    print('\n cur_id:' + str(cmd_cur_id))
    while True:
        result = get_r(str(cmd_cur_id))
        print (result)
        if result is not None :
            print(result)
            break
        time.sleep(1)

    cls = np.argmax(result)


    return {'r':cls_dict.get(cls) } 


@hug.static('/web')
def web():
    return ('./',)


@hug.post('/upload')
def upload_file(body):
    """accepts file uploads"""
    # <body> is a simple dictionary of {filename: b'content'}
    content = list(body.values()).pop()
    filesize = len(content)
    print('file size that uploadded is : ', filesize)
    with open('lastest.jpg','wb') as f:
        f.write(content)
    return {'filename': 'lastest.jpg', 'filesize': filesize}
