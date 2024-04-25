# apsis-net
![](/useage/apsis.png) 

Apsis-net is a Bengali language ocr system for Printed Documents developed at [Apsis Solutions limited](https://apsissolutions.com/)

The full system is focused on bengali text recognition only 
* Text recognition:
    * Bangla Text : ApsisNet 
        * ApsisNet is a model developed at Apsis Solutions Limited. 
        * It is used by [bbOCR](https://github.com/BengaliAI/bbocr/blob/dev/modules.md) as the recognition model 
        * ApsisNet is found to be the best among other available recognition models (such as tesseract and easyOCR) in the linked [paper](https://arxiv.org/abs/2308.10647)


# **Installation**


## **As module/pypi package**
### **cpu installation**

```bash
pip install apsisnet
```

### **gpu installation**

It is recommended to use conda environment . Specially for GPU.

* **installing cudatoolkit and cudnn**: 

```bash
conda install cudatoolkit
conda install cudnn
```

* **installing packages**

```bash
pip install apsisnet
```

* **exporting environment variables**

```bash
mkdir -p $CONDA_PREFIX/etc/conda/activate.d
echo 'export LD_LIBRARY_PATH=$CUDNN_PATH/lib:$CONDA_PREFIX/lib/:$LD_LIBRARY_PATH' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
```

## **Building from source : Linux/Ubuntu**
It is recommended to use conda environment .

* **clone the repository** : 
```bash
git clone https://github.com/mnansary/apsisnet.git
cd apsisnet
```


* **create a conda environment**: 

```bash
conda create -n apsisnet python=3.9
```

* **activate conda environment**: 

```bash
conda activate apsisnet

```
* **cpu installation**  :

```bash
bash install.sh cpu
``` 
* **gpu installation**  :
    
```bash
bash install.sh gpu
``` 

# Useage


## Apsisnet : Bangla Recognizer

* useage
```python
from apsisnet import ApsisNet
bnocr=ApsisNet()
bnocr.infer(crops)
```
* docstring for ```ApsisNet.infer```

```python
"""
Perform inference on image crops.

Args:
    crops (list[np.ndarray]): List of image crops.
    batch_size (int): Batch size for inference (default: 32).
    normalize_unicode (bool): Flag to normalize unicode (default: True).

Returns:
    list[str]: List of inferred texts.
"""
```


**check ```useage/useage.ipynb``` for examples**


**TESTED GPU INFERENCE SERVER CONFIG**  

```python
OS          : Ubuntu 20.04.6 LTS      
Memory      : 62.4 GiB 
Processor   : Intel® Xeon(R) Silver 4214R CPU @ 2.40GHz × 24    
Graphics    : NVIDIA RTX A6000/PCIe/SSE2
Gnome       : 3.36.8
```
# License
Contents of this repository are restricted to non-commercial research purposes only under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/). 

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>

