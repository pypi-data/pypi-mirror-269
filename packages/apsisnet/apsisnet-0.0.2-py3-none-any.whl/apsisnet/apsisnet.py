#-*- coding: utf-8 -*-
from __future__ import print_function
import warnings
warnings.filterwarnings('ignore')
#-------------------------
# imports
#-------------------------
import cv2
import onnxruntime as ort
import numpy as np
import os
from bnunicodenormalizer import Normalizer
from pathlib import Path
from .utils import download,correctPadding
from .modules import Recognizer
NORM=Normalizer()

#-------------------------
# model class
#------------------------
class ApsisNet(Recognizer):
    """
    A class representing the ApsisNet OCR model.

    Attributes:
        img_height (int): The height of the input image.
        img_width (int): The width of the input image.
        pos_max (int): Maximum position value.
        bnocr_gid (str): Google Drive ID for model weights.
        model (ort.InferenceSession): ONNX runtime inference session.
        vocab (list): List of characters in the vocabulary.

    Methods:
        get_model_weights: Get the path to the model weights.
        process_batch: Process a batch of image crops.
        infer: Perform inference on image crops.
    """

    def __init__(
        self,
        providers: list[str] = ['CUDAExecutionProvider', 'CPUExecutionProvider'],
        img_height: int = 32,
        img_width: int = 256,
        pos_max: int = 40,
        bnocr_gid: str = "1YwpcDJmeO5mXlPDj1K0hkUobpwGaq3YA"
    ) -> None:
        """
        Initialize the ApsisNet OCR model.

        Args:
            providers (list[str]): List of execution providers for ONNX runtime.
            img_height (int): The height of the input image (default: 32).
            img_width (int): The width of the input image (default: 256).
            pos_max (int): Maximum position value (default: 40).
            bnocr_gid (str): Google Drive ID for model weights (default: "1Ywpc...").

        """
        super().__init__()
        self.img_height = img_height
        self.img_width = img_width
        self.pos_max = pos_max
        self.bnocr_gid = bnocr_gid
        self.model = ort.InferenceSession(self.get_model_weights(), providers=providers)

        # Define the vocabulary
        self.vocab = [
            "blank", "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-",
            ".", "/", ":", ";", "<", "=", ">", "?", "।", "ঁ", "ং", "ঃ", "অ", "আ", "ই",
            "ঈ", "উ", "ঊ", "ঋ", "এ", "ঐ", "ও", "ঔ", "ক", "খ", "গ", "ঘ", "ঙ", "চ", "ছ",
            "জ", "ঝ", "ঞ", "ট", "ঠ", "ড", "ঢ", "ণ", "ত", "থ", "দ", "ধ", "ন", "প", "ফ",
            "ব", "ভ", "ম", "য", "র", "ল", "শ", "ষ", "স", "হ", "া", "ি", "ী", "ু", "ূ",
            "ৃ", "ে", "ৈ", "ো", "ৌ", "্", "ৎ", "ড়", "ঢ়", "য়", "০", "১", "২", "৩", "৪",
            "৫", "৬", "৭", "৮", "৯", "‍", "sep", "pad"
        ]

    def get_model_weights(self) -> str:
        """
        Get the path to the model weights.

        Returns:
            str: Path to the model weights.
        """
        home_path = str(Path.home())
        weight_path = Path(home_path, ".apsis_net", "bnocr.onnx")
        weight_path = Path(weight_path).resolve()
        weight_path.parent.mkdir(exist_ok=True, parents=True)
        weight_path = str(weight_path)
        if not os.path.isfile(weight_path):
            download(self.bnocr_gid, weight_path)
        return weight_path

    def process_batch(self, crops: list[np.ndarray]) -> dict:
        """
        Process a batch of image crops.

        Args:
            crops (list[np.ndarray]): List of image crops. 

        Returns:
            dict: Processed batch of image and position data. The dict has two keys
                  {
                      "image" : np.ndarray of processed images
                      "pos"   : np.ndarray of positonal vectors
                  }
        """
        batch_img = []
        batch_pos = []
        for img in crops:
            if type(img)==str:
                img=cv2.imread(img)
            # Correct padding
            img, _ = correctPadding(img, (self.img_height, self.img_width))
            # Normalize
            img = img / 255.0
            # Extend batch
            img = np.expand_dims(img, axis=0)
            batch_img.append(img)
            # Position
            pos = np.array([[i for i in range(self.pos_max)]])
            batch_pos.append(pos)

        # Stack images and positions
        img = np.vstack(batch_img).astype(np.float32)
        pos = np.vstack(batch_pos).astype(np.float32)

        # Return batch input
        return {"image": img, "pos": pos}

    def infer(self, crops: list[np.ndarray], batch_size: int = 32, normalize_unicode: bool = True) -> list[str]:
        """
        Perform inference on image crops.

        Args:
            crops (list[np.ndarray]): List of image crops
            batch_size (int): Batch size for inference (default: 32).
            normalize_unicode (bool): Flag to normalize unicode (default: True).

        Returns:
            list[str]: List of inferred texts.
        """
        # Adjust batch size
        if len(crops) < batch_size:
            batch_size = len(crops)

        texts = []
        for idx in range(0, len(crops), batch_size):
            batch = crops[idx:idx+batch_size]
            inp = self.process_batch(batch)
            preds = self.model.run(None, inp)[0]
            preds = np.argmax(preds, axis=-1)

            # Decoding predictions
            for pred in preds:
                label = ""
                for c in pred[1:]:
                    if c != self.vocab.index("sep"):
                        label += self.vocab[c]
                    else:
                        break
                texts.append(label)

        if normalize_unicode:
            normalized = [NORM(text)["normalized"] for text in texts]
            for idx in range(len(normalized)):
                if normalized[idx] is not None:
                    texts[idx] = normalized[idx]
                else:
                    texts[idx] = ""

        return texts

