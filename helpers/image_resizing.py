import logging
import multiprocessing
import os
import time

import PIL
from PIL import Image
from django.conf import settings

FORMAT = "[%(threadName)s, %(process)d, %(asctime)s, %(levelname)s] %(message)s"
logging.basicConfig(filename="logfile.log", level=logging.INFO, format=FORMAT)


class ThumbnailMakerService:
    def __init__(self, target_sizes=False):
        self.home_dir = os.path.join(settings.BASE_DIR, 'media')
        self.input_dir = os.path.join(self.home_dir)
        self.output_dir = os.path.join(self.home_dir, 'resized_images')
        self.img_queue = multiprocessing.JoinableQueue()
        self.target_sizes = target_sizes if target_sizes else [200]

    def perform_resize(self):
        os.makedirs(self.output_dir, exist_ok=True)

        logging.info("beginning image resizing")

        while True:
            filename = self.img_queue.get()

            if filename is not None:
                logging.info(f"resizing image {filename}")
                orig_img = Image.open(self.input_dir + os.path.sep + filename)

                for base_width in self.target_sizes:
                    img = orig_img
                    w_percent = (base_width / float(img.size[0]))
                    h_size = int((float(img.size[1]) * float(w_percent)))

                    img = img.resize((base_width, h_size), PIL.Image.LANCZOS)

                    new_filename = os.path.splitext(filename)[0] + '_' + str(base_width) + os.path.splitext(filename)[1]
                    out_filepath = self.output_dir + os.path.sep + new_filename
                    img.save(out_filepath)

                logging.info(f"done resizing image: {filename}")
                self.img_queue.task_done()
            else:
                self.img_queue.task_done()
                break

    def make_thumbnails(self, img_list):
        logging.info("START make_thumbnails")
        start = time.perf_counter()

        for img in img_list:
            self.img_queue.put(img)

        num_processes = multiprocessing.cpu_count()
        for _ in range(2):
            p = multiprocessing.Process(target=self.perform_resize)
            p.start()

        for _ in range(num_processes):
            self.img_queue.put(None)

        end = time.perf_counter()

        logging.info(f"END make_thumbnails in {end - start} seconds")