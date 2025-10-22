# BehaviorClassifier Pipeline Diagram

**The Conveyor**: Complete data flow from tracked CSV to scored outputs

---

## 📥 INPUT FILES

```
*_tracked.csv                          *_sleap.csv (optional)
├─ FrameIndex                          ├─ FrameIndex
├─ VisualStim                          ├─ View confidence scores
├─ Stim0, Stim1                        ├─ Head_X/Y
├─ NormalizedCentroidX/Y               ├─ Thorax_X/Y
└─ PixelChange                         ├─ Abdomen_X/Y
                                       ├─ LeftWing_X/Y
                                       └─ RightWing_X/Y
```

---

## 🔄 PIPELINE STAGES

```
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 1: LOAD & CLEAN STIMULUS                                 │
├─────────────────────────────────────────────────────────────────┤
│ Input:  *_tracked.csv                                           │
│ Action: - Load CSV to DataFrame                                 │
│         - Clean ALL stimulus channels (VisualStim, Stim0, Stim1)│
│           • fill_zeros(tolerance=NOISE_TOLERANCE)               │
│           • clean_ones()                                        │
│ Output: df with cleaned stimulus columns                        │
│ Module: BC_UTILS (stimulus cleaners)                            │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 2: PRE-FLIGHT QC (FATAL ERRORS)                          │
├─────────────────────────────────────────────────────────────────┤
│ Action: - Validate schema (required columns present)            │
│         - Check data types and ranges                           │
│         - Validate stimulus detection mapping                   │
│ Pass:   Continue to feature construction                        │
│ FAIL:   → Copy inputs to Error/ folder                          │
│         → Log to REPORT_ERROR.csv                               │
│         → STOP processing this file                             │
│ Module: BC_QC (error detection)                                 │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 3: FEATURE CONSTRUCTION                                   │
├─────────────────────────────────────────────────────────────────┤
│ Action: - Geometry conversion:                                  │
│           NormalizedCentroidX/Y → Position_X/Y (mm)             │
│         - Speed calculation (mm/s from position deltas)         │
│         - Motion conversion: PixelChange → Motion (0/1)         │
│         - IF SLEAP data:                                        │
│           • Select view (Top/Left/Right from confidences)       │
│           • Compute Orientation (0°=North)                      │
│ New Cols: Position_X, Position_Y, Speed, Motion                 │
│           (+ Orientation, View if SLEAP)                        │
│ Module: BC_UTILS (geometry, motion, pose)                       │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 4: CLASSIFICATION (5 LAYERS)                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ 4a. LAYER1 (Raw Speed-Based)                                    │
│     Rules: if Speed ≥ 75 mm/s        → Jump                     │
│            elif Motion == 0           → Freeze                  │
│            elif 4 ≤ Speed < 75        → Walk                    │
│            else (Speed < 4)           → Stationary              │
│     New Col: Layer1                                             │
│                                                                  │
│ 4b. LAYER1_DENOISED (Smoothed Speed)                            │
│     Step 1: Smooth Speed → Speed_Denoised                       │
│             • Centered 0.5s window                              │
│             • Guard: If ANY frame ≥75 mm/s, don't smooth        │
│             • Guard: Skip stimulus response windows             │
│     Step 2: Reclassify using Speed_Denoised                     │
│     Step 3: Delete micro-bouts ≤ NOISE_TOLERANCE frames         │
│             • NEVER delete Jump bouts                           │
│     New Cols: Speed_Denoised, Layer1_Denoised                   │
│                                                                  │
│ 4c. LAYER2 (Windowed Voting)                                    │
│     • Centered 0.1s window on Layer1 labels                     │
│     • Count votes for each behavior                             │
│     • Majority wins (ties: Walk > Stationary > Freeze)          │
│     New Col: Layer2                                             │
│                                                                  │
│ 4d. LAYER2_DENOISED (Robust Voting)                             │
│     • Same as Layer2 but on Layer1_Denoised                     │
│     • Require >50% valid frames in window                       │
│     New Col: Layer2_Denoised                                    │
│                                                                  │
│ 4e. BEHAVIOR_DENOISED (Gap Filling)                             │
│     • Fill NaN gaps ≤1s when same label bounds both sides       │
│     • Skip gaps in stimulus response windows                    │
│     • Optional: Check flank bout lengths                        │
│     New Col: Behavior_Denoised                                  │
│                                                                  │
│ Module: BC_CLASSIFIER                                           │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 5: RESISTANT BEHAVIOR (Stimulus-Locked)                   │
├─────────────────────────────────────────────────────────────────┤
│ Action: For each stimulus onset:                                │
│         - Build coverage window:                                │
│           [onset - 1s, onset + 1s]                              │
│         - Check if Freeze bout fully covers window              │
│         - If YES → Resistant_Freeze                             │
│         - If NO  → NaN                                          │
│                                                                  │
│ Applied to: Layer2 → Resistant                                  │
│             Layer2_Denoised → Resistant_Denoised                │
│                                                                  │
│ New Cols: Resistant, Resistant_Denoised                         │
│ Module: BC_CLASSIFIER (resistant detection)                     │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 6: BEHAVIOR MAPPING (Final Labels)                        │
├─────────────────────────────────────────────────────────────────┤
│ Action: Map Layer2 → Behavior domain                            │
│         - Simplify to {Jump, Walk, Stationary, Freeze}          │
│         - Promotion: Freeze + Resistant_Freeze → Resistant_Freeze│
│                                                                  │
│ Applied to: Layer2 + Resistant → Behavior                       │
│             Layer2_Denoised + Resistant_Denoised → Behavior_Denoised│
│                                                                  │
│ New Cols: Behavior, Behavior_Denoised                           │
│ Module: BC_CLASSIFIER (behavior mapping)                        │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 7: POSE SCORING (Optional, if SLEAP available)            │
├─────────────────────────────────────────────────────────────────┤
│ Action: - Compute Orientation from body parts                   │
│         - Select best view (Top/Left/Right)                     │
│         - Extract View_X, View_Y coordinates                    │
│ New Cols: Orientation, View, View_X, View_Y                     │
│           (+ body part coordinates)                             │
│ Module: BC_UTILS (pose view selection)                          │
│ Note: These go to separate *_pose.csv file                      │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 8: ALIGNMENT & CROPPING                                   │
├─────────────────────────────────────────────────────────────────┤
│ Action: - Extract experimental periods from EXPERIMENT          │
│         - Crop to relevant time windows                         │
│         - Align to standardized timebase                        │
│ Module: BC_UTILS (alignment)                                    │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 9: POST-CLASSIFICATION FLAGS (Non-Fatal QC)               │
├─────────────────────────────────────────────────────────────────┤
│ Action: - Check NaN fraction in outputs                         │
│         - Validate behavior patterns                            │
│         - Check bout length distributions                       │
│         - Validate pose data (if applicable)                    │
│                                                                  │
│ Pass:   → Publish to Scored/ folder                             │
│ FLAG:   → Publish to Flag/Scored/ folder                        │
│         → Log to REPORT_FLAG.csv                                │
│         → Continue (non-fatal)                                  │
│                                                                  │
│ Module: BC_QC (flag detection)                                  │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 10: ATOMIC PUBLISH                                        │
├─────────────────────────────────────────────────────────────────┤
│ Action: For each output CSV:                                    │
│         1. Write to temp file (*.~tmp.csv)                      │
│         2. fsync (flush to disk)                                │
│         3. Rename temp → final (atomic operation)               │
│                                                                  │
│ Outputs: *_scored.csv  (to Scored/ or Flag/Scored/)            │
│          *_pose.csv    (to Pose/ or Flag/Pose/, if SLEAP)      │
│                                                                  │
│ Module: BC_UTILS (atomic CSV writer)                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📤 OUTPUT FILES

### *_scored.csv (17 columns)
```
[Metadata]
FrameIndex

