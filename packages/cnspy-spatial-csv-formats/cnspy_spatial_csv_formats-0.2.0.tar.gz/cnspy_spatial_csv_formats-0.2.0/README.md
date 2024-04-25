# cnspy_spatial_csv_formats Package

This package holds header and format definitions for [CSV-files](https://en.wikipedia.org/wiki/Comma-separated_values) that hold timestamped 3D **spatial** information. 
By **spatial** 
- 3-DoF relative position (), 
- 3-DoF attitude , 
- 6-DoF pose (position + orientation represented by quaternions in the [qx qy qz qw] order)
- 3-DoF position and 3-DoF orientation with uncertainty (position and orientation uncertainties is given by two 3x3 upper triangular covariance matrices). **TODO: make default assumption on the uncertainty space**
- 3-DoF position and 3-DoF orientation with **typed** uncertainty (position and orientation uncertainties is given by two 3x3 upper triangular covariance matrices) [1*]. 
- 6-DoF pose with upper triangular pose uncertainty. **TODO: make default assumption on the uncertainty space**
- 6-DoF pose with upper triangular pose  **typed** uncertainty  [1*] .

[1*] Typed uncertainty: The space/reference frame of the covariance is specified by the "est_err_type" and "err_representation" entry. In case of an error-state estimator, the error representation of the orientation needs to be specified in the CSV files. The estimation error types are defined in the [EstimationErrorType](./cnspy_spatial_csv_formats/EstimationErrorType.py) file. The error representation type is defined in the [ErrorRepresentationType](./cnspy_spatial_csv_formats/ErrorRepresentationType.py) file. 


Orientation are represented by quaternions in the [qx qy qz qw] order, meaning that the real-part appears at the end aka JPL order.

File headers are in the first line of a CSV file **should not** start with a `#`, followed by a sequence of unique comma separated strings/chars. 

It is highly recommended loading the CSV files into a [pandas.DataFrame](https://pypi.org/project/pandas/). For convenience, there is a package called [cnspy_csv2dataframe](https://github.com/aau-cns/cnspy_csv2dataframe) that does the conversion using the [CSVFormatPose](CSVFormatPose.py) definitions.


## Note

The [CSVFormatPose.TUM](./cnspy_spatial_csv_formats/CSVSpatialFormatType.py) format, got it's name for file format used in the [TUM RGB-D benchmark tool](https://vision.in.tum.de/data/datasets/rgbd-dataset/tools#evaluation). Noticeable, is that the order of quaternion is non-alphabetically (`[q_x,q_y,q_z, q_w]` instead of `[q_w, q_x, q_y, q_z]`), meaning that first comes the imaginary part, then the real part, but this is just a matter of taste and definition! To be backward compatible with older/other tools ([TUM RGB-D benchmark tool](ttps://vision.in.tum.de/data/datasets/rgbd-dataset/tools#evaluation), [rpg_trajectory_evaluation](https://github.com/uzh-rpg/rpg_trajectory_evaluation), etc.), we follow this non-alphabetically order!
Note that the  [rpg_trajectory_evaluation](https://github.com/uzh-rpg/rpg_trajectory_evaluation) framework is based on `space-separated`  `*.txt` trajectory files, meaning that these files cannot be directly processed in the current framework as the file header cannot be interpreted correctly. Support may be added in future.   

## Installation

Install the current code base from GitHub and pip install a link to that cloned copy
```
git clone https://github.com/aau-cns/spatial_csv_formats.git
cd spatial_csv_formats
pip install -e .
```
or the [official package](https://pypi.org/project/cnspy-spatial-csv-formats/) via
```commandline
pip install cnspy-spatial-csv-formats
```


## Dependencies

It is part of the [cnspy eco-system](hhttps://github.com/aau-cns/cnspy_eco_system_test) of the [cns-github](https://github.com/aau-cns) group.  

* [enum]()

## License


Software License Agreement (GNU GPLv3  License), refer to the LICENSE file.

*Sharing is caring!* - [Roland Jung](https://github.com/jungr-ait)
