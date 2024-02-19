import cv2

def save_image( path, count ,image, bboxes, keypoints):
    image = cv2.cvtColor(image.copy(),cv2.COLOR_BGR2RGB)

    for bbox in bboxes:

        start_point = (bbox[0], bbox[1])
        end_point = (bbox[2], bbox[3])
        
        image = cv2.rectangle(image.copy(), start_point, end_point, (0, 0, 255), 5)
        image = cv2.putText(image.copy(), " " + str(start_point), 
                               start_point, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3, cv2.LINE_AA)
        image = cv2.putText(image.copy(), " " + str(end_point), 
                               end_point, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3, cv2.LINE_AA)

    for kps in keypoints:
         
        beak = kps[0]
        tail = kps[1]

        image = cv2.circle(image.copy(), beak, 1, (0, 255, 0), 5)
        image = cv2.putText(image.copy(), " " + str(beak),beak, 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3, cv2.LINE_AA)
        image = cv2.circle(image.copy(), tail, 1, (0, 255, 0), 5)
        image = cv2.putText(image.copy(), " " + str(tail),tail,
                             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3, cv2.LINE_AA)
    

    cv2.imwrite( str(path)+ '/PredictedImage'+ str(count) + '.jpg' , image )
        