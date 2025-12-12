#!/usr/bin/env python3
import os
import sys
import json
import numpy as np

import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter


# ---------------------------
# BODY_25 skeleton definition
# ---------------------------
BODY_25_PAIRS = [
    (1, 8), (1, 2), (1, 5),
    (2, 3), (3, 4),
    (5, 6), (6, 7),
    (8, 9), (9, 10), (10, 11),
    (8, 12), (12, 13), (13, 14),
    (1, 0), (0, 15), (15, 17),
    (0, 16), (16, 18),
    (14, 19), (19, 20),
    (11, 22), (22, 23),
]

CONF_THRESHOLD = 0.1


# ---------------------------
# Load 1 frame's BODY_25 JSON
# ---------------------------
def load_keypoints(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    if not data.get("people"):
        return None

    flat = data["people"][0]["pose_keypoints_2d"]
    pts = [(flat[i], flat[i+1], flat[i+2]) for i in range(0, len(flat), 3)]
    return pts  # list of (x,y,c) for 25 joints


# ---------------------------
# Main
# ---------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: make_stick_anim.py /path/to/json_folder")
        sys.exit(1)

    json_dir = os.path.abspath(sys.argv[1])

    if not os.path.isdir(json_dir):
        print(f"Error: not a directory: {json_dir}")
        sys.exit(1)

    # collect frame files
    json_files = sorted(
        f for f in os.listdir(json_dir)
        if f.endswith(".json")
    )

    if not json_files:
        print(f"No JSON keypoints found in {json_dir}")
        sys.exit(1)

    json_paths = [os.path.join(json_dir, f) for f in json_files]

    # Load all frames and gather bounds
    all_frames = []
    xs_all, ys_all = [], []

    for jp in json_paths:
        pts = load_keypoints(jp)
        all_frames.append(pts)

        if pts:
            for (x, y, c) in pts:
                if c > CONF_THRESHOLD:
                    xs_all.append(x)
                    ys_all.append(y)

    if not xs_all:
        print("No confident keypoints found.")
        sys.exit(1)

    # determine bounds
    x_min, x_max = min(xs_all), max(xs_all)
    y_min, y_max = min(ys_all), max(ys_all)
    margin_x = max((x_max - x_min) * 0.1, 10)
    margin_y = max((y_max - y_min) * 0.1, 10)

    x_min -= margin_x
    x_max += margin_x
    y_min -= margin_y
    y_max += margin_y

    # Create plot
    fig, ax = plt.subplots(figsize=(4, 6))
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_max, y_min)  # invert y-axis
    ax.axis("off")

    joint_scatter = ax.scatter([], [], s=20, color="black")
    lines = []
    for _ in BODY_25_PAIRS:
        line, = ax.plot([], [], linewidth=2, color="black")
        lines.append(line)

    # output path
    clip_dir = os.path.dirname(json_dir)
    clip_name = os.path.basename(clip_dir)
    out_video = os.path.join(clip_dir, f"{clip_name}_stick.mp4")

    print(f"Input folder : {json_dir}")
    print(f"Output video : {out_video}")
    print(f"Frames       : {len(all_frames)}")

    writer = FFMpegWriter(fps=10, codec="mpeg4", bitrate=2000)

    # ---------------------------
    # Rendering loop
    # ---------------------------
    with writer.saving(fig, out_video, dpi=150):
        for idx, pts in enumerate(all_frames):

            # CASE 1: no detection
            if pts is None:
                joint_scatter.set_offsets(np.empty((0, 2)))
                for line in lines:
                    line.set_data([], [])
            
            # CASE 2: person present
            else:
                xs = [p[0] for p in pts]
                ys = [p[1] for p in pts]
                cs = [p[2] for p in pts]

                xy = [
                    [x, y]
                    for (x, y, c) in zip(xs, ys, cs)
                    if c > CONF_THRESHOLD
                ]

                if xy:
                    joint_scatter.set_offsets(np.array(xy))
                else:
                    joint_scatter.set_offsets(np.empty((0, 2)))

                # skeleton lines
                for (pair, line) in zip(BODY_25_PAIRS, lines):
                    i, j = pair
                    x1, y1, c1 = pts[i]
                    x2, y2, c2 = pts[j]
                    if c1 > CONF_THRESHOLD and c2 > CONF_THRESHOLD:
                        line.set_data([x1, x2], [y1, y2])
                    else:
                        line.set_data([], [])

            # progress prints
            if idx % 50 == 0:
                print(f"Frame {idx+1}/{len(all_frames)}")

            writer.grab_frame()

    print("Done.")


if __name__ == "__main__":
    main()

