import numpy as np
import shapely.affinity
import shapely.geometry


class RotatedRect:
    def __init__(self, rect):
        self.cx = rect[0]
        self.cy = rect[1]
        self.w = rect[2]
        self.h = rect[3]
        self.angle = rect[4]

    def get_contour(self):
        w = self.w
        h = self.h
        c = shapely.geometry.box(-w / 2.0, -h / 2.0, w / 2.0, h / 2.0)
        rc = shapely.affinity.rotate(c, self.angle)
        return shapely.affinity.translate(rc, self.cx, self.cy)

    def intersection(self, other):
        return self.get_contour().intersection(other.get_contour())


def calculate_overlapping(_rect_1, _rect_2, visualization=False):
    # standard ~red
    r1 = RotatedRect(_rect_1)
    # detected  ~blue
    r2 = RotatedRect(_rect_2)

    if visualization:
        from descartes import PolygonPatch
        from matplotlib import pyplot
        fig = pyplot.figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        my_x_ticks = np.arange(-10, 10, 1)
        my_y_ticks = np.arange(-10, 10, 1)
        pyplot.xticks(my_x_ticks)
        pyplot.yticks(my_y_ticks)
        ax.add_patch(PolygonPatch(r1.get_contour(), fc='#990000', alpha=0.7))
        ax.add_patch(PolygonPatch(r2.get_contour(), fc='#000099', alpha=0.7))
        ax.add_patch(PolygonPatch(r1.intersection(r2), fc='#009900', alpha=1))
        pyplot.show()
    return r1.intersection(r2).area, r1.w * r1.h, r2.w * r2.h


'''if __name__ == '__main__':
    rect_1 = [-0.26, 6.51, 1.06, 0.46, -82.50592249883854]
    rect_2 = [-0.2201, 6.5619, 0.4706, 1.0059, 178.64251094383937]
    overlap = calculate_overlapping(rect_1, rect_2, False)
    print(overlap)'''
