#coding=utf-8
import sys
import os
import time
import numpy as np


# Make sure that caffe is on the python path:
web_path = os.getcwd()
caffe_root = '/home/zjw/caffe-ssd/'  # this file is expected to be in {caffe_root}/examples      #####################
import os
os.chdir(caffe_root)
import sys
sys.path.insert(0, '/home/zjw/caffe-ssd/python')                                                 #####################
import caffe
caffe.set_device(0)
caffe.set_mode_gpu()

####################################################
####################################################
model_def = '/home/zjw/cnn-models-master/VGG19_cvgj/deploy.prototxt'                                        
model_weights = '/home/zjw/cnn-models-master/VGG19_cvgj/vgg19_cvgj_iter_1000.caffemodel'  #####################

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)

# input preprocessing: 'data' is the name of the input blob == net.inputs[0]
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2, 0, 1))
transformer.set_mean('data', np.array([104,117,123])) # mean pixel
transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
#transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

####################################################
image_resize = 224                                                                         #####################
net.blobs['data'].reshape(1,3,image_resize,image_resize)

#image = caffe.io.load_image('examples/images/fish-bike.jpg')           
#image = caffe.io.load_image('testdata/test.jpg')
def pred(imagepath):
    #imagepath = '/home/zjw/cnn-models-master/VGG19_cvgj/test/zdjy1.jpg'
    image = caffe.io.load_image(imagepath)                #####################
    #plt.imshow(image) 
    ####################################################
    transformed_image = transformer.preprocess('data', image)
    net.blobs['data'].data[...] = transformed_image

    # Forward pass.
    output = net.forward()
    output_prob = output['prob'][0]  # the output probability vector for the first image in the batch
    print(output_prob)
    labels=['youtanxiaofan','lajiduiji','renxingdaotingche','zhandaojingying']
    #print labels
    #print imagepath
    
    return np.array_str(output_prob,suppress_small=True)

def write_result(lines):
    with open(web_path + '/' +'r.io','w') as r:
        r.writelines(lines)

def main():
    cmds = []

    while True:
        with open(web_path + '/'+'p.io','r') as p:
            p_lines = p.readlines()
            r_lines = []
            cmd_id = p_lines[0]
            if cmd_id not in cmds:
                cmds.append(cmd_id)
                result = pred(web_path + '/' + 'lastest.jpg')
                r_lines.append(cmd_id)
                r_lines.append(result)
                print r_lines
                write_result(r_lines)
        time.sleep(0.2)
        


if __name__ == "__main__":
    main()
