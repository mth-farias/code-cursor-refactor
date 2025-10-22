# Discovery Log

## Speed_Denoised - Missing PARAM

**Date**: 2025-10-22  
**Status**: ⚠️ Missing from Config.PARAM

### What
`Speed_Denoised` is a computed column output in scored CSVs but NOT registered in PARAM.

### Evidence
- **Created**: `_classifier.py` line 595 (`layer1_denoised()`)
- **Published**: `_main.py` line 934 (scored schema)
- **Missing**: Not in `Config.PARAM["SCORED"]`
- **Example CSV**: `data/ExampleFiles/scored.csv` doesn't have it (old?)

### Schema Should Be
```python
SCORED = [
    ...,
    "Speed",
    "Speed_Denoised",  # <-- ADD THIS
    "Motion",
    ...
]
```

### Action Needed
Add to Config.PARAM during refactoring.

---

## Data Flow Trace

### Input Files
- `*_tracked.csv` - From tracker (Speed, Motion, Position_X, Position_Y, VisualStim, Stim0, Stim1)
- `*_sleap.csv` - Optional pose data

### Pipeline Stages

**1. Load & Clean**
- Load tracked CSV
- Clean ALL stimulus channels (fill zeros, clean ones)
- Columns: Base + stimulus columns

**2. Pre-flight QC**
- Fatal errors: missing columns, invalid data
- Stop if errors → copy inputs to Error/

**3. Feature Construction**
- Speed (already in tracked)
- Orientation (computed)
- Motion (PixelChange → Motion)
- Pose view selection (if SLEAP available)

**4. Classification**
- Layer1: Speed + Motion → labels
- **Speed_Denoised**: Smooth Speed (0.5s window, guards)
- Layer1_Denoised: Speed_Denoised + Motion → labels + micro-bout deletion
- Layer2: Windowed voting on Layer1
- Layer2_Denoised: Robust voting with >50% valid requirement
- Behavior_Denoised: Gap-fill Layer2_Denoised (≤1s gaps, skip response windows)

**5. Resistant**
- Build coverage windows (pre+post stim)
- Check if Freeze covers window
- Output: Resistant_Freeze or NaN

**6. Pose Scoring** (optional)
- If SLEAP data available
- Pose labels based on view

**7. Alignment & Crop**
- Extract experimental periods
- Align to timebase

**8. Post-classification Flags**
- Non-fatal warnings (high NaN, suspicious patterns)
- Don't block publish

**9. Atomic Publish**
- Write to temp
- fsync
- Rename
- Outputs: `*_scored.csv`, `*_pose.csv` (if applicable)

### Output Columns (SCORED)
```
FrameIndex, VisualStim, Stim0, Stim1,
Position_X, Position_Y,
Speed, Speed_Denoised, Motion,  <-- Speed_Denoised HERE
Layer1, Layer1_Denoised,
Layer2, Layer2_Denoised,
Resistant, Resistant_Denoised,
Behavior, Behavior_Denoised
```

### Column Mapping Analysis

**INPUT (tracked.csv)**:
```
FrameIndex, VisualStim, Stim0, Stim1,
NormalizedCentroidX, NormalizedCentroidY, PixelChange
```

**COMPUTED (during processing)**:
```
Position_X, Position_Y  ← from NormalizedCentroidX/Y (geometry conversion)
Speed                   ← from position deltas
Motion                  ← from PixelChange
Speed_Denoised          ← from Speed (smoothed) ⚠️ MISSING FROM PARAM
Orientation             ← in pose.csv (from SLEAP)
```

**CLASSIFICATION (all computed)**:
```
Layer1, Layer1_Denoised,
Layer2, Layer2_Denoised,
Resistant, Resistant_Denoised,
Behavior, Behavior_Denoised
```

**OUTPUT (scored.csv)**:
```
FrameIndex + stims + Position_X/Y + Speed + Speed_Denoised + Motion +
Layer1 + Layer1_Denoised + Layer2 + Layer2_Denoised +
Resistant + Resistant_Denoised + Behavior + Behavior_Denoised
```

**OUTPUT (pose.csv)** (if SLEAP available):
```
FrameIndex + Orientation + View + View_X/Y +
Head_X/Y + Thorax_X/Y + Abdomen_X/Y + LeftWing_X/Y + RightWing_X/Y
```

### Findings
✅ Resistant_Denoised IS used (parallel to other _Denoised columns)  
✅ Orientation IS published (in pose.csv, not scored.csv)  
⚠️ Speed_Denoised MISSING from PARAM (add to SCORED)  
✅ All other columns accounted for

