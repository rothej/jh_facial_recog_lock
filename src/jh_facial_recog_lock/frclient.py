# Code derived from luxonis/depthai-experiments, modifications are noted as "custom"
import os
import argparse
import blobconverter
import cv2
import depthai as dai
import numpy as np
from MultiMsgSync import TwoStageHostSeqSync
import RPi.GPIO as GPIO         # custom
from time import sleep          # custom
import zmq                      # custom
import signal                   # custom
from datetime import datetime   # custom
import sys                      # custom

RELAY_PIN = 11                  # custom, will manipulate pin 11, GPIO17

GPIO.setmode(GPIO.BOARD)        # custom, sets Rpi pin numbering scheme to follow headers on J8
GPIO.setup(RELAY_PIN, GPIO.OUT) # custom, sets GPIO pin to out
GPIO.output(RELAY_PIN, 0)       # custom, start locked

parser = argparse.ArgumentParser()
parser.add_argument("-name", "--name", type=str, help="Name of the person for database saving")

args = parser.parse_args()

context = zmq.Context()                     # custom
pushSocket = context.socket(zmq.PUSH)       # custom
pushSocket.bind("tcp://127.0.0.1:55002")    # custom - modify if add'l client
pullSocket = context.socket(zmq.PULL)       # custom
pullSocket.bind("tcp://127.0.0.1:55001")    # custom

## Handle SIGINT for exiting program and unbinding sockets. # custom 
def exitHandler(sig, frame):                                # custom
    print("Unbinding ports and exiting . . .")              # custom
    pushSocket.unbind("tcp://127.0.0.1:55001")              # custom
    pullSocket.unbind("tcp://127.0.0.1:55002")              # custom
    sys.exit(0)                                             # custom
                                                            # custom
signal.signal(signal.SIGINT, signal.default_int_handler)    # custom
## End SIGINT handler.                                      # custom

def frame_norm(frame, bbox):
    normVals = np.full(len(bbox), frame.shape[0])
    normVals[::2] = frame.shape[1]
    return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)

VIDEO_SIZE = (1072, 1072)
databases = "databases"
if not os.path.exists(databases):
    os.mkdir(databases)

class TextHelper:
    def __init__(self) -> None:
        self.bg_color = (0, 0, 0)
        self.color = (255, 255, 255)
        self.text_type = cv2.FONT_HERSHEY_SIMPLEX
        self.line_type = cv2.LINE_AA
    def putText(self, frame, text, coords):
        cv2.putText(frame, text, coords, self.text_type, 1.0, self.bg_color, 4, self.line_type)
        cv2.putText(frame, text, coords, self.text_type, 1.0, self.color, 2, self.line_type)

