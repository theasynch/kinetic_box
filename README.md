# 📦 KineticBox

**KineticBox** is an intelligent computer vision tool that detects and tracks moving objects in a video.  
It draws bounding hitboxes of randomized colors (Red, Green, Blue) around each object and displays their **instantaneous speed** in pixels/frame.

This tool is perfect for basic surveillance analysis, motion tracking, and visual debugging of video movement patterns.  
It ensures visual clarity by limiting visual clutter: **no more than 3 hitboxes per region**, and maintains **persistent object identity** for a clean output.

---

## 🚀 Features

- 🔲 Hitboxes for every moving object
- 🎨 Randomized color per object (Red, Green, or Blue)
- ⚡ Instantaneous speed displayed above each object
- 🧠 Persistent object tracking using centroid proximity
- 🧹 Clutter control: max 3 hitboxes per region
- 💾 Exports the fully processed video in `.mp4` format

---

## 📦 Requirements

Make sure you have Python 3.x installed.

Install the required libraries using pip:

```bash
pip install opencv-python numpy
```

## 📂 How to Use

1. **Place your video** (e.g. `input_video.mp4`) in the same directory as the script.

2. **Edit the script**:

   Set the video file name in the `VIDEO_PATH` variable:

   ```python
   VIDEO_PATH = 'input_video.mp4'
   ```
3. **Run the script**:
   ```python
   python kineticbox.py
   ```
4. **Check the output:**
   The output file will be titled `output_with_hitboxes.mp4`

## 🛠️ Configuration (Optional)
Inside the script, you can customize:

| Variable                 | Purpose                                   | Default |
| ------------------------ | ----------------------------------------- | ------- |
| `PROXIMITY_THRESHOLD`    | Controls how close hitboxes can be        | `100`   |
| `MAX_HITBOXES_IN_REGION` | Max hitboxes allowed in a local region    | `3`     |
| `MAX_MATCH_DISTANCE`     | Matching distance for persistent tracking | `50`    |


## 🧪 Example Use Cases
- 📹 Analyzing foot traffic in hallways or lobbies

- 🎮 Game dev: motion debugging from gameplay video

- 🕵️ Security footage analysis

- 📈 Creating speed datasets for moving objects


## 🧠 How It Works
- The program uses background subtraction (MOG2) to detect moving objects.

- Objects are tracked frame-by-frame using centroid proximity.

- Speed is calculated as the distance moved between frames.

- Hitboxes and speed text are rendered with OpenCV in real time.

## 💡 Ideas for Future Versions
- Export object motion data to CSV

- Add heatmap generation of object movement

- Integrate real-time webcam support

- Use object classification for smarter labeling


### Authored by abeyaarom and licensed under MIT 2025
