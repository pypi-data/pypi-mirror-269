English detection example

<!-- 
### <div align="center">安装</div>

```bash
pip install -U tensorrt_yolo
```

```bash
git clone https://github.com/laugh12321/TensorRT-YOLO  # clone
cd TensorRT-YOLO
xmake f -k shared --tensorrt="C:/Program Files/NVIDIA GPU Computing Toolkit/TensorRT/v8.6.1.6"
# xmake f -k static --tensorrt="C:/Program Files/NVIDIA GPU Computing Toolkit/TensorRT/v8.6.1.6"
```

### <div align="center">模型导出</div>

使用下面的命令将导出 ONNX 模型并添加 [EfficientNMS](https://github.com/NVIDIA/TensorRT/tree/main/plugin/efficientNMSPlugin) 插件进行后处理。

**注意：** 导出 PP-YOLOE 与 PP-YOLOE+ 的 ONNX 模型，只会对 `batch` 维度进行修改，`height` 与 `width` 维度无法被更改，需要在[PaddleDetection](https://github.com/PaddlePaddle/PaddleDetection)中设置，默认为 `640`。

```bash
# yolov5 use local repository
trtyolo export -w yolov5s.pt -v yolov5 -o output --repo_dir your_local_yolovs_repository
# yolov8
trtyolo export -w yolov8s.pt -v yolov8 -o output
# yolov9 dynamic batch use github repository
trtyolo export -w yolov9-c.pt -v yolov9 -b -1 -o output
# PP-YOLOE, PP-YOLOE+
trtyolo export --model_dir modeldir --model_filename model.pdmodel --params_filename model.pdiparams -o output
```

生成的 ONNX 模型使用 `trtexec` 工具导出 TensorRT 模型。

```bash
# Static
trtexec --onnx=model.onnx --saveEngine=model.engine --fp16
# Dynamic
trtexec --onnx=model.onnx --saveEngine=model.engine --minShapes=images:1x3x640x640 --optShapes=images:4x3x640x640 --maxShapes=images:8x3x640x640 --fp16
```

### <div align="center">[PTQ INT8量化](tools/README.md)</div>

### <div align="center">[推理示例](demo/detect/README.md)</div> -->