class FaceRecognition:
    def __init__(self, db_path, name) -> None:
        self.read_db(db_path)
        self.name = name
        self.bg_color = (0, 0, 0)
        self.color = (255, 255, 255)
        self.text_type = cv2.FONT_HERSHEY_SIMPLEX
        self.line_type = cv2.LINE_AA
        self.printed = True
        self.unlock_counter = 0 # custom
        self.alert_counter = 0  # custom

    def cosine_distance(self, a, b):
        if a.shape != b.shape:
            raise RuntimeError("array {} shape not match {}".format(a.shape, b.shape))
        a_norm = np.linalg.norm(a)
        b_norm = np.linalg.norm(b)
        return np.dot(a, b.T) / (a_norm * b_norm)

    def new_recognition(self, results):
        conf = []
        max_ = 0
        label_ = None
        for label in list(self.labels):
            for j in self.db_dic.get(label):
                conf_ = self.cosine_distance(j, results)
                if conf_ > max_:
                    max_ = conf_
                    label_ = label

        conf.append((max_, label_))
        name = conf[0] if conf[0][0] >= 0.5 else (1 - conf[0][0], "UNKNOWN")
        # self.putText(frame, f"name:{name[1]}", (coords[0], coords[1] - 35))
        # self.putText(frame, f"conf:{name[0] * 100:.2f}%", (coords[0], coords[1] - 10))

        if name[1] == "UNKNOWN":
            self.create_db(results)
            self.unlock_counter = 0                                                                     # custom
            self.alert_counter = self.alert_counter + 1                                                 # custom
        else:                                                                                           # custom
            self.unlock_counter = self.unlock_counter + 1                                               # custom
            self.alert_counter = 0                                                                      # custom
        if self.unlock_counter == 7:                                                                    # custom
            print("Unlocking.")                                                                         # custom
            GPIO.output(RELAY_PIN, 1)                                                                   # custom
            self.unlock_counter = self.unlock_counter + 1                                               # custom
            GPIO.output(RELAY_PIN, 0)                                                                   # custom
        if self.unlock_counter == 17:                                                                   # custom
            print("Access complete, locking.")                                                          # custom
            GPIO.output(RELAY_PIN, 0)                                                                   # custom
            self.unlock_counter = 0                                                                     # custom
        if self.alert_counter == 7:                                                                     # custom
            print("Locking.")                                                                           # custom
            GPIO.output(RELAY_PIN, 0)                                                                   # custom
            try:                                                                                        # custom
                self.current_datetime = str(datetime.now())                                             # custom
                self.msg_string = 'Unauthorized entry attempt detected at %s' % (self.current_datetime) # custom
                pushSocket.send_string(self.msg_string, zmq.NOBLOCK)                                    # custom
                self.alert_counter = 0                                                                  # custom
            except:                                                                                     # custom
                print("Alert message to server failed to send.")                                        # custom
            else:                                                                                       # custom
                print("Alert message to server sent successfully.")                                     # custom
        return name

    def read_db(self, databases_path):
        self.labels = []
        for file in os.listdir(databases_path):
            filename = os.path.splitext(file)
            if filename[1] == ".npz":
                self.labels.append(filename[0])

        self.db_dic = {}
        for label in self.labels:
            with np.load(f"{databases_path}/{label}.npz") as db:
                self.db_dic[label] = [db[j] for j in db.files]

    def putText(self, frame, text, coords):
        cv2.putText(frame, text, coords, self.text_type, 1, self.bg_color, 4, self.line_type)
        cv2.putText(frame, text, coords, self.text_type, 1, self.color, 1, self.line_type)

    def create_db(self, results):
        if self.name is None:
            if not self.printed:
                print("Wanted to create new DB for this face, but --name wasn't specified")
                self.printed = True
            return
        print('Saving face...')
        try:
            with np.load(f"{databases}/{self.name}.npz") as db:
                db_ = [db[j] for j in db.files][:]
        except Exception as e:
            db_ = []
        db_.append(np.array(results))
        np.savez_compressed(f"{databases}/{self.name}", *db_)
        self.adding_new = False

print("Creating pipeline...")
pipeline = dai.Pipeline()

print("Creating Color Camera...")
cam = pipeline.create(dai.node.ColorCamera)
# For ImageManip rotate you need input frame of multiple of 16
cam.setPreviewSize(1072, 1072)
cam.setVideoSize(VIDEO_SIZE)
cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
cam.setInterleaved(False)
cam.setBoardSocket(dai.CameraBoardSocket.RGB)

host_face_out = pipeline.create(dai.node.XLinkOut)
host_face_out.setStreamName('color')
cam.video.link(host_face_out.input)

# ImageManip as a workaround to have more frames in the pool.
# cam.preview can only have 4 frames in the pool before it will
# wait (freeze). Copying frames and setting ImageManip pool size to
# higher number will fix this issue.
copy_manip = pipeline.create(dai.node.ImageManip)
cam.preview.link(copy_manip.inputImage)
copy_manip.setNumFramesPool(20)
copy_manip.setMaxOutputFrameSize(1072*1072*3)

