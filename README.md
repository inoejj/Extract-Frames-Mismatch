# Extract-Frames-Mismatch

This script compares the classifier that a human scored and the machine's prediction and extract the frames when there is a disagreement. Then a human can look at the extracted frames to judge if there is a human error or machine error.

As you can see below there are two gifs. The red dot shows when there is a disagreement. Who do you think is correct? The machine or the human scorer? 

### Random forest prediction
![Computer Prediction](/images/video1_computer_prediction.gif)

### Human scoring
![Human Scoring](/images/Video2_no_frameHuman Prediction.gif)

## Tutorial

1. First go to [https://osf.io/jnsft/](https://osf.io/jnsft/) to download the sample .csv file and the videos.

2. Run the script.

3. The script will generate frames from the video where the labeled data and machine's prediction does not match.
