import unittest
import torch
from irisml.tasks.create_ultralytics_yolov9_detection_model import Task


class TestCreateUltralyticsYolov9DetectionModel(unittest.TestCase):
    def test_simple(self):
        outputs = Task(Task.Config('yolov9c', 80)).execute(Task.Inputs())
        self.assertIsInstance(outputs.model, torch.nn.Module)

        model = outputs.model

        training_output = model.training_step(torch.zeros((1, 3, 128, 128)), [torch.zeros((0, 5))])
        self.assertIsInstance(training_output['loss'], torch.Tensor)

        model.eval()
        prediction_output = model.prediction_step(torch.zeros((1, 3, 128, 128)))
        self.assertIsInstance(prediction_output, list)
        self.assertIsInstance(prediction_output[0], torch.Tensor)
        self.assertEqual(prediction_output[0].shape[1], 6)
