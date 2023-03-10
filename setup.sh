

# Update Raspi to Latest Version
sudo apt update
sudo apt full-upgrade -y

# Install Gpiozero
sudo apt update
sudo pip3 install gpiozero

# Python3 Dev
sudo apt-get install python3-dev -y

# Tensorflow Lite Intallation
sudo apt update
sudo apt upgrade -y
echo "deb [signed-by=/usr/share/keyrings/coral-edgetpu-archive-keyring.gpg] https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo tee /usr/share/keyrings/coral-edgetpu-archive-keyring.gpg >/dev/null
sudo apt update
sudo apt install python3-tflite-runtime libatlas-base-dev -y

# Download Tensorflow Lite Model
sudo apt install git -y
git clone https://github.com/tensorflow/examples --depth 1
mv ./examples ./tensorflow_model
cd ./tensorflow_model/lite/examples/audio_classification/raspberry_pi
chmod +x ./setup.sh
sudo ./setup.sh
cd ~

# Pyaudio
#sudo apt install portaudio19-dev python3-pyaudio -y

# Librosa (Optional)
# pip3 install librosa

# Install Adafruit DHT11 Library
pip3 install adafruit-circuitpython-dht
sudo apt-get install libgpiod2

# Install Port Audio
sudo apt-get install libportaudio2


