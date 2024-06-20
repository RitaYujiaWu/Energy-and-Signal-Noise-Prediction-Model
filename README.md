# Energy-and-Signal-Noise-Prediction-Model
(This is a project for DSC40A at UCSD)  
  
High-Purity Germanium (HPGe) detector is one of the most sensitive detectors human beings have ever manufactured. It is sensitive in the sense that it measures the energy of elementary particles (electrons, photons, etc) very accurately. Because of this, HPGe detectors have a wide range of applications, including the search for neutrinos and dark matter, medical imaging, as well as nuclear non-proliferation.  
When a particle comes into the HPGe detector, it produces a waveform, or time series data, as shown in the picture below. A time series is a sequence of data points that occur in successive order over some period of time. More formally, we can define time series this way: for each data point, a time series contains n pairs of ti, ai where ti is the ith time sample and ai is the value at the ith time sample. To simplify this problem, we extract certain features from the HPGe time series to build **two prediction models**:
 - Find the best prediction rule using regression to estimate the energy of each HPGe detector waveform.
 - Produce a ”classification score” for each HPGe detector waveform, for which the signal data point (data point with a label of 1) should have a higher score than the noise data point (data point with a label of 0).
![HPGe img](https://github.com/RitaYujiaWu/Energy-and-Signal-Noise-Prediction-Model/blob/main/img.png)
  
We are given access to two separate CSV files:   
1. `HPGeData.csv` A CSV containing training data with information about 400 elementary particles which deposit their energy in an HPGe detector. We read this in as a DataFrame where the columns are different parameters. The columns are:

| Column              | Description                                                                                                                                                                    |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `tDrift50`          | Period from the Start of Rise (t<sub>SR</sub>) to when the waveform reaches 50% of Max Amp (t<sub>50</sub>), can also be written as t<sub>50</sub> − t<sub>SR</sub>.           |
| `tDrift90`          | Period from the Start of Rise (t<sub>SR</sub>) to when the waveform reaches 90% of Max Amp (t<sub>90</sub>), can also be written as t<sub>90</sub> − t<sub>SR</sub>.           |
| `tDrift100`         | Period from the Start of Rise (t<sub>SR</sub>) to when the waveform reaches Max Amp, can also be written as t<sub>MAXAMP</sub> − t<sub>SR</sub>.                               |
| `blnoise`           | The standard deviation of amplitude values a<sub>i</sub> in the green-colored region.                                                                                          |
| `tslope`            | The slope of the waveform tail.                                                                                                                                                |
| `Max_Amp`           | Maximum amplitude of the waveform, or the largest number among all a<sub>i</sub>s                                                                                              |
  
2. `training_classification.csv` A CSV containing training data with information about 3000 elementary particles which deposit their energy in an HPGe detector. Some of them are signal-like, i.e. they exhibit the same shape with neutrinoless double-beta decay, others are noise-like, i.e. they look different from neutrinoless double-beta decay. This is a labeled dataset where signal-like data has a label of 1 and background-like data has a label of 0. We read this as a DataFrame where the columns are different parameters. The columns are:

| Column              | Description                                                                                                                                                                    |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `tDrift50`          | Period from the Start of Rise (t<sub>SR</sub>) to when the waveform reaches 50% of Max Amp (t<sub>50</sub>), can also be written as t<sub>50</sub> − t<sub>SR</sub>.           |
| `tDrift90`          | Period from the Start of Rise (t<sub>SR</sub>) to when the waveform reaches 90% of Max Amp (t<sub>90</sub>), can also be written as t<sub>90</sub> − t<sub>SR</sub>.           |
| `tDrift100`         | Period from the Start of Rise (t<sub>SR</sub>) to when the waveform reaches Max Amp, can also be written as t<sub>MAXAMP</sub> − t<sub>SR</sub>.                               |
| `blnoise`           | The standard deviation of amplitude values a<sub>i</sub> in the green-colored region.                                                                                          |
| `tslope`            | The slope of the waveform tail.                                                                                                                                                |
| `Energy`            | The energy of each waveform, i.e. the target of the previous challenge.                                                                                                        |
| `Current Amplitude` | A new parameter extracted from the waveform, by taking a derivative of the waveform and reading out the maximum of the derivative.                                             |


