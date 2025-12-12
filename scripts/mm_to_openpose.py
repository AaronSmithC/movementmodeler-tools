#!/usr/bin/env python3
import json
import os
import sys

def convert_mm_to_openpose(mm_json_path, out_dir):
    with open(mm_json_path, "r") as f:
        data = json.load(f)

    width = data.get("width", 1)
    height = data.get("height", 1)
    frames = data["frames"]

    os.makedirs(out_dir, exist_ok=True)

    for frame in frames:
        idx = frame.get("frameIndex", 0)
        people_out = []

        for person in frame.get("people", []):
            keypoints = [0.0] * (25 * 3)

            for j in person.get("joints", []):
                k = j.get("index", -1)
                if 0 <= k < 25:
                    x_norm = j.get("x", 0.0)
                    y_norm = j.get("y", 0.0)
                    c = j.get("c", 0.0)

                    x = x_norm * width
                    y = (1.0 - y_norm) * height

                    keypoints[3*k:3*k+3] = [float(x), float(y), float(c)]

            people_out.append({
                "person_id": [-1],
                "pose_keypoints_2d": keypoints
            })

        openpose_frame = {
            "version": 1.3,
            "people": people_out
        }

        out_fname = f"pose_{idx:012d}_keypoints.json"
        out_path = os.path.join(out_dir, out_fname)

        with open(out_path, "w") as f:
            json.dump(openpose_frame, f)

    print(f"Converted {len(frames)} frames to {out_dir}")

def main():
    if len(sys.argv) != 3:
        print("Usage: mm_to_openpose.py movementmodeler.json output_dir")
        sys.exit(1)

    convert_mm_to_openpose(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
