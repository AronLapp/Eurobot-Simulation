# Eurobot Simulation using gz-sim

## 1. Requirements

- gz sim harmonic
- ros2 jazzy integration for gazebo harmonic

```bash
sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
sudo apt-get update
sudo apt-get install gz-harmonic ros-jazzy-ros-gz
```

## 2. Workspace setup and build

```bash
cd ~/ros2_ws/src
cd ..
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-select eurobot_gz_sim
source install/setup.bash
```

## 3. Starting a simulation

```bash
ros2 launch eurobot_gz_sim eurobot{2x}_world.launch.py
```
