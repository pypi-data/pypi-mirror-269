# Robocon Ball Detection and Decision Making

This project is designed to detect balls and make decisions based on their positions in the context of a Robocon competition.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](https://github.com/mariswarycharan/Robocon_24_version/blob/main/LICENSE)

## Introduction

Robocon Ball Detection and Decision Making is a Python project that utilizes computer vision techniques to detect balls and analyze their positions. The main goal is to aid in decision-making processes, especially in scenarios such as Robocon competitions where precise understanding of the game environment is crucial.

## Features

- Ball detection using YOLO (You Only Look Once) object detection model.
- Decision-making algorithm based on the positions of detected balls and predefined rules.
- Visualization of detected balls and decision outcomes.

## Installation

To use this project, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/mariswarycharan/Robocon_24_version.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the project:

   ```bash
    from Robocon_24 import decision_maker
    import cv2

    image = cv2.imread(r'sample.jpg')

    final_decision, result_image = decision_maker(image)

    print(final_decision)

    cv2.imshow('Result',result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
   ```

