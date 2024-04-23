import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from loguru import logger
from tqdm import tqdm

from tensorrt_yolo import TRTYOLO, ImageBatcher, generate_labels_with_colors, visualize_detections

labels = r'E:\Projects\Cpp\TensorRT-YOLO\demo\detect\labels.txt'
engine = r'E:\Models\YOLOv8/yolov8s.engine'
labels = generate_labels_with_colors(labels)
source = 'E:/laugh/Downloads/coco128/images/train2017'
output = 'output'


detection = TRTYOLO(engine)
detection.warmup()

total_time = 0.0
total_infers = 0
total_images = 0
batcher = ImageBatcher(
    input_path=source, batch_size=detection.batch_size, imgsz=detection.imgsz, dtype=detection.dtype, dynamic=detection.dynamic
)
for batch, images, batch_shape in tqdm(batcher, total=len(batcher.batches), desc="Processing batches", unit="batch"):
    start_time_ns = time.perf_counter_ns()
    detections = detection.infer(batch, batch_shape)
    end_time_ns = time.perf_counter_ns()
    elapsed_time_ms = (end_time_ns - start_time_ns) / 1e6
    total_time += elapsed_time_ms
    total_images += len(images)
    total_infers += 1
    if output:
        output_dir = Path(output)
        output_dir.mkdir(parents=True, exist_ok=True)
        with ThreadPoolExecutor() as executor:
            args_list = [(str(image), str(output_dir / image.name), detections[i], labels) for i, image in enumerate(images)]
            executor.map(visualize_detections, *zip(*args_list))

average_latency = total_time / total_infers
average_throughput = total_images / (total_time / 1000)
logger.success(
    "Benchmark results include time for H2D and D2H memory copies\n"
    f"    CPU Average Latency: {average_latency:.3f} ms\n"
    f"    CPU Average Throughput: {average_throughput:.1f} ips\n"
    "    Finished Inference."
)
