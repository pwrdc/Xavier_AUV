class BoundingBox:
    """
    Class representing a bounding box
    """

    def __init__(self, x=0, y=0, w=0, h=0, p=0, detected_item=None):
        self.__update_points(x, y, w, h, p, detected_item)

    def __update_points(self, x, y, w, h, p, detected_item):
        """
        Internal use only
        :param x:
        :param y:
        :param w:
        :param h:
        :return:
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.p = p

        # Center - relative coordinates
        self.xc = 2*x - 1
        self.yc = 2*y - 1

        # Diagonal coordinates
        self.x1 = x - w/2
        self.x2 = x + w/2
        self.y1 = y - h/2
        self.y2 = y + h/2

        # Points with diagonal coordinates
        self.p1 = (int(self.x1), int(self.y1))
        self.p2 = (int(self.x2), int(self.y2))

        self.detected_item = detected_item

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "w": self.w,
            "h": self.h,
            "p": self.p
        }

    @staticmethod
    def from_points(x1, y1, x2, y2, p=0, detected_item=None):  # -> BoundingBox
        """
        Builds a bounding box from 2 points lying on rectangle diagonal

        :param x1: X coordinate of top left corner
        :param y1: Y coordinate of top left corner
        :param x2: X coordinate of bottom right corner
        :param y2: Y coordinate of bottom right corner
        :param p: Probability of bounding box (from 0 to 1)
        :return: BoundingBox representing provided rectangle
        """
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        w = x2 - x1
        h = y2 - y1

        return BoundingBox(x, y, w, h, self.p, self.detected_item)

    def normalize(self, img_width, img_height, inplace=False):  # -> BoundingBox
        """
        Normalizes coordinates from range of (0, 0):(img_width, img_height) to (0,0):(1,1).
        Eg. 104x104 Bounding box with center in (208, 104) becomes 0.25x0,25 with center in (0.5, 0.25) for img of size
        416x416
        :param img_width: width of image in respect to which BoundingBox is normalized
        :param img_height: height of image in respect to which BoundingBox is normalized
        :param inplace: Values replaced in current object if set to true. New object is returned if set to False
        :return: Bounding box with normalized coordinates
        """
        x = self.x / img_width
        y = self.y / img_height
        w = self.w / img_width
        h = self.h / img_height

        if inplace:
            self.__update_points(x, y, w, h, self.p, self.detected_item)

            return self
        else:
            return BoundingBox(x, y, w, h, self.p, self.detected_item)

    def denormalize(self, img_width, img_height, inplace=False):  # -> BoundingBox
        """
        Maps coordinates from range of (0, 0):(1, 1) to (0,0):(img_width, img_height).
        Eg. 0.25x0.25 Bounding box with center in (0.5, 0.25) becomes 104x104 with center in(208, 104) for img of size
        416x416
        :param img_width: width of image in respect to which BoundingBox is normalized
        :param img_height: height of image in respect to which BoundingBox is normalized
        :param inplace: Values replaced in current object if set to true. New object is returned if set to False
        :return: Bounding box with normalized coordinates
        """
        x = self.x * img_width
        y = self.y * img_height
        w = self.w * img_width
        h = self.h * img_height

        if inplace:
            self.__update_points(x, y, w, h, self.p, self.detected_item)
            return self
        else:
            return BoundingBox(x, y, w, h, self.p, self.detected_item)

    def __str__(self):
        return f"x={self.xc}, y={self.yc}, w={self.w}, h={self.h}, p={self.p}, item={self.detected_item}"

    def mvg_avg(self, new_observation, discount_factor, inplace=False):
        """
        Function used to smooth noisy bounding box observations. 
        :param new_observation: New observation of bounding box that will be incorporated with current one
        :discount_factor: From 0 to 1. How much current knowledge is prefered over new one. If 0.0 - discard all old data
                          (Similar to just setting values to new_observation ones). If 1.0 - knew knowledge will be discarded
                          (This means -just do nothing)
        """

        x = (1 - discount_factor) * new_observation.x + discount_factor * self.x
        y = (1 - discount_factor) * new_observation.y + discount_factor * self.y
        w = (1 - discount_factor) * new_observation.w + discount_factor * self.w
        h = (1 - discount_factor) * new_observation.h + discount_factor * self.h
        p = (1 - discount_factor) * new_observation.p + discount_factor * self.p

        if inplace:
            self.__update_points(x,y,w,h,p, self.detected_item)
            return self
        else:
            return BoundingBox(x,y,w,h,p, self.detected_item)


if __name__ == "__main__":

    # Example usage
    box = BoundingBox(208, 104, 104, 104)
    print(f"x: {box.x}, y: {box.y}, w: {box.w}, h: {box.h}")

    box.normalize(416, 416, True)
    print(f"x: {box.x}, y: {box.y}, w: {box.w}, h: {box.h}")  # 0.5, 0.25, 0.25, 0.25

    box.denormalize(416, 416, True)
    print(f"x: {box.x}, y: {box.y}, w: {box.w}, h: {box.h}")  # 208, 104, 104, 104
