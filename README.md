# Headshot creator

## Description
Producing consistent size headshots for people given variable sized inputs.

Will take input images and find faces using Keras VGGFace model. Padding is then applied to top and bottom of the face. The width is then adjusted to ensure the expected aspect ratio of the output.

A warning will be displayed if the calculated image is beyond the bounds of the original image. Adjust the padding or aspect ratio accordingly. The process will still continue with other detected faces and images in input directory.

## Arguments (and defaults)
* `output_size` [(400, 500)] - Resolution of the output images
* `padding` [(40, 60)] - Padding (percentage compared to size of face) of top and bottom of image
* `confidence_threshold` [0.95] - Threshold at which confidnece of face detection is output. Keep high to avoid background images

## Running in Docker
Amend the `input` volume mapping to location where images are stored

Amend the `output` volume mapping to output location

Amend the run arguments in `docker-compose.yaml`. See above for arguments description and defaults.

```
docker-compose up
```

First run builds the image and will take longer. Subsequent runs will be quicker.

## Running locally
Create and activate Conda environment `conda env create -f env.yaml`, `conda activate headshot-creator`

Run with arguments to override defaults (detailed above).
```
python main.py \
  --output_size='(800,500)' \
  --padding='(40,100)' \
  --confidence_threshold=0.95
```

## References
Ideas from https://machinelearningmastery.com/how-to-perform-face-recognition-with-vggface2-convolutional-neural-network-in-keras/