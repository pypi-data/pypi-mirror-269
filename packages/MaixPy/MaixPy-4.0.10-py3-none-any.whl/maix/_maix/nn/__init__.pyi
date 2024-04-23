"""
maix.nn module
"""
from __future__ import annotations
import maix._maix.err
import maix._maix.image
import maix._maix.tensor
from . import F
__all__ = ['Classifier', 'F', 'LayerInfo', 'MUD', 'NN', 'Object', 'YOLOv5']
class Classifier:
    label_path: str
    labels: list[str]
    mean: list[float]
    scale: list[float]
    def __init__(self, model: str = '') -> None:
        ...
    def classify(self, img: maix._maix.image.Image, softmax: bool = True) -> list[tuple[int, float]]:
        """
        Forward image to model, get result. Only for image input, use classify_raw for tensor input.
        
        Args:
          - img: image, format should match model input_type， or will raise err.Exception
          - softmax: if true, will do softmax to result, or will return raw value
        
        
        Returns: result, a list of (label, score). In C++, you need to delete it after use.
        """
    def classify_raw(self, data: maix._maix.tensor.Tensor, softmax: bool = True) -> list[tuple[int, float]]:
        """
        Forward tensor data to model, get result
        
        Args:
          - data: tensor data, format should match model input_type， or will raise err.Excetion
          - softmax: if true, will do softmax to result, or will return raw value
        
        
        Returns: result, a list of (label, score). In C++, you need to delete it after use.
        """
    def input_format(self) -> maix._maix.image.Format:
        """
        Get input image format, only for image input
        
        Returns: input image format, image::Format type.
        """
    def input_height(self) -> int:
        """
        Get model input height, only for image input
        
        Returns: model input size of height
        """
    def input_shape(self) -> list[int]:
        """
        Get input shape, if have multiple input, only return first input shape
        
        Returns: input shape, list type
        """
    def input_size(self) -> maix._maix.image.Size:
        """
        Get model input size, only for image input
        
        Returns: model input size
        """
    def input_width(self) -> int:
        """
        Get model input width, only for image input
        
        Returns: model input size of width
        """
    def load(self, model: str) -> maix._maix.err.Err:
        """
        Load model from file, model format is .mud,
        MUD file should contain [extra] section, have key-values:
        - model_type: classifier
        - input_type: rgb or bgr
        - mean: 123.675, 116.28, 103.53
        - scale: 0.017124753831663668, 0.01750700280112045, 0.017429193899782137
        - labels: imagenet_classes.txt
        
        Args:
          - model: MUD model path
        
        
        Returns: error code, if load failed, return error code
        """
class LayerInfo:
    dtype: maix._maix.tensor.DType
    name: str
    shape: list[int]
    def __init__(self, name: str = '', dtype: maix._maix.tensor.DType = ..., shape: list[int] = []) -> None:
        ...
    def __str__(self) -> str:
        """
        To string
        """
    def to_str(self) -> str:
        """
        To string
        """
class MUD:
    items: dict[str, dict[str, str]]
    type: str
    def __init__(self, model_path: str = None) -> None:
        ...
    def load(self, model_path: str) -> maix._maix.err.Err:
        """
        Load model from file
        
        Args:
          - model_path: direction [in], model file path, model format can be MUD(model universal describe file) file.
        
        
        Returns: error code, if load success, return err::ERR_NONE
        """
class NN:
    def __init__(self, model: str = '') -> None:
        ...
    def extra_info(self) -> dict[str, str]:
        """
        Get model extra info define in MUD file
        
        Returns: extra info, dict type, key-value object, attention: key and value are all string type.
        """
    def forward(self, inputs: maix._maix.tensor.Tensors) -> maix._maix.tensor.Tensors:
        """
        forward run model, get output of model,
        this is specially for MaixPy, not efficient, but easy to use in MaixPy
        
        Args:
          - input: direction [in], input tensor
        
        
        Returns: output tensor. In C++, you should manually delete tensors in return value and return value.
        """
    def forward_image(self, img: maix._maix.image.Image, mean: list[float] = [], scale: list[float] = [], fit: maix._maix.image.Fit = ...) -> maix._maix.tensor.Tensors:
        """
        forward model, param is image
        
        Args:
          - img: input image
          - mean: mean value, a list type, e.g. [0.485, 0.456, 0.406], default is empty list means not normalize.
          - scale: scale value, a list type, e.g. [1/0.229, 1/0.224, 1/0.225], default is empty list means not normalize.
          - fit: fit mode, if the image size of input not equal to model's input, it will auto resize use this fit method,
        default is image.Fit.FIT_FILL for easy coordinate calculation, but for more accurate result, use image.Fit.FIT_CONTAIN is better.
        
        
        Returns: output tensor. In C++, you should manually delete tensors in return value and return value.
        """
    def inputs_info(self) -> list[LayerInfo]:
        """
        Get model input layer info
        
        Returns: input layer info
        """
    def load(self, model: str) -> maix._maix.err.Err:
        """
        Load model from file
        
        Args:
          - model: direction [in], model file path, model format can be MUD(model universal describe file) file.
        
        
        Returns: error code, if load success, return err::ERR_NONE
        """
    def loaded(self) -> bool:
        """
        Is model loaded
        
        Returns: true if model loaded, else false
        """
    def outputs_info(self) -> list[LayerInfo]:
        """
        Get model output layer info
        
        Returns: output layer info
        """
class Object:
    class_id: int
    h: int
    score: float
    w: int
    x: int
    y: int
    def __init__(self, x: int = 0, y: int = 0, w: int = 0, h: int = 0, class_id: int = 0, score: float = 0) -> None:
        ...
    def __str__(self) -> str:
        """
        Object info to string
        
        Returns: Object info string
        """
class YOLOv5:
    anchors: list[float]
    label_path: str
    labels: list[str]
    mean: list[float]
    scale: list[float]
    def __init__(self, model: str = '') -> None:
        ...
    def detect(self, img: maix._maix.image.Image, conf_th: float = 0.5, iou_th: float = 0.45, fit: maix._maix.image.Fit = ...) -> list[...]:
        """
        Detect objects from image
        
        Args:
          - img: Image want to detect, if image's size not match model input's, will auto resize with fit method.
          - conf_th: Confidence threshold, default 0.5.
          - iou_th: IoU threshold, default 0.45.
          - fit: Resize method, default image.Fit.FIT_CONTAIN.
        
        
        Returns: Object list. In C++, you should delete it after use.
        """
    def input_format(self) -> maix._maix.image.Format:
        """
        Get input image format
        
        Returns: input image format, image::Format type.
        """
    def input_height(self) -> int:
        """
        Get model input height
        
        Returns: model input size of height
        """
    def input_size(self) -> maix._maix.image.Size:
        """
        Get model input size
        
        Returns: model input size
        """
    def input_width(self) -> int:
        """
        Get model input width
        
        Returns: model input size of width
        """
    def load(self, model: str) -> maix._maix.err.Err:
        """
        Load model from file
        
        Args:
          - model: Model path want to load
        
        
        Returns: err::Err
        """
