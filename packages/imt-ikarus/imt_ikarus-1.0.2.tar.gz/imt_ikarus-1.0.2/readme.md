# `IKArus` <ins>I</ins>nertial and Optical Data of <ins>K</ins>inematic Ch<ins>A</ins>in Motion

This repository hosts the `Ikarus` dataset.
It contains *real-world* IMU and OMC data from kinematic chain motion.

![](imgs/pose1_noBG.png)

It contains:
- `dataset/*`: the preprocessed dataset
- `preprocess/*`: unpreprocessed data and preprocessing logic to re-create the `dataset` folder
- `src/*`: a Python Package that 
    - provides convenient access to the data from a Python environment
    - defines benchmarks
    - defines baselines

## `dataset/*`
There exist two different five-segment kinematic chains, namely `arm` and `gait`.
The two five-segment kinematic chains differ in types of joints in the setup.
- `arm`: S(egment)1 - *1D joint* (Z) - S2 - *1D joint* (Y) - S3 -  *1D joint* (X) - S4 - *3D joint* - S5
- `gait`: S2 - *1D joint* (Y) - S3 - *2D joint* - S4 - *2D joint* - S5 -  *1D joint* (Y) - S1

For each of the two kinematic chains several experiments `expX` (recordings) have been performed. An experiment is one continous recording of IMU and OMC data whilst the kinematic chain is moving.

Each experiment contains several different types of motions `motionY`, such as, e.g., fast motion, slow motion, standstills...

The motions are from one continous experiment and are ordered chronologically. As a result, two (or more) motions, e.g., `motion01` and `motion02` can be concatenated to create one longer continous timeseries.

The dataset folder hierarchy is structured in this way:

```
dataset
├── arm
│   ├── exp01
│   │   ├── motion01_canonical
│   │   │   ├── exp01_motion01_imu_nonrigid.csv
│   │   │   ├── exp01_motion01_imu_rigid.csv
│   │   │   └── exp01_motion01_omc.csv
│   │   ├── motion02_pause1
│   │   ├── motion03_slow1
│   │   ├── motion04_pause2
│   │   ├── motion05_fast
│   │   ├── motion06_pause3
│   │   ├── motion07_fast_slow_fast
│   │   ├── motion08_freeze1
│   │   ├── motion09_fast_slow
│   │   ├── motion10_freeze2
│   │   ├── motion11_slow2
│   │   ├── motion12_shaking
│   │   └── motion13_pause4
│   ├── exp02
│   ├── exp03
│   ├── exp04
│   └── exp05
├── gait
│   ├── exp06
│   ├── exp07
│   ├── exp08
│   ├── exp09
│   ├── exp10
│   └── exp11
```

For each experiment `expX` and `motionY` the folder `armOrGait/expX/motionY` contains three files:
- `expX_motionY_imu_nonrigid.csv`: The acc/gyr/mag measurements of five IMUs where each IMU is *nonrigidly* attached to the respective segment.
- `expX_motionY_imu_rigid.csv`: The acc/gyr/mag measurements of five IMUs where each IMU is *rigidly* attached to the respective segment.
- `expX_motionY_omc.csv`: For each of the five segments, four 3D marker positions and the absolute orientation as a quaternion.

All `.csv` files contain the respective sampling frequency (e.g. 40 Hz) as the first line:
```csv
# sampling frequency: 40
```

The header of, e.g. `expX_motionY_imu_rigid.csv`, starts with:
```csv
seg1_acc_x,seg1_acc_y,seg1_acc_z,seg1_gyr_x,seg1_gyr_y,seg1_gyr_z,seg1_mag_x,seg1_mag_y,seg1_mag_z, ...
```

> [!IMPORTANT]  
> The identifiers of the segments for `arm` are: `seg1` - `seg2` - `seg3` - `seg4` - `seg5`, and for `gait` are: `seg2` - `seg3` - `seg4` - `seg5` - `seg1`

The identifiers of the markers (M1 to M4) for the five segments (S1 to S5) can be read of from the following figure

![](imgs/marker_numbering_arm.png)


## `preprocess/*`
Refer to the readme in the subfolder.

## `src/*`
Requires Python 3.10 or higher.

The Python Package allows convenient access to the data and can be installed with
> pip install imt-ikarus

Note that the Python Package will automatically download the required data on-demand. By default it comes with no data at all and there is no data stored in a redundant way.

### Quickstart
```python
import ikarus

# concatenates 3 motions: the motion01, motion02 and motion03 
data = ikarus.load_data(
    exp_id         = 1,
    motion_start   = 1,
    motion_stop    = 3,
    resample_to_hz = 100
)

print(data.keys())
# ['seg1', 'seg2', 'seg3', 'seg4', 'seg5']

print(data['seg1'].keys())
# ['imu_rigid', 'imu_nonrigid', 'marker1', 'marker2', 'marker3', 'marker4', 'quat']

print(data['seg1']['imu_rigid'].keys())
# ['acc', 'gyr', 'mag']
```
