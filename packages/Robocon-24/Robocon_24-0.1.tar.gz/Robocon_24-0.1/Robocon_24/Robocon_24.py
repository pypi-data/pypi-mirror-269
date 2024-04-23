from ultralytics import YOLO
import cv2

model = YOLO(r"models\best_2.pt")

def point_inside(rectangle, entire_coordinates):    
    x1, y1 ,x2, y2 , _ , _ = rectangle
    return (entire_coordinates[0] <= x1 <= entire_coordinates[2] and entire_coordinates[1] <= y1 <= entire_coordinates[3]) or (entire_coordinates[0] <= x2 <= entire_coordinates[2] and entire_coordinates[1] <= y2 <= entire_coordinates[3])

def decision_maker(image_input_def):
    global model

    # initial balls pattern
    balls_pattern = {'rack_1': {'blue_ball':0,'red_ball':0}, 
                    'rack_2': {'blue_ball':0,'red_ball':0}, 
                    'rack_3': {'blue_ball':0,'red_ball':0}, 
                    'rack_4': {'blue_ball':0,'red_ball':0}, 
                    'rack_5': {'blue_ball':0,'red_ball':0}}
    
    input_image = image_input_def
    
    # model prediction
    results = model.predict(input_image,conf = 0.3,classes = [0,1,2])

    # find the position of the detected balls
    balls_detected_condinates = list(filter( lambda x: x[-1] != 2.0, results[0].boxes.numpy().data.tolist()))
    # find the position of the detected silos
    detected_silo_condinates = sorted(list(filter( lambda x: x[-1] == 2.0, results[0].boxes.numpy().data.tolist())),key=lambda x: x[0])

    # allow only five silo is detected
    if len(detected_silo_condinates) == 5: 
        
        finded_balls_in_silo = {}
        
        # adding the no of blue and red balls in each silo in the dictionary
        for id,i in enumerate(detected_silo_condinates):
            l = []
            d = {}
            for j in balls_detected_condinates:
                res_inside = point_inside(j,i)
                if res_inside:
                    l.append((j[-1]))
            blue_ball_count = l.count(0.0)
            red_ball_count = l.count(1.0)
            d['blue_ball'] = blue_ball_count
            d['red_ball'] = red_ball_count
            finded_balls_in_silo["rack_" + str(id + 1)] = d
            
        # adding finded_balls_in_silo in actual balls pattern
        balls_pattern['rack_1'] = finded_balls_in_silo['rack_1']
        balls_pattern['rack_2'] = finded_balls_in_silo['rack_2']
        balls_pattern['rack_3'] = finded_balls_in_silo['rack_3']
        balls_pattern['rack_4'] = finded_balls_in_silo['rack_4']
        balls_pattern['rack_5'] = finded_balls_in_silo['rack_5']

        emtpy_racks = []
        my_ball_check_count = 0

        # finding empty racks
        for rack,ball_count in balls_pattern.items():
            if ball_count['blue_ball'] != 0:
                my_ball_check_count += 1
            if ball_count['red_ball'] == 0 and ball_count['red_ball'] == 0:
                emtpy_racks.append(rack)

        # removing completely filled in racks
        for rack,ball_count in list(balls_pattern.items()):
            total_ball_count_in_rack = ball_count['blue_ball'] + ball_count['red_ball']
            if total_ball_count_in_rack == 3:
                balls_pattern.pop(rack)

 
        max_ball_list = []
        
        # ------------------------------------- main rack logic -------------------------------------
        if len(emtpy_racks) == 0 or my_ball_check_count >= 3:
            
            # print("FIRST LOOP entered in after 3 ball placed in rack !!!!!!!!!!!!!!!!")
            
            for rack,ball_count in balls_pattern.items():
                count_my_ball = ball_count['blue_ball']
                count_opponent_ball = ball_count['red_ball']
                
                if count_my_ball == 1 and count_opponent_ball == 1:
                    sub_result = 2
                else:
                    sub_result = count_my_ball - count_opponent_ball
                # print(balls_pattern[rack], "m",count_my_ball,'o',count_opponent_ball)
                max_ball_list.append((rack,sub_result))
                
        # putting my ball in first three racks 
        if my_ball_check_count < 3 :
    
            # print("SECOND LOOP entered in before first 3 ball placed in rack !!!!!!!!!!!!!!!!")
            
            for rack,ball_count in balls_pattern.items():
                count_my_ball = ball_count['red_ball']
                count_opponent_ball = ball_count['blue_ball']
                
                if count_my_ball == 1 and count_opponent_ball == 1:
                    sub_result = 2
                    max_ball_list.append((rack,sub_result))
                
        if max_ball_list == []:
            keys_position = emtpy_racks[0]
        else:
            keys_position = max(max_ball_list, key=lambda x: x[1])[0]
            
    else:
        keys_position = 0        
        
    final_image_result  = results[0].plot()
    final_image_result = cv2.putText(final_image_result,str(keys_position),(450,400),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(255,0,0),thickness=1)
    return keys_position,final_image_result

