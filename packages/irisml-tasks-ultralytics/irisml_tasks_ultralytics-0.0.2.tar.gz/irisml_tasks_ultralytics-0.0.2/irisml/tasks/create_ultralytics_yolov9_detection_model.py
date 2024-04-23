import dataclasses
import logging
import typing
import torch
from ultralytics.cfg import IterableSimpleNamespace
from ultralytics.nn.tasks import DetectionModel
import ultralytics.utils.ops
from ultralytics.utils import DEFAULT_CFG_DICT
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Create a Yolo Detection model using Ultralytics library.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Config:
        model_name: typing.Literal['yolov9c', 'yolov9e']
        num_classes: int

    @dataclasses.dataclass
    class Outputs:
        model: torch.nn.Module

    def execute(self, inputs):
        logger.info(f"Creating YOLOv9 detection model. name={self.config.model_name}, num_classes={self.config.num_classes}")
        yolo_model = DetectionModel(self.config.model_name + '.yaml', nc=self.config.num_classes)
        yolo_model.nc = self.config.num_classes
        yolo_model.names = {i: f'class_{i}' for i in range(self.config.num_classes)}
        yolo_cfg = IterableSimpleNamespace(**DEFAULT_CFG_DICT)
        yolo_cfg.nc = self.config.num_classes
        yolo_model.args = yolo_cfg
        return self.Outputs(model=YoloV9DetectionModel(yolo_model))


class YoloV9DetectionModel(torch.nn.Module):
    def __init__(self, yolo_model):
        super().__init__()
        self._model = yolo_model

    def predict(self, image):
        return self.model(image)

    def training_step(self, inputs, targets):
        batch_index = torch.cat([torch.full((len(t), 1), i, device=inputs.device) for i, t in enumerate(targets)], dim=0,)
        cls = torch.cat([t[:, 0] for t in targets], dim=0)
        bboxes = torch.cat([t[:, 1:] for t in targets], dim=0)

        # convert bbox from (x1, y1, x2, y2) to (center_x, center_y, width, height)
        widths = bboxes[:, 2] - bboxes[:, 0]
        heights = bboxes[:, 3] - bboxes[:, 1]
        bboxes[:, 0] = (bboxes[:, 0] + bboxes[:, 2]) / 2
        bboxes[:, 1] = (bboxes[:, 1] + bboxes[:, 3]) / 2
        bboxes[:, 2] = widths
        bboxes[:, 3] = heights

        # Yolo Batch Object
        # img: torch.FloatTensor. shape=(N, 3, H, W). normalized to [0, 1]
        # batch_idx: Int Tensor. shape=(-1, 1). index of bbox in the batch
        # cls: Int Tensor. shape=(-1, 1). class index of bbox
        # bboxes: Float Tensor. shape=(-1, 4). (center_x, center_y, width, height) of bbox. normalized to [0, 1]
        batch = {'img': inputs, 'batch_idx': batch_index, 'cls': cls, 'bboxes': bboxes}
        loss, _ = self._model(batch)
        return {'loss': loss}

    def prediction_step(self, inputs):
        assert isinstance(inputs, torch.Tensor) and inputs.dim() == 4  # (N, C, H, W)

        if self.training:
            raise RuntimeError("Model is in training mode. Call eval() before prediction_step.")

        results = self._model.predict(inputs)
        yolo_predictions = ultralytics.utils.ops.non_max_suppression(results, conf_thres=0.25, iou_thres=0.7, agnostic=False, max_det=300)
        predictions = []
        for pred in yolo_predictions:
            assert isinstance(pred, torch.Tensor) and pred.shape[1] == 6  # (x1, y1, x2, y2, conf, cls)
            new_pred = torch.cat([pred[:, 5:6], pred[:, 4:5], pred[:, :4]], dim=1)
            new_pred[:,2] /= inputs.shape[3]
            new_pred[:,3] /= inputs.shape[2]
            new_pred[:,4] /= inputs.shape[3]
            new_pred[:,5] /= inputs.shape[2]
            predictions.append(new_pred)

        return predictions

    def load_state_dict(self, *args, **kwargs):
        self._model.load_state_dict(*args, **kwargs)

    def state_dict(self):
        return self._model.state_dict()
