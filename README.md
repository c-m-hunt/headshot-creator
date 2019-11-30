# Headshot creator

## Description
Producing consistent size headshots for people given variable sized inputs.

Will take input images and find faces using Keras VGGFace model. Padding is then applied to top and bottom of the face. The width is then adjusted to ensure the expected aspect ratio of the output.

A warning will be displayed if the calculated image is beyond the bounds of the original image. Adjust the padding or aspect ratio accordingly. The process will still continue with other detected faces and images in input directory.

## Running in Docker
Amend the `input` volume mapping to location where images are stored

Amend the `output` volume mapping to output location

Amend the run parameters in `docker-compose.yaml`
* `output_size` - Resolution of the output images
* `padding` - Padding (percentage compared to size of face) of top and bottom of image

```
docker-compose up
```

First run builds the image and will take longer. Subsequent runs will be quicker.

## References
Ideas from https://machinelearningmastery.com/how-to-perform-face-recognition-with-vggface2-convolutional-neural-network-in-keras/