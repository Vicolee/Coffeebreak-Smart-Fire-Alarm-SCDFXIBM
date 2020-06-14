# Coffeebreak-SFA_SCDFXIBM

## Contents

1. [Short description](#short-description)
1. [Video](#video)
1. [The architecture](#the-architecture)
1. [Long description](#long-description)
1. [Getting started](#getting-started)
1. [Built with](#built-with)
1. [Contributing](#contributing)

## Short description

### Team details

Team name: Coffeebreak

Team members: 

* Alexander Gunawan
* Aloysius Wang
* Benjamin Lee
* Jasper Ong
* Vico Lee

### What's the problem?
* False alarms can be a major hazard to any fire alarm system for two main reasons:
  * Repeated false alarms reduce people’s trust in the sound-off system, reducing the sense of urgency during evacuation in life-threatening situations. 
  * Wastage of resources due to unnecessary allocation to the non-existent threats, curtailing SCDF’s ability to target real threats. 

### How can technology help?
* Sensors imbued with Internet-of-Things (IoT) technology can be integrated into existing fire alarm systems for smarter detection of potential fires.    

* Using state-of-the-art technology including deep neural networks and computer vision, we are able to better analyse data collected from these smart alarms.

* Our proposed detection system gathers important data from past threats to make predictions. This allows SCDF personnel to make informed decisions and formulate strategic plans to fight potential threats. 

* By using limited resources in a targeted and efficient way, SCDF is able to handle more situations in a given period of time 

### Our proposed solution

Deploying deep learning algorithms to analyse data from past fire alarms, we can more accurately judge the severity of fires given factors such as CO levels, smoke density, humidity and location. This will allow SCDF to make more informed decisions when allocating resources. 

## Video

[![Watch the video](video.jpg)](https://youtu.be/svXU00e7Pbs)

## The architecture

![architecture.png](https://github.com/jasperosy/Coffeebreak-Placeholder_SCDFXIBM/blob/master/architecture.png)

1. When the fire alarm rings, the sensors in the fire alarm will record environmental data, storing it in a backend database. 
2. Severity rating is determined by performing classification on environmental data. 
3. If the alarm is determined to be a false alarm, an announcement will be made. 
4. If a real fire has broken out, SCDF will be notified. Severity rating will be used to recommend an appropriate amount of resources that should be deployed to combat the emergency.  

## Long description

[More detail is available here](DESCRIPTION.md)

## Getting started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
Things you will need before running our code.
* Dataset
* 64-Bit Python 3
* Numpy
* Tensorflow

### Installing

**NOTE:**
The codes provided are skeletal codes in the absence of a valid dataset. For more details on the dataset, [click here](DESCRIPTION.md)
```bash
git clone https://github.com/jasperosy/Coffeebreak-SFA_SCDFXIBM.git
cd Coffeebreak-SFA_SCDFXIBM
pip install -r requirements.txt
python main.py
```

## Built with
* [IBM Watson Studio](https://cloud.ibm.com/catalog/services/watson-studio) - We used the computational resources available on Watson Studio.

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.
