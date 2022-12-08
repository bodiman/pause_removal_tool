# **Pause Removal Model**
### Setup Anaconda Environment:

```
conda create -n myenv python=3.9
```

```
conda install pytorch torchvision torchaudio -c pytorch
```

### Then install all the Python module requirements:

```
pip install -r requirements.txt 
```

## **Model-training.ipynb documentation:**

### Data representation:
- The metadata file points to each file in the dataset and its NaturalPause value. As a first step in the notebook, we create a pandas dataframe to represent each file's path and their respective pause value.

### Audio Processing:
- Before the data is loaded into the dataset, it is processed into a mel spectrogram image as input.

- The Data is gathered by a PyTorch function called DataLoader, through passed inputs being the file paths.  More info here: [torch.utils.data.DataLoader()](https://pytorch.org/docs/stable/data.html).

- The Data Loader preprocesses the audio files into images. The stages for preprocessing are:
1. Open — Opening and loading the wav file from the path
2. Rechanneling — taking the stereo channels and converting them to seperate arrays
3. Resampling — 
4. Pad — 
5. Time shift —
6. Spectrogram


