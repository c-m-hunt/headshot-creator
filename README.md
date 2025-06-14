# Headshot creator

## Description
Producing consistent size headshots for people given variable sized inputs.

Will take input images and find faces using Keras VGGFace model. Padding is then applied to top and bottom of the face. The width is then adjusted to ensure the expected aspect ratio of the output.

Works best when person is centered and looking directly at the camera.

A warning will be displayed if the calculated image is beyond the bounds of the original image. Adjust the padding or aspect ratio accordingly. The process will still continue with other detected faces and images in input directory.

## Arguments (and defaults)
* `output_size` [(400, 500)] - Resolution of the output images
* `padding` [(0.4, 0.6)] - Padding (percentage compared to size of face) of top and bottom of image
* `confidence_threshold` [0.95] - Threshold at which confidnece of face detection is output. Keep high to avoid background images
* `output_path` [''] - Path within the output folder to place images
* `input_file` [`None`] - An input file with a list of URLs to use
* `debug` [`False`] - Outputs input image with boxes draw. Blue - detected face. Green - output headshot. Red - headshot not output. Orange - headshot below the confidence threshold
* `img_format` ['jpg'] - Format of the output images

## Running in Docker
Amend the `input` volume mapping to location where images are stored

Amend the `output` volume mapping to output location

Amend the run arguments in `docker-compose.yaml`. See above for arguments description and defaults.

```
docker-compose up
```

First run builds the image and will take longer. Subsequent runs will be quicker.

## Running locally
Install with `uv sync`

Run with arguments to override defaults (detailed above).
```
uv run python main.py headshots \
  --output_size='(800,1000)' \
  --padding='(0.3,0.6)' \
  --confidence_threshold=0.95 \
  --output_path=./ \
  --input_file=./test.txt \
  --img_format=png \
  --debug
```

## References
* Ideas from https://machinelearningmastery.com/how-to-perform-face-recognition-with-vggface2-convolutional-neural-network-in-keras/
* Detections from https://github.com/ipazc/mtcnn
