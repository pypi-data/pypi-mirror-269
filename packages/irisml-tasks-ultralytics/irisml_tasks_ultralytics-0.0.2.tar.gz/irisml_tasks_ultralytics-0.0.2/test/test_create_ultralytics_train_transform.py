import unittest
import PIL.Image
import torch
from irisml.tasks.create_ultralytics_train_transform import Task


class TestCreateUltralyticsTrainTransform(unittest.TestCase):
    def test_simple(self):
        outputs = Task(Task.Config(input_size=640)).execute(Task.Inputs())
        transform = outputs.transform

        inputs, targets = transform(PIL.Image.new("RGB", (256, 256), color='red'), torch.tensor([[0, 0.1, 0.1, 0.9, 0.9]]))
        self.assertIsInstance(inputs, torch.Tensor)
        self.assertEqual(targets.size(), (1, 5))
        self.assertEqual(inputs.size(), (3, 640, 640))

        # The image should be still red
        red, green, blue = inputs.mean(dim=(1, 2))
        self.assertGreater(red, green)
        self.assertGreater(red, blue)