# ImageManip that will crop the frame before sending it to the Face detection NN node
face_det_manip = pipeline.create(dai.node.ImageManip)
face_det_manip.initialConfig.setResize(300, 300)
copy_manip.out.link(face_det_manip.inputImage)

# NeuralNetwork
print("Creating Face Detection Neural Network...")
face_det_nn = pipeline.create(dai.node.MobileNetDetectionNetwork)
face_det_nn.setConfidenceThreshold(0.5)
face_det_nn.setBlobPath(blobconverter.from_zoo(name="face-detection-retail-0004", shaves=6))
# Link Face ImageManip -> Face detection NN node
face_det_manip.out.link(face_det_nn.input)

face_det_xout = pipeline.create(dai.node.XLinkOut)
face_det_xout.setStreamName("detection")
face_det_nn.out.link(face_det_xout.input)

# Script node will take the output from the face detection NN as an input and set ImageManipConfig
# to the 'age_gender_manip' to crop the initial frame
script = pipeline.create(dai.node.Script)
script.setProcessor(dai.ProcessorType.LEON_CSS)

face_det_nn.out.link(script.inputs['face_det_in'])
# We also interested in sequence number for syncing
face_det_nn.passthrough.link(script.inputs['face_pass'])

copy_manip.out.link(script.inputs['preview'])

with open("script.py", "r") as f:
    script.setScript(f.read())

print("Creating Head pose estimation NN")

headpose_manip = pipeline.create(dai.node.ImageManip)
headpose_manip.initialConfig.setResize(60, 60)
headpose_manip.setWaitForConfigInput(True)
script.outputs['manip_cfg'].link(headpose_manip.inputConfig)
script.outputs['manip_img'].link(headpose_manip.inputImage)

headpose_nn = pipeline.create(dai.node.NeuralNetwork)
headpose_nn.setBlobPath(blobconverter.from_zoo(name="head-pose-estimation-adas-0001", shaves=6))
headpose_manip.out.link(headpose_nn.input)

headpose_nn.out.link(script.inputs['headpose_in'])
headpose_nn.passthrough.link(script.inputs['headpose_pass'])

print("Creating face recognition ImageManip/NN")

face_rec_manip = pipeline.create(dai.node.ImageManip)
face_rec_manip.initialConfig.setResize(112, 112)
face_rec_manip.inputConfig.setWaitForMessage(True)

script.outputs['manip2_cfg'].link(face_rec_manip.inputConfig)
script.outputs['manip2_img'].link(face_rec_manip.inputImage)

face_rec_nn = pipeline.create(dai.node.NeuralNetwork)
face_rec_nn.setBlobPath(blobconverter.from_zoo(name="face-recognition-arcface-112x112", zoo_type="depthai", shaves=6))
face_rec_manip.out.link(face_rec_nn.input)

arc_xout = pipeline.create(dai.node.XLinkOut)
arc_xout.setStreamName('recognition')
face_rec_nn.out.link(arc_xout.input)


with dai.Device(pipeline) as device:
    facerec = FaceRecognition(databases, args.name)
    sync = TwoStageHostSeqSync()
    text = TextHelper()

    queues = {}
    # Create output queues
    for name in ["color", "detection", "recognition"]:
        queues[name] = device.getOutputQueue(name)

    while True:
        for name, q in queues.items():
            # Add all msgs (color frames, object detections and face recognitions) to the Sync class.
            if q.has():
                sync.add_msg(q.get(), name)

        msgs = sync.get_msgs()
        if msgs is not None:
            frame = msgs["color"].getCvFrame()
            dets = msgs["detection"].detections

            for i, detection in enumerate(dets):
                bbox = frame_norm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (10, 245, 10), 2)

                features = np.array(msgs["recognition"][i].getFirstLayerFp16())
                conf, name = facerec.new_recognition(features)
                text.putText(frame, f"{name} {(100*conf):.0f}%", (bbox[0] + 10,bbox[1] + 35))

            cv2.imshow("color", cv2.resize(frame, (800,800)))

        if cv2.waitKey(1) == ord('q'):
            break