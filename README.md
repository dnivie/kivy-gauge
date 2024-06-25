# kivy-gauge
A kivy python app running as a container on RaspberryPI

```sh
docker build -t kivy-app .

xhost +local:root

docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix kivy-app0

```