[Stimuli - cleaned]
VisualStim, Stim0, Stim1

[Features]
Position_X, Position_Y, Speed, Speed_Denoised, Motion

[Classification Layers]
Layer1, Layer1_Denoised, Layer2, Layer2_Denoised

[Resistant Labels]
Resistant, Resistant_Denoised

[Final Behavior]
Behavior, Behavior_Denoised
```

### *_pose.csv (15 columns, if SLEAP)
```
FrameIndex, Orientation, View, View_X, View_Y,
Head_X, Head_Y, Thorax_X, Thorax_Y, Abdomen_X, Abdomen_Y,
LeftWing_X, LeftWing_Y, RightWing_X, RightWing_Y
```

### REPORT_ERROR.csv
```
Lists all files with fatal errors (pre-flight QC failures)
```

### REPORT_FLAG.csv
```
Lists all files with non-fatal flags (post-classification warnings)
```

---

## 🔀 ERROR HANDLING BRANCHES

```
Pre-flight FAIL ──→ Error/Tracked/*_tracked.csv (input copy)
                 └→ Error/Pose/*_sleap.csv (if exists)
                 └→ REPORT_ERROR.csv (log entry)
                 └→ STOP (no outputs generated)

Post-class FLAG ──→ Flag/Scored/*_scored.csv (output)
                 └→ Flag/Pose/*_pose.csv (if SLEAP)
                 └→ REPORT_FLAG.csv (log entry)
                 └→ CONTINUE (outputs generated with warning)

Success ─────────→ Scored/*_scored.csv
                 └→ Pose/*_pose.csv (if SLEAP)
```

---

## 📊 COLUMN COUNT PROGRESSION

```
Stage               | Columns | New Additions
--------------------|---------|----------------------------------
INPUT (tracked)     |   7     | Base data
After Clean         |   7     | (stimulus columns cleaned in-place)
After Features      |  11     | +4: Position_X/Y, Speed, Motion
After Layer1        |  12     | +1: Layer1
After Layer1_Den    |  14     | +2: Speed_Denoised, Layer1_Denoised
After Layer2        |  15     | +1: Layer2
After Layer2_Den    |  16     | +1: Layer2_Denoised
After Resistant     |  18     | +2: Resistant, Resistant_Denoised
After Behavior      |  20     | +2: Behavior, Behavior_Denoised
After Alignment     |  17     | -3: Crop to experimental periods
OUTPUT (scored)     |  17     | Final published columns
```

---

## 🎯 KEY DECISION POINTS

1. **Pre-flight QC**: FAIL → Error folder, STOP
2. **SLEAP available?**: YES → Pose scoring, NO → Skip
3. **Post-class QC**: FLAG → Flag folder, but CONTINUE
4. **All success**: Publish to Scored/ folder

---

## ⚙️ CRITICAL PARAMETERS

```python
# Speed thresholds
HIGH_SPEED = 75 mm/s      # Jump threshold
LOW_SPEED = 4 mm/s        # Walk/Stationary boundary

# Denoising
NOISE_TOLERANCE = frames  # Micro-bout deletion threshold
SPEED_DENOISE_AVG_WINDOW_SEC = 0.5  # Speed smoothing window
LAYER2_AVG_WINDOW_SEC = 0.1         # Voting window

# Gap filling
MAX_NAN_BOUT_CLEAN_SEC = 1.0  # Max gap to fill
SKIP_RESPONSE_WINDOW = True   # Don't fill near stimuli

# Resistant detection
STARTLE_PRE_STIM_SEC = 1.0   # Coverage before stim
STARTLE_POST_STIM_SEC = 1.0  # Coverage after stim
```

---

## 🏗️ MODULE RESPONSIBILITIES

| Module | Responsibility |
|--------|---------------|
| **BC_UTILS** | Stimulus cleaning, geometry, motion, pose, I/O |
| **BC_CLASSIFIER** | All 5 classification layers + resistant + behavior |
| **BC_QC** | Pre-flight errors + post-class flags + reports |
| **BC_MAIN** | Orchestration, discovery, progress, error handling |
| **BC_COLAB** | Colab adapter, Mixed PATH mode |

---

**Visual Reference Complete** ✅

