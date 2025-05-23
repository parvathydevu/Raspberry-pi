import cv2
import numpy as np

class ImageProcessor:
    def __init__(self):
        self.original_image = None  # Original loaded image (BGR)
        self.processed_image = None  # Transformed image

    def load_image(self, path):
        img = cv2.imread(path)
        if img is not None:
            self.original_image = img
            self.processed_image = img.copy()
            return True
        return False

    def save_image(self, path):
        if self.processed_image is not None:
            cv2.imwrite(path, self.processed_image)
            return True
        return False

    def get_display_image(self):
        """Return current image converted to RGB for display in QLabel"""
        if self.processed_image is None:
            return None
        img = self.processed_image
        if len(img.shape) == 2:  # grayscale
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img

    def reset_image(self):
        if self.original_image is not None:
            self.processed_image = self.original_image.copy()

    def apply_transformation(self, name, param=50):
        if self.original_image is None:
            return

        img = self.original_image.copy()

        if name == "Convert to Grayscale":
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        elif name == "Gaussian Blur":
            k = param if param % 2 == 1 else param + 1
            k = max(1, k)
            img = cv2.GaussianBlur(img, (k, k), 0)

        elif name == "Median Blur":
            k = param if param % 2 == 1 else param + 1
            k = max(1, k)
            img = cv2.medianBlur(img, k)

        elif name == "Sobel Edge Detection":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            img = cv2.convertScaleAbs(sobelx) + cv2.convertScaleAbs(sobely)

        elif name == "Canny Edge Detection":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.Canny(gray, 100, 200)

        elif name == "Thresholding (Binary or Adaptive)":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, img = cv2.threshold(gray, param, 255, cv2.THRESH_BINARY)

        elif name == "Image Rotation":
            (h, w) = img.shape[:2]
            M = cv2.getRotationMatrix2D((w / 2, h / 2), param, 1.0)
            img = cv2.warpAffine(img, M, (w, h))

        elif name == "Image Resizing":
            scale = param / 50.0
            if scale <= 0: scale = 0.1
            img = cv2.resize(img, None, fx=scale, fy=scale)

        elif name == "Erosion":
            kernel = np.ones((3, 3), np.uint8)
            iterations = max(1, param // 10)
            img = cv2.erode(img, kernel, iterations=iterations)

        elif name == "Dilation":
            kernel = np.ones((3, 3), np.uint8)
            iterations = max(1, param // 10)
            img = cv2.dilate(img, kernel, iterations=iterations)

        elif name == "FlipHorizontal":
            img = cv2.flip(img, 1)

        elif name == "FlipVertical":
            img = cv2.flip(img, 0)

        elif name == "Brightness":
            beta = param - 50  # range -50 to +50
            img = cv2.convertScaleAbs(img, alpha=1, beta=beta)

        elif name == "Contrast":
            alpha = param / 50.0  # range 0.02 to 2.0
            img = cv2.convertScaleAbs(img, alpha=alpha, beta=0)

        self.processed_image = img
