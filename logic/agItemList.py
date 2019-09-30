from autogreener.utils import Bbox

class AGItemList():
    def __init__(self):
        self.items = []

    def add_child(self, *args):
        for item in args:
            self.items.append(item)

    def prune_empty(self):
        def is_dead(item):
            return (item.text.isspace() or not item.text.strip())
            
        for i in reversed(self.items):
            if is_dead(i):
                self.items.remove(i)
        # [self.items.remove(i) for i in reversed(self.items) if is_dead(i)]

    def dilate_all(self):
        for item in self.items:
            item.bbox.dilate(20, -2)

    def cluster_overlapping(self, dilate=(0,0)):
        items_before_cluster = 0
        items_after_cluster = 1

        while(items_before_cluster != items_after_cluster):
            
            items_before_cluster = len(self.items)

            listCopy = self.items.copy()

            reference = listCopy.pop(0)

            cluster = [reference]
            for other in reversed(listCopy):
                if reference.bbox.intersects(other.bbox, dilate=dilate):
                    cluster.append(other)
                    listCopy.remove(other)
            
            for item in cluster:
                self.items.remove(item)
            
            reference.bbox = sum(map(lambda x: x.bbox, cluster))
            reference.text = ' '.join(*[map(lambda x: x.text, cluster)])

            self.items.append(reference)

            items_after_cluster = len(self.items)

class AGItem():
    def __init__(self, bbox=None, text='', fg=(0,0,0), bg=(1,1,1)):
        if bbox is None:
            self.bbox = None
        elif isinstance(bbox, Bbox):
            self.bbox = bbox
        elif isinstance(bbox, dict):
            x, y, w, h = bbox.values()
            self.bbox = Bbox(( x, y, x+w, y+h ))
        else:
            self.bbox = Bbox(bbox)
        self.text = text
        self.fg = fg
        self.bg = bg

if __name__ == "__main__":
    test = AGItemList()

    # Test data
    itemA = AGItem(text='good')
    itemB = AGItem(text='      \n')

    test.add_child(itemA, itemB)

    print(f'Before pruning: {len(test.items)} items.')

    test.prune_empty()

    print(f'After pruning: {len(test.items)} items.')


    from autogreener.logic.hocr_parser import HOCRParser
    from PIL import Image

    image = Image.open(r'/Users/jasorein/Documents/Autogreener/data/input/ss.png')

    hocr = HOCRParser()

    hocr.load_image(image)

    hocr_results = hocr.get_all_with_tag('line')

    boxes, text, images = list(zip(*hocr_results))

    tree = AGItemList()

    for b, t in zip(boxes, text):
        tree.add_child(AGItem(bbox=b, text=t))
        # self.app.previewFrame.canvas.create_rectangle(b)

    print(f'Before pruning: {len(tree.items)} items.')

    tree.prune_empty()

    print(f'After pruning: {len(tree.items)} items.')