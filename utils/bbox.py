import numpy as np

class Bbox():
    def __init__(self, x):
        if isinstance(x, Bbox):
            self.xmin, self.ymin, self.xmax, self.ymax = x.xmin, x.ymin, x.xmax, x.ymax
        elif isinstance(x, (list, tuple, np.ndarray)):
            if len(x) != 4:
                raise ValueError(f'Bbox list/tuple/array should be length 4, was length {len(x)}')
            else:
                self.xmin, self.ymin, self.xmax, self.ymax = Bbox.format_bbox_values(x[0], x[1], x[2], x[3])
        else:
            raise TypeError(f'Bbox constructor should be of type Bbox, list, tuple or np.ndarray - {type(x)} found')

    @property
    def bbox(self):
        return (self.xmin, self.ymin, self.xmax, self.ymax)
    @bbox.setter
    def bbox(self, x1, y1, x2, y2):
        self.xmin, self.ymin, self.xmax, self.ymax = Bbox.format_bbox_values(x1, y1, x2, y2)

    @property
    def area(self):
        return self.width * self.height

    @property
    def width(self):
        return self.xmax - self.xmin
    @width.setter
    def width(self, w):
        self.xmax = self.xmin + w

    @property
    def height(self):
        return self.ymax - self.ymin
    @height.setter
    def height(self, h):
        self.ymax = self.ymin + h

    @property
    def center(self):
        return ((self.xmax + self.xmin)/2, (self.ymax + self.ymin)/2)
    @center.setter
    def center(self, c):
        if len(c) != 2:
            raise ValueError('Center point should be tuple of dimension 2')
        else:
            self.translate(np.subtract(c, self.center))

    def translate(self, t):
        if len(t) != 2:
            raise ValueError('Translation vector should be tuple of dimension 2')
        self.xmin += t[0]
        self.xmax += t[0]
        self.ymin += t[1]
        self.ymax += t[1]
        return self

    def dilate(self, x, y):
        self.xmin -= x
        self.xmax += x
        self.ymin -= y
        self.ymax += y
        return self

    def scale(self, x, y):
        raise NotImplementedError('Use dilate for now instead')

    @property
    def NW(self):
        return (self.xmin, self.ymin)
    
    @property
    def SE(self):
        return (self.xmax, self.ymax)

    @property
    def W(self):
        return (self.xmin, (self.ymax + self.ymin)/2)

    @property
    def E(self):
        return (self.xmax, (self.ymax + self.ymin)/2)

    @staticmethod
    def intersection(bbA, bbB):
        xmin = max(bbA.xmin, bbB.xmin)
        ymin = max(bbA.ymin, bbB.ymin)
        xmax = min(bbA.xmax, bbB.xmax)
        ymax = min(bbA.ymax, bbB.ymax)
        
        if (xmax < xmin or ymax < ymin):
            return None
        else:
            return Bbox((xmin, ymin, xmax, ymax))

    @staticmethod
    def get_iou(bbA, bbB):
        iArea = Bbox.intersection(bbA, bbB).area
        uArea = bbA.area + bbB.area - iArea
        return iArea / uArea

    @staticmethod
    def format_bbox_values(x1, y1, x2, y2):
        return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)


    # for some reason b3 misses a pixel,wtf? don't worry about it for now
    @staticmethod
    def to_border_pixels(bbox):
        def create_coordinate_grid(width, height):
            i_coords, j_coords = np.meshgrid(range(width), range(height), indexing='ij')
            coordinate_grid = np.array(np.dstack((j_coords, i_coords)))
            return coordinate_grid

        bbox = Bbox.format_bbox_values(*bbox)

        coords = create_coordinate_grid(bbox[2]+1, bbox[3]+1)

        x1, y1, x2, y2 = bbox

        b1 = coords[x1              , y1 : y2+1         ]
        b2 = coords[x1+1 : x2+1     , y2                ]
        b3 = coords[x2              , y2-1 : y1 : -1    ]
        b4 = coords[x2-1 : x1 : -1  , y1                ]

        px =  np.concatenate((b1, b2, b3, b4))
        return px



    def intersects(self, other, dilate=None):
        if not isinstance(other, Bbox):
            return False

        if dilate is not None:
            bbA = Bbox(self).dilate(dilate[0], dilate[1])
            bbB = Bbox(other).dilate(dilate[0], dilate[1])
            return True if Bbox.intersection(bbA, bbB) is not None else False
        else:
            return True if Bbox.intersection(self, other) is not None else False

    def as_xywh(self):
        return [self.xmin, self.ymin, self.width, self.height]    
    
    

    def __add__(self, other):
        if not other:
            return self.bbox
        return Bbox((min(self.xmin, other.xmin),
                    min(self.ymin, other.ymin),
                    max(self.xmax, other.xmax),
                    max(self.ymax, other.ymax)))
    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __and__(self, other):
        return Bbox.intersection(self, other)

    def __str__(self):
        return str(self.bbox)

    def __iter__(self):
        return iter(self.bbox)

    def __eq__(self, other):
        if isinstance(other, Bbox):
            return self.bbox == other.bbox
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


if __name__ == '__main__':
    pass