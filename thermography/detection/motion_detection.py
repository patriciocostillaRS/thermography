import cv2
import numpy as np

from thermography.utils import scale_image

__all__ = ["MotionDetector"]


class MotionDetector:
    def __init__(self, scaling : float = 1.0):
        """
        Initializes the motion detector object.

        :param scaling: Scaling to apply to each frame passed to the function. This allows faster estimations of motion over the entire image when scaled down.
        """
        self.scaling = scaling

        self.__last_frame = None
        self.flow = None

    def motion_estimate(self, frame: np.ndarray) -> np.ndarray:
        """
        Estimates the motion between the frame passed as parameter and the one stored in self.__last_frame.

        :param frame: New frame of the sequence.
        :return: The estimation of the mean motion between self.__last_frame and the frame passed as argument. The motion estimate is expressed in pixel units.
        """

        frame = scale_image(frame, self.scaling)
        if self.__last_frame is None:
            self.__last_frame = frame.copy()
            return np.array([0, 0])

        self.flow = cv2.calcOpticalFlowFarneback(self.__last_frame, frame, 1.0, 0.5, 5, 15, 3, 5, 1.1,
                                                 cv2.OPTFLOW_FARNEBACK_GAUSSIAN)

        mean_flow = np.mean(self.flow, axis=(0, 1))
        self.__last_frame = frame.copy()

        return -(mean_flow / self.scaling)
