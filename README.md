# movementmodeler-tools

Small helper scripts for working with pose data exported from the
MovementModeler iOS app.

These scripts are intentionally simple and meant to be read, modified,
or discarded as needed.

## Capture Tips (Important)

MovementModeler works best when the subject is clearly separated from the background.

For cleaner motion data:
- Fewer background people is always better
- Use a slightly elevated camera angle
- Keep a clean, visible floor plane
- Minimize background motion behind the subject

A higher vantage point reduces background skeleton detection while preserving enough perspective to accurately capture movement.

## What’s included

### mm_to_openpose.py
Converts a MovementModeler clip export into a directory of per-frame,
OpenPose-style BODY-25 JSON files.

```bash
python scripts/mm_to_openpose.py movementmodeler_clip.json frames_json/

MovementModeler app:
https://aegisstation.com/movementmodeler-education
