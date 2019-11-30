# Headshot creator

## Description
Producing consistent size headshots for people given variable sized inputs.

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