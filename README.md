# movementmodeler-tools

Small helper scripts for working with pose data exported from the
MovementModeler iOS app.

These scripts are intentionally simple and meant to be read, modified,
or discarded as needed.

## What’s included

### mm_to_openpose.py
Converts a MovementModeler clip export into a directory of per-frame,
OpenPose-style BODY-25 JSON files.

```bash
python scripts/mm_to_openpose.py movementmodeler_clip.json frames_json/
