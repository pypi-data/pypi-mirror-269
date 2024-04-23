
from DXR_BJ import drawer

import cv2
import time
draw=drawer.Drawer()
img=cv2.imread('1.jpg')
res={'10': {'error': False, 'bFlag': True, 'bState': True, 'sType': 'IRPerson', 'cnType': '热成像行人检测', 'sValue': '1', 'lResults': {'rect': [[0.4, 0.001851851851851852, 0.515625, 0.9944444444444445, 0.557663]], 'track': [], 'region': [], 'line': [], 'point': [], 'text': [['person']], 'sValue': '1', 'res_key': 'rect'}}, '17': {'error': False, 'bFlag': True, 'bState': False, 'sType': 'HKIR', 'cnType': '温度监控', 'sValue': '0', 'lResults': {'rect': [], 'track': [], 'region': [], 'line': [], 'point': [], 'text': [], 'sValue': '', 'res_key': 'rect'}}}

while True:
    num=0
    for key, value in res.items():
        outmessage=value
        t1=time.time()
        outframe,_= draw.draw_frame_box(img, outmessage)
        if num != 0:
            frame = outframe.copy()   ##多算法标记类兼容
        print(f'标记时间:{1000*(time.time()-t1)}')
        # cv2.imshow('1',outframe)
        # cv2.waitKey(10) 
        num=num+1