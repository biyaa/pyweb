import numpy as np
import glob as glob

# Make sure that caffe is on the python path:
caffe_root = '/home/zjw/caffe-ssd/'  # this file is expected to be in {caffe_root}/examples      #####################
import os
os.chdir(caffe_root)
import sys
sys.path.insert(0, '/home/zjw/caffe-ssd/python')                                                 #####################
import caffe
caffe.set_device(0)
caffe.set_mode_gpu()

####################################################
from google.protobuf import text_format
from caffe.proto import caffe_pb2
# load PASCAL VOC labels
labelmap_file = 'data/coco/labelmap_coco.prototxt'
file = open(labelmap_file, 'r')
labelmap = caffe_pb2.LabelMap()
text_format.Merge(str(file.read()), labelmap)

def get_labelname(labelmap, labels):
    num_labels = len(labelmap.item)
    labelnames = []
    if type(labels) is not list:
        labels = [labels]
    for label in labels:
        found = False
        for i in xrange(0, num_labels):
            if label == labelmap.item[i].label:
                found = True
                labelnames.append(labelmap.item[i].display_name)
                break
        assert found == True
    return labelnames

####################################################
model_def = 'models/VGGNet/coco/SSD_512x512/deploy.prototxt'                                  #####################
model_weights = 'models/VGGNet/coco/SSD_512x512/VGG_coco_SSD_512x512_iter_360000.caffemodel'  #####################


net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)

# input preprocessing: 'data' is the name of the input blob == net.inputs[0]
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2, 0, 1))
transformer.set_mean('data', np.array([104,117,123])) # mean pixel
transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

####################################################
image_resize = 512                                                                            #####################
net.blobs['data'].reshape(1,3,image_resize,image_resize)

#image = caffe.io.load_image('examples/images/fish-bike.jpg')           
#image = caffe.io.load_image('testdata/test.jpg')

def ProcAPicture(filepath):
    image = caffe.io.load_image(filepath)                    #####################
    
    ####################################################
    transformed_image = transformer.preprocess('data', image)
    net.blobs['data'].data[...] = transformed_image
    
    # Forward pass.
    detections = net.forward()['detection_out']
    
    # Parse the outputs.
    det_label = detections[0,0,:,1]
    det_conf = detections[0,0,:,2]
    det_xmin = detections[0,0,:,3]
    det_ymin = detections[0,0,:,4]
    det_xmax = detections[0,0,:,5]
    det_ymax = detections[0,0,:,6]
    
    # Get detections with confidence higher than 0.1.
    top_indices = [i for i, conf in enumerate(det_conf) if conf >= 0.11]                                  #####################
    
    top_conf = det_conf[top_indices]
    top_label_indices = det_label[top_indices].tolist()
    top_labels = get_labelname(labelmap, top_label_indices)
    top_xmin = det_xmin[top_indices]
    top_ymin = det_ymin[top_indices]
    top_xmax = det_xmax[top_indices]
    top_ymax = det_ymax[top_indices]
    ####################################################
    '''
    umbrella chair
    table
    chair >= 6
    '''
    #limistprint = {"umbrella":0.1,"chair":0.1,"dining table":0.1}
    limistprint = {"umbrella":0,"chair":0,"dining table":0}
    for i in xrange(top_conf.shape[0]):
        label_name = top_labels[i]
        if label_name in limistprint:
            limistprint[label_name]=limistprint[label_name]+1
    if limistprint["dining table"] > 0 or limistprint["chair"] >=5 or (limistprint["chair"] > 0 and limistprint["umbrella"]):
        return 1
    else:
        return 0

dirpath = sys.argv[1]

if __name__ == '__main__':


 
def write_result(lines):
    with open(web_path + '/' +'r.io','w') as r:
        r.writelines(lines)
        
def format_result(r):
    result =  = np.zeros(5)
    if r == 1:
        np.put(result,4,1)
    else:
        np.put(result,5,1)
       
    return result

def main():
    cmds = []

    while True:
        with open(web_path + '/'+'p.io','r') as p:
            p_lines = p.readlines()
            r_lines = []
            cmd_id = p_lines[0]
            if cmd_id not in cmds:
                cmds.append(cmd_id)
                result = ProcAPicture(web_path + '/' + 'lastest.jpg')
                result = format_result(result)
                print ("check "+str(result))
                r_lines.append(cmd_id)
                r_lines.append(result)
                print r_lines
                write_result(r_lines)
        time.sleep(0.2)
        


if __name__ == "__main__":
    main()