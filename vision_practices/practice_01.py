import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import numpy.typing as npt
import itertools
import tqdm
import rerun as rr

class GestureDetectorLogger:
    def __init__(self,video_mode: bool = False):
        self._video_mode = video_mode

        base_options = python.BaseOptions(
            model_asset_path = "gesture_recognizer.task"
        )

        options = vision.GestureRecognizerOptions(
            base_options = base_options,
            running_mode = mp.tasks.vision.RunningMode.VIDEO if self._video_mode else mp.tasks.vision.RunningMode.IMAGE
        )
        self.recognizer = vision.GestureRecognizer.create_from_options(options)

        rr.log(
            "/",
            rr.AnnotationContext(
                rr.ClassDescription(
                    info = rr.AnnotationInfo(id = 0, label = "Hand3D"),
                    keypoint_connections = mp.solutions.hands.HAND_CONNECTIONS
                )
            ),
            
        )
        rr.log("Hand3D", rr.ViewCoordinates.RIGHT_HAND_X_DOWN)

    def detect(self, image: npt.NDArray[np.uint8]) -> None:
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data = image)
        recognition_result = self.recognizer.recognize(image)

        for i, gesture in enumerate (recognition_result.gestures):
            # Get the top gesture from the recognition result
            print("Top gesture Result: ", gesture[0].category_name)
        if recognition_result.hand_landmarks:
            # Obtain hand landmarks from MediaPipe
            hand_landmarks = recognition_result.hand_landmarks
            print("Hand Landmarks: " + str(hand_landmarks))

            #obtain hand connections from MediaPipe
            mp_hands_connections = mp.solutions.hands.HAND_CONNECTIONS
            print("Hand Connections: " + str(mp_hands_connections))

    def convert_landmarks_to_image_coordinates(self, hand_landmarks, width, height):
        return [(int(lm.x * width), int(lm.y * height)) for hand_landmark in hand_landmarks for lm in hand_landmark]
    
    def detect_and_log(self, image:npt.NDArray[np.uint8], frame_time_nano : int | None ) -> None : 
        #Recognize gestures in the image
        height, width, _ = image.shape
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data = image)

        recognition_result = (
            self.recognizer.recognize_for_video(image,int(frame_time_nano / 1e6))
            if self._video_mode
            else self.recognizer.recognize(image)
        )


        for i, gestures in enumerate(recognition_result.gestures):
            #Get the top gesture from the recognition
            gesture_category = gestures[0].category_name if recognition_result.gestures else "None"
            print("Gesture category: ", gesture_category)

        if recognition_result.hand_landmarks:
            hand_landmarks = recognition_result.hand_landmarks

            points = self.convert_landmarks_to_image_coordinates(hand_landmarks, width, height)
            # Log points to the image and hand entity
            rr.log(
                "Media/video/points",
                rr.Points2D(points, radii = 10, colors = [255,0,0])
            )              

            #Obtain hand connections from MediaPipe
            mp_hands_connections = mp.solutions.hands.HAND_CONNECTIONS
            points0 = [points[connection[0]] for connection in mp_hands_connections]
            points1 = [points[connection[1]] for connection in mp_hands_connections]

            #Log connections to the image and hand entity

            rr.log(
                "Media/video/connections",
                rr.LineStrips2D(
                    np.stack((points0, points1),axis=1),
                    colors = [255,165,0]
                )
            ) 
        else:
            rr.log("Media/video/points", rr.Clear(recursive = True))
            rr.log("Media/video/connections", rr.Clear(recursive = True))


def run_from_video_capture (vid : int | str, max_frame_count: int | None) -> None:
    """
    RUn the detector on avideo stream.

    parameters
    ---------

    vid: 
        the video stream to run the detector on. use 0/1 for the default camera
    max_frame_count: 
        the maximum numberof frames to process. if None, process al frames
    """

    cap = cv2.VideoCapture(vid)
    fps = cap.get(cv2.CAP_PROP_FPS)

    detector = GestureDetectorLogger(video_mode = True)

    try:
        it: Iterable[int] = itertools.count() if max_frame_count is None else range(max_frame_count)

        for frame_idx in tqdm.tqdm(it, desc="Processing frames"):
            ret, frame = cap.read()
            if not ret:
                break
            if np.all(frame == 0):
                continue

            frame_time_nano = int(cap.get(cv2.CAP_PROP_POS_MSEC) * 1e6)
            if frame_time_nano == 0:
                frame_time_nano = int(frame_idx * 1000 / fps * 1e6)

            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

#            rr.set_time_sequence("frame_nr",frame_idx)
#            rr.set_time_nanos("frame_time", frame_time_nano)
            detector.detect_and_log(frame,frame_time_nano)
            rr.log(
                "Media/video",
                rr.Image(frame)
            )
    except KeyboardInterrupt:
        pass

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    
    rr.init("Gesture_Recognition", spawn =True)
    run_from_video_capture(0,None)