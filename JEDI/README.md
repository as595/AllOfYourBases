

JEDI Madagscar
===

*Requirements:*

Python 2.7

- numpy
- scipy
- matplotlib
- george 0.2.1
- celerite
- emcee
- autograd
- corner
- acor



Lecture: Gaussian Process Modelling in Python
---

This folder contains material for the STFC Data Intensive CDT Kick-Off lecture on GPM in Python. 

There are two iPython scripts to accompany the lecture:

 - GPMIntro.ipynb
 - GPMCarbonDioxide.ipynb
 
 These scripts use the input data set:
 
 - mauna_loa.dat
 
 You can also find the contents of these scripts described step-by-step here:
 
 - https://allofyourbases.com/2017/08/21/gaussian-processes-in-python/
 
 here:
 
 - https://allofyourbases.com/2017/09/04/gaussian-process-modelling-in-python/
 
 and here:
 
 - https://allofyourbases.com/2017/09/17/predicting-the-future/
 


Tutorial: Gaussian Process Modelling in Python
---

This folder contains material for the STFC Data Intensive CDT Kick-Off tutorial on GPM in Python. There are two levels of tutorial depending on Python proficiency. Both use the dataset KIC1430163.tbl.

Level: Beginner
- KeplerLightCurve.ipynb - uses the **george** (v0.2.1) GPM library

A step by step guide can also be found here: https://allofyourbases.com/2017/09/23/spinning-stars/

Level: Intermediate
- KeplerLightCurveCelerite.ipynb - uses the **celerite** GPM library; includes MCMC optimization of hyper-parameters

A step by step guide can also be found here: https://allofyourbases.com/2017/10/02/spinning-stars-ii-celerite/
