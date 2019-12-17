import pandas as pd
import os
import cv2

############ Get DataFrame #####################
df=pd.read_csv('SML_output.csv')
df=df[['RF prediction','Target','Frame_no','Video_no']]
#Narrow down to different
df.loc[df['RF prediction'] == df['Target'], 'Same_or_diff'] = True
df.loc[df['RF prediction'] != df['Target'], 'Same_or_diff'] = False
df=df.loc[df['Same_or_diff'] == False]
#To find the number of diff choice -->  df['Same_or_diff'].value_counts()

#dataframe where the random forest predicts an attack
df_RF=df.loc[(df['RF prediction'] == 1)]

#dataframe where the user predicts an attack
df_Target=df.loc[(df['Target'] == 1)]

#loop through random forest to create a list for every frames in every video
dfRFvideo={}
RF_list={}
df_RF_list=list(df_RF['Video_no'].unique())
for x in df_RF_list:
    dfRFvideo[x] = df.loc[(df['RF prediction'] == 1) & (df['Video_no']== x)]
    RF_list[x] = dfRFvideo[x]['Frame_no']
    RF_list[x]=(RF_list[x].tolist())

#loop through all video to generate frames

for i in df_RF_list:
    j = 0
    #Read the video from specified path
    vid = r"C:\Users\TheGoldenLab\Desktop\Extract_frames_mismatch\Video"+str(i)+r"_no_frame.mp4"
    vid_name=str(vid[-19:-4])+r"Computer Prediction"
    cam = cv2.VideoCapture(vid)
    try:
        # creating a folder named data
        if not os.path.exists(vid_name):
            os.makedirs(vid_name)

        # if not created then raise error
    except OSError:
        print('Error: Creating directory of data')


    while j < (len(RF_list[i])):

        target_frame = RF_list[i][j]
        print(target_frame)
        j+=1

        for count in range(target_frame - 25, target_frame + 25):
            fps = cam.get(cv2.CAP_PROP_FPS)
            frameCount = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = count / fps
            timeofevent=(target_frame-1)/fps
            mintime=(target_frame-50)/fps
            maxtime = (target_frame + 50) / fps
            minframe=target_frame-50
            maxframe=target_frame+50

            #to extract frames from video
            currentFrame = count
            cam.set(1, currentFrame)
            ret, frame = cam.read()
            name = './'+str(vid_name)+'/TargetFrame_'+str(target_frame) + 'frame_' + str(count) + '.jpg'
            print('Creating...' + name)
            cv2.imwrite(name, frame) #create video into folder

            #overlay details onto frame
            im = cv2.imread(name, 1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(im, 'Event ID: Random Forest thinks is an attack', (100, 150), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(im, 'Probability Frame(PF)'+str(target_frame), (100, 100), font, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(im, 'Video:'+str(vid[-19:-4]), (100, 50), font, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(im, 'Time bout:' + str(mintime)+'-'+str(maxtime), (100, 200), font, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(im, 'Frames:' + str(minframe) + '-' + str(maxframe), (100, 250), font, 0.8, (255, 0, 0), 2,cv2.LINE_AA)
            cv2.putText(im, 'Current Time:' + str(duration), (100, 300), font, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(im, 'Current Frames:' + str(currentFrame+1), (100, 350), font, 0.8, (255, 0, 0), 2,cv2.LINE_AA)

            cv2.imwrite(name, im)
            #highlight the target frame
            if count == (target_frame-1):
                im = cv2.imread(name, 1)
                cv2.circle(im, (500, 500), 63, (0, 0, 255), -1)
                cv2.imwrite(name, im)




cam.release()
cv2.destroyAllWindows()


print('Completed! The following are the target frames')

RF_list
