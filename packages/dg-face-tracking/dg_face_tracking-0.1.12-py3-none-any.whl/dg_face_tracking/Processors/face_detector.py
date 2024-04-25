import sys, os
import logging as log
import threading
import multiprocessing
from queue import Queue, Empty as EmptyQueue
import cv2
import numpy as np
import math

from typing import Optional, Union

import degirum as dg
import degirum_tools
import time

from pathlib import Path
Path(__file__).resolve()

# import mytools
from ..config_rt import ConfigRT

from ..Data.frame_data import FrameData
from ..Data.face_data import FaceData

from ..utils.rotate import normalize_landmarks, get_face_img

default_config = {
    'show_face': False,
    'face_crop_aspect_ratio': 0.0,
    'face_margin': 0.0,
    'single_face': False,
    'normalize_face': False,
    'model': {
        'deployment': "cloud",
        'cloud_url': "https://cs.degirum.com/degirum/MehrdadTest",
        'model': "mobilenet_face_recognition--112x112_float_openvino_cpu_2",
        'input_image_format': "RAW",
        'input_numpy_colorspace': "BGR",
    }
}


class FaceDetector(threading.Thread):
    def __init__(self, proc_id: str = "face_detector",
                 config_name: str = "FaceDetector",
                 q_in: Union[Queue, multiprocessing.Queue] = None,
                 runs_event:  Union[threading.Event, multiprocessing.Event] = None):
        self.proc_id = proc_id
        self.q_in = Queue() if q_in is None else q_in
        self.q_out_map: dict = {}

        self.start_time = -1
        self.n_data = 0

        self.stop_event = threading.Event()
        self.runs_event = threading.Event() if runs_event is None else runs_event

        self.results_thread = threading.Thread(target=self.process_results, args=())
        self.result_queue = Queue()

        self.model = None
        self.model_cfg: dict = {}

        self.show_face = True
        self.face_crop_aspect_ratio = 0.0
        self.face_margin = 0.0
        self.normalize_face = False
        self.single_face = False

        self.n_try = 5

        # Starting real-time config tracking service
        self.config = ConfigRT(config_name)
        try:
            self.apply_config()
        except Exception as e:
            self.config.stop()
            raise e

        super(FaceDetector, self).__init__()

    def stop(self):
        self.config.stop()
        self.stop_event.set()
        self.results_thread.join()
        self.config.join()

    def is_stopped(self) -> bool:
        """
        Check if the service is stopped
        :return: bool
        """
        return self.stop_event.is_set()

    def wait2run(self, timeout=None):
        return self.runs_event.wait(timeout)

    def add_q_out(self, destination, q_out):
        self.q_out_map[destination] = q_out

    def start(self) -> None:
        self.results_thread.start()
        super(FaceDetector, self).start()

    def get_id(self):
        return self.proc_id

    def apply_config(self):
        if not self.config.is_modified():
            return
        self.show_face = self.config.get('show_face', default_config['show_face'])
        self.face_crop_aspect_ratio = self.config.get('face_crop_aspect_ratio', default_config['face_crop_aspect_ratio'])
        self.face_margin = self.config.get('face_margin', default_config['face_margin'])
        self.single_face = self.config.get('single_face', default_config['single_face'])
        self.normalize_face = self.config.get('normalize_face', default_config['normalize_face'])
        try:
            model_cfg = self.config.get('model', default_config['model'])
            if model_cfg != self.model_cfg:
                cloud_token = degirum_tools.get_token()
                deployment = model_cfg['deployment']
                if deployment == "cloud":
                    deployment = dg.CLOUD
                elif deployment == "local":
                    deployment = dg.LOCAL
                cloud_url = model_cfg['cloud_url']
                model_name = model_cfg['model']
                zoo = dg.connect(deployment, cloud_url, cloud_token)
                model = zoo.load_model(model_name)
                model.input_image_format = model_cfg['input_image_format']
                model.input_numpy_colorspace = model_cfg['input_numpy_colorspace']
                # model.measure_time = True
                self.model = model
                self.model_cfg = model_cfg

                # dg.enable_default_logger().setStream(open("trace.txt", "w"))

                print(f"FaceDetector: Applied config for {self.model} model.")
        except Exception as e:
            print("FaceDetector: apply_config: " + str(e))
            raise e

    def put2q(self, data):
        for q_out in self.q_out_map.values():
            try:
                q_out.put_nowait(data)
            except Exception as e:
                print("FaceDetector: result_process: failed to put in q_out" + str(e))

    def run(self):
        self.runs_event.set()
        n_res = 0

        for res in self.model.predict_batch(self.data_source()):
            n_res += 1
            elapsed = time.time() - self.start_time
            if n_res % 10 == 0:
                print(f"Processed: {n_res}; Throughput: {n_res / elapsed:.1f} frames/sec")
            self.result_queue.put(res)
            if self.stop_event.is_set():
                break

        print("FaceDetector: run: sending poison pill")
        self.result_queue.put_nowait(None)

        # Stop result_process thread
        spent_time = time.time() - self.start_time
        #print(self.model.time_stats())
        #self.model.reset_time_stats()
        print(f"FaceDetector: Total frames: {self.n_data}; Throughput: {self.n_data / spent_time:.1f} frames/sec")
        self.result_queue.put(None)
        self.results_thread.join()
        self.config.stop()
        self.config.join()
        print("FaceDetector: exiting")

    def test_data_source(self):
        frame_img = cv2.imread("C:/Datasets/lfw/Aaron_Eckhart/Aaron_Eckhart_0001.jpg")
        self.start_time = time.time()
        for _ in range(10000):
            self.n_data += 1
            yield frame_img
            #time.sleep(0.001)

    def data_source(self):
        while not self.is_stopped():
            #self.apply_config()
            try:
                data = self.q_in.get(timeout=0.1)
                self.n_data += 1
                if self.start_time < 0:
                    self.start_time = time.time()
            except:
                continue

            if data is None:
                # yield None, None
                print("FaceDetector: Got poison pill")
                break
            if isinstance(data, FrameData):
                frame_img = data.get_source_image()
                # frame_img = cv2.imread("C:/Datasets/lfw/Aaron_Eckhart/Aaron_Eckhart_0001.jpg")
                # print("Yielding...")
                yield frame_img, data
                time.sleep(0.001)

    def process_results(self):
        win_capt = "Faces"
        n_processed = 0
        while not self.is_stopped():
            try:
                result = self.result_queue.get()
            except:
                continue
            if result is None:
                print("FaceDetector: Send poison pill")
                self.put2q(None)
                break
            if len(result.results) == 0 or 'bbox' not in result.results[0]:
                continue

            n_processed += 1
            elapsed = time.time() - self.start_time
            #print(f"FaceDetector: process_results: {n_processed}; Results Q size: {self.result_queue.qsize()};  {n_processed / elapsed:.1f} per sec")

            results = result.results

            if self.single_face and len(result.results) > 1:
                best_result = result.results[0]
                bbox = best_result['bbox']
                best_box_area = abs(bbox[0] - bbox[2])*abs(bbox[1] - bbox[3])
                for i in range(1, len(result.results)):
                    res = result.results[i]
                    bbox = res['bbox']
                    box_area = abs(bbox[0] - bbox[2]) * abs(bbox[1] - bbox[3])
                    if box_area > best_box_area:
                        best_result = res
                        best_box_area = box_area
                results = [best_result]

            for res in results:
                if 'bbox' not in res:
                    print("FaceDetector: process_results: bbox is missing in results")
                    continue
                bbox = res['bbox']
                landmarks = res['landmarks'] if 'landmarks' in res else None
                frame_data = result.info
                if isinstance(frame_data, FrameData):
                    face_data = FaceData()
                    face_data.from_data(frame_data)

                    face_data.set_bbox(bbox)
                    if landmarks is not None:
                        face_data.set_landmarks(landmarks)
                    face_img, face_img0 = get_face_img(result.image,
                                                       face_data.get_bbox(),
                                                       face_data.get_landmarks(),
                                                       aspect=self.face_crop_aspect_ratio,
                                                       margin=self.face_margin,
                                                       use_normalization=self.normalize_face)

                    if self.show_face and face_img is not None:
                        h0, w0 = face_img0.shape[:2]
                        h, w = face_img.shape[:2]
                        img = face_img
                        img0 = face_img0
                        if h > h0:
                            img0 = cv2.copyMakeBorder(img0, top=0, bottom=(h-h0), left=0, right=0, borderType=cv2.BORDER_CONSTANT)
                        elif h0 > h:
                            img  = cv2.copyMakeBorder(img,  top=0, bottom=(h0-h), left=0, right=0, borderType=cv2.BORDER_CONSTANT)
                        if w > w0:
                            img0 = cv2.copyMakeBorder(img0, top=0, bottom=0, left=0, right=(w-w0), borderType=cv2.BORDER_CONSTANT)
                        elif w0 > w:
                            img  = cv2.copyMakeBorder(img,  top=0, bottom=0, left=0, right=(w0-w), borderType=cv2.BORDER_CONSTANT)
                        img = np.concatenate((img0, img), axis=1)
                        cv2.imshow(win_capt, img)
                        cv2.waitKey(1)
                        time.sleep(1)

                    face_data.set_face_image(face_img)
                    self.put2q(face_data)
                    time.sleep(0.001)
        # end of while
        return

