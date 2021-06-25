import cv2
import mediapipe as mp
import pyautogui
from gaze_tracking import GazeTracking
import time





def main():
        
    screen_x, screen_y = pyautogui.size()
    print(f"screen_x {screen_x}")
    print(f"screen_y {screen_y}")

    # pyautogui.moveTo(0, 0)



    gaze = GazeTracking()

    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture("20210624_043009.mp4")

    not_out_of_bound = False

    calibrate = False
    calibrate_count = 0

    calibrate_xmin = 0
    calibrate_xmax = 0
    calibrate_ymin = 0
    calibrate_ymax = 0

    # hard code for face
    calibrate = True
    calibrate_xmin = 0.35323383084577115
    calibrate_xmax = 0.5980392156862745
    calibrate_ymin = 0.19607843137254902
    calibrate_ymax = 0.27522935779816515

    # # hard code for eyes
    # calibrate = True
    # calibrate_xmin = 0.4805194805194805
    # calibrate_xmax = 0.5497835497835498
    # calibrate_ymin = 0.2217391304347826
    # calibrate_ymax = 0.24782608695652175

    calibrate_x_range = 0
    calibrate_y_range = 0


    old_timestamp = time.time() * 1000000


    pixel_xmin_box_in = None
    pixel_xmax_box_in = None
    pixel_ymin_box_in = None
    pixel_ymax_box_in = None

    pixel_xmin_box_out = None
    pixel_xmax_box_out = None
    pixel_ymin_box_out = None
    pixel_ymax_box_out = None

    pixel_xmin_crop = None
    pixel_xmax_crop = None
    pixel_ymin_crop = None
    pixel_ymax_crop = None


    


    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("can not read")
                break

            frame = cv2.flip(frame, 1)
            original_frame = frame.copy()

            cam_y, cam_x, chanel = frame.shape

            
            wk = cv2.waitKey(1)

            move_box = False


            

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = face_detection.process(image)

            # Draw the face detection annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            # print(image.shape)
            # print(f"x : {x} | y : {y}")
            # print("--------------------------------------")
            if results.detections:
                detection = results.detections[0]
                # print(detection)
                # print(detection.location_data.relative_bounding_box)

                pixel_xmin = cam_x * detection.location_data.relative_bounding_box.xmin
                pixel_xmax = cam_x * (detection.location_data.relative_bounding_box.width + detection.location_data.relative_bounding_box.xmin)

                pixel_ymin = cam_y * detection.location_data.relative_bounding_box.ymin
                pixel_ymax = cam_y * (detection.location_data.relative_bounding_box.height + detection.location_data.relative_bounding_box.ymin)

                # print(f"pixel_xmin:{pixel_xmin} | pixel_ymin:{pixel_ymin}")
                # print(f"pixel_xmax:{pixel_xmax} | pixel_ymax:{pixel_ymax}")

                # mp_drawing.draw_detection(image, detection)

                # check frame box
                if(
                    pixel_xmin_box_in == None and
                    pixel_xmax_box_in == None and
                    pixel_ymin_box_in == None and
                    pixel_ymax_box_in == None and
                    pixel_xmin_box_out == None and
                    pixel_xmax_box_out == None and
                    pixel_ymin_box_out == None and
                    pixel_ymax_box_out == None
                ):
                    pixel_xmin_box_in = pixel_xmin + (cam_x * 0.025)
                    pixel_xmax_box_in = pixel_xmax - (cam_x * 0.025)
                    pixel_ymin_box_in = pixel_ymin + (cam_y * 0.025)
                    pixel_ymax_box_in = pixel_ymax - (cam_x * 0.025)
                    
                    pixel_xmin_box_out = pixel_xmin - (cam_x * 0.025)
                    pixel_xmax_box_out = pixel_xmax + (cam_x * 0.025)
                    pixel_ymin_box_out = pixel_ymin - (cam_y * 0.025)
                    pixel_ymax_box_out = pixel_ymax + (cam_x * 0.025)

                    pixel_xmin_crop = pixel_xmin
                    pixel_xmax_crop = pixel_xmax
                    pixel_ymin_crop = pixel_ymin
                    pixel_ymax_crop = pixel_ymax


                # update box
                if(
                    pixel_xmin > pixel_xmin_box_in or
                    pixel_xmax < pixel_xmax_box_in or
                    pixel_ymin > pixel_ymin_box_in or
                    pixel_ymax < pixel_ymax_box_in or
                    pixel_xmin < pixel_xmin_box_out or
                    pixel_xmax > pixel_xmax_box_out or
                    pixel_ymin < pixel_ymin_box_out or
                    pixel_ymax > pixel_ymax_box_out
                ):
                    pixel_xmin_box_in = pixel_xmin + (cam_x * 0.025)
                    pixel_xmax_box_in = pixel_xmax - (cam_x * 0.025)
                    pixel_ymin_box_in = pixel_ymin + (cam_y * 0.025)
                    pixel_ymax_box_in = pixel_ymax - (cam_x * 0.025)

                    pixel_xmin_box_out = pixel_xmin - (cam_x * 0.025)
                    pixel_xmax_box_out = pixel_xmax + (cam_x * 0.025)
                    pixel_ymin_box_out = pixel_ymin - (cam_y * 0.025)
                    pixel_ymax_box_out = pixel_ymax + (cam_x * 0.025)

                    pixel_xmin_crop = pixel_xmin
                    pixel_xmax_crop = pixel_xmax
                    pixel_ymin_crop = pixel_ymin
                    pixel_ymax_crop = pixel_ymax


                    



                pixel_xmin = int(pixel_xmin)
                pixel_xmax = int(pixel_xmax)
                pixel_ymin = int(pixel_ymin)
                pixel_ymax = int(pixel_ymax)
                
                pixel_xmin_crop = int(pixel_xmin_crop)
                pixel_xmax_crop = int(pixel_xmax_crop)
                pixel_ymin_crop = int(pixel_ymin_crop)
                pixel_ymax_crop = int(pixel_ymax_crop)
                
                pixel_xmin_box_in = int(pixel_xmin_box_in)
                pixel_xmax_box_in = int(pixel_xmax_box_in)
                pixel_ymin_box_in = int(pixel_ymin_box_in)
                pixel_ymax_box_in = int(pixel_ymax_box_in)
                
                pixel_xmin_box_out = int(pixel_xmin_box_out)
                pixel_xmax_box_out = int(pixel_xmax_box_out)
                pixel_ymin_box_out = int(pixel_ymin_box_out)
                pixel_ymax_box_out = int(pixel_ymax_box_out)
                
                not_out_of_bound = pixel_xmin_crop >= 0 and pixel_xmax_crop <= cam_x-1 and pixel_ymin_crop >= 0 and pixel_ymax_crop <= cam_y-1
                if not_out_of_bound:
                    cv2.rectangle(image, (pixel_xmin, pixel_ymin), (pixel_xmax, pixel_ymax), (0,0,255), 1)
                    cv2.rectangle(image, (pixel_xmin_crop, pixel_ymin_crop), (pixel_xmax_crop, pixel_ymax_crop), (0,255,255), 1)
                    cv2.rectangle(image, (pixel_xmin_box_in, pixel_ymin_box_in), (pixel_xmax_box_in, pixel_ymax_box_in), (0,255,0), 1)
                    cv2.rectangle(image, (pixel_xmin_box_out, pixel_ymin_box_out), (pixel_xmax_box_out, pixel_ymax_box_out), (255,0,0), 1)
                    # cv2.circle(image, (pixel_xmin, pixel_ymin), radius=10, color=(225, 0, 100), thickness=1)


            if results.detections and not_out_of_bound:
                # iris detection
                # face_img = original_frame.copy()[pixel_ymin:pixel_ymax, pixel_xmin:pixel_xmax, :]
                face_img = original_frame.copy()[pixel_ymin_crop:pixel_ymax_crop, pixel_xmin_crop:pixel_xmax_crop, :]
                # face_img = cv2.blur(face_img, (7,7))


                # face_img = original_frame.copy()
                gaze.refresh(face_img)
                left_pupil = gaze.pupil_left_coords()
                right_pupil = gaze.pupil_right_coords()
                
                face_y, face_x, _ = face_img.shape
                # print(f"face_img.shape {face_img.shape}")

                # iris control mouse
                if left_pupil is not None and right_pupil is not None:
                    left_pupil_norm_x = (left_pupil[0] / face_x)
                    left_pupil_norm_y = (left_pupil[1] / face_y)
                    
                    right_pupil_norm_x = (right_pupil[0] / face_x)
                    right_pupil_norm_y = (right_pupil[1] / face_y)

                    mean_pupil_x = (left_pupil[0] + right_pupil[0]) / 2
                    mean_pupil_y = (left_pupil[1] + right_pupil[1]) / 2
                    # print(f"{mean_pupil_x} | {mean_pupil_y}")
                    
                    # draw circle midle eyes
                    mean_pupil_x = int(mean_pupil_x)
                    mean_pupil_y = int(mean_pupil_y)
                    cv2.circle(face_img, (mean_pupil_x, mean_pupil_y), radius=5, color=(0, 0, 255), thickness=1)

                    mean_pupil_norm_x = mean_pupil_x / face_x
                    mean_pupil_norm_y = mean_pupil_y / face_y
                    # print(f"X {mean_pupil_norm_x} | Y {mean_pupil_norm_y}")

                    # print(left_pupil)
                    # print(f"{left_pupil_norm_x} | {left_pupil_norm_y}")

                    

                    # move mouse
                    if calibrate:
                        # mouse_x = screen_x * left_pupil_norm_x
                        # mouse_y = screen_y * left_pupil_norm_y

                        

                        calibrate_box_xmin = int(calibrate_xmin * face_x)
                        calibrate_box_xmax = int(calibrate_xmax * face_x)
                        calibrate_box_ymin = int(calibrate_ymin * face_y)
                        calibrate_box_ymax = int(calibrate_ymax * face_y)


                        # draw calibrate box
                        cv2.rectangle(face_img, (calibrate_box_xmin, calibrate_box_ymin), (calibrate_box_xmax, calibrate_box_ymax), (0,0,255), 1)

                        calibrate_x_range_norm_to_zero = mean_pupil_norm_x - calibrate_xmin
                        calibrate_y_range_norm_to_zero = mean_pupil_norm_y - calibrate_ymin

                        # print(f"x {calibrate_x_range_norm_to_zero} | y {calibrate_y_range_norm_to_zero}")
                        

                        calibrate_x_range_norm = calibrate_x_range_norm_to_zero / (calibrate_xmax - calibrate_xmin)
                        calibrate_y_range_norm = calibrate_y_range_norm_to_zero / (calibrate_ymax - calibrate_ymin)

                        # print(f"x {calibrate_x_range_norm} | y {calibrate_y_range_norm}")

                        # calibrate_x_range_norm = int(calibrate_x_range_norm)
                        # calibrate_y_range_norm = int(calibrate_y_range_norm)

                        # mouse_x = screen_x * mean_pupil_norm_x
                        # mouse_y = screen_y * mean_pupil_norm_y
                        
                        mouse_x = screen_x * calibrate_x_range_norm
                        mouse_y = screen_y * calibrate_y_range_norm

                        mouse_x = int(mouse_x)
                        mouse_y = int(mouse_y)


                        # map range value
                        if mouse_x < 1:
                            mouse_x = 1
                        if mouse_x > screen_x:
                            mouse_x = screen_x - 1

                        if mouse_y < 1:
                            mouse_y = 1
                        # if mouse_y > screen_y:
                        #     mouse_y = screen_y - 1
                        if mouse_y > 1040:
                            mouse_y = 1040 - 1

                        # print(f"mouse_x : {mouse_x} | screen_y : {mouse_y}")

                        pyautogui.moveTo(mouse_x, mouse_y)
                        if gaze.is_blinking():
                            

                            new_timestamp = time.time() * 1000000
                            distance_timestamp = new_timestamp - old_timestamp
                            old_timestamp = new_timestamp
                            print(f"blinking {distance_timestamp}")
                            if distance_timestamp < 1000000:
                                print("Click !")
                                pyautogui.click(button='left')
                                pass

                    else:
                        if wk == 32:

                            if calibrate_count == 0:
                                calibrate_xmin = mean_pupil_norm_x
                            elif calibrate_count == 1:
                                calibrate_xmax = mean_pupil_norm_x
                            elif calibrate_count == 2:
                                calibrate_ymin = mean_pupil_norm_y
                            elif calibrate_count == 3:
                                calibrate_ymax = mean_pupil_norm_y

                                
                            if calibrate_count >= 3:
                                calibrate = True
                            calibrate_count += 1
                            print(f"{calibrate_count} : calibrate_xmin {calibrate_xmin} | calibrate_xmax {calibrate_xmax} | calibrate_ymin {calibrate_ymin} | calibrate_ymax {calibrate_ymax}")
                            
                            if calibrate:
                                calibrate_x_range = calibrate_xmax - calibrate_xmin
                                calibrate_y_range = calibrate_ymax - calibrate_ymin
                                print("________________________________________________________________________")
                            
                        elif wk == 8 or wk == ord("a"):

                            calibrate_count -= 1
                            if calibrate_count < 0:
                                calibrate_count = 0

                            if calibrate_count == 0:
                                calibrate_xmin = 0
                            elif calibrate_count == 1:
                                calibrate_xmax = 0
                            elif calibrate_count == 2:
                                calibrate_ymin = 0
                            elif calibrate_count == 3:
                                calibrate_ymax = 0


                            print(f"{calibrate_count} : calibrate_xmin {calibrate_xmin} | calibrate_xmax {calibrate_xmax} | calibrate_ymin {calibrate_ymin} | calibrate_ymax {calibrate_ymax}")
                    

            
                    
            cv2.imshow('main', image)
            # cv2.imshow("ts", ts)

            if not_out_of_bound:
                face_img = gaze.annotated_frame()
                cv2.imshow('face', face_img)
            
            if wk == ord("s"):
                calibrate_count = 0

                calibrate_xmin = 0
                calibrate_ymin = 0
                calibrate_xmax = 0
                calibrate_ymax = 0
                
                calibrate = False

            if wk == 27 or wk == ord("q"):
                break
            # if cv2.waitKey(1) & 0xFF == 27:
            #     break
    cap.release()


if __name__ == "__main__":
    main()