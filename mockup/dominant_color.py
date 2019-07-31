import cv2
import numpy as np
from sklearn.cluster import KMeans


def clamp(x):
    """

    :param x: int
    :return:
    """
    x = int(x)
    return max(0, min(x, 255))


def my_subt(x, y):
    x = int(x)
    y = int(y)

    if x - y < 0:
        return 0
    else:
        return x - y


def my_add(x, y):
    x = int(x)
    y = int(y)

    if x + y > 255:
        return 255
    else:
        return x + y


# 3,5,7
# 5,10,15
# 9,9,9

# a = (c-b) + (b-a)
# a = dif + temp

def change_color(arr, src_color, dst_color, interval=10):
    """
    Changes array as given parameters
    :param arr: numpy array
    :param src_color: tuple
    :param dst_color: tuple
    :param interval: int
    """

    dif = list()
    for i in range(3):
        dif.append(arr[i] - src_color[i])
    if abs(dif[0]) <= interval and abs(dif[1]) <= interval and abs(dif[2]) <= interval:
        for i in range(3):
            arr[i] = dst_color[i] + dif[i]


def make_histogram(cluster):
    """
    Count the number of pixels in each cluster
    :param: KMeans cluster
    :return: numpy histogram
    """
    num_labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    hist, _ = np.histogram(cluster.labels_, bins=num_labels)
    hist = hist.astype('float32')
    hist /= hist.sum()
    return hist


def sort_hsvs(hsv_list):
    """
    Sort the list of HSV values
    :param hsv_list: List of HSV tuples
    :return: List of indexes, sorted by hue, then saturation, then value
    """
    bars_with_indexes = []
    for index, hsv_val in enumerate(hsv_list):
        bars_with_indexes.append((index, hsv_val[0], hsv_val[1], hsv_val[2]))
    bars_with_indexes.sort(key=lambda elem: (elem[1], elem[2], elem[3]))
    return [item[0] for item in bars_with_indexes]


def get_dominant_colors(img_name, num_clusters=5):
    img = cv2.imread(img_name)
    height, width, _ = np.shape(img)

    # reshape the image to be a simple list of RGB pixels
    image = img.reshape((height * width, 3))

    # we'll pick the 5 most common colors
    clusters = KMeans(n_clusters=num_clusters)
    clusters.fit(image)

    # count the dominant colors and put them in "buckets"
    histogram = make_histogram(clusters)
    # then sort them, most-common first
    combined = zip(histogram, clusters.cluster_centers_)
    combined = sorted(combined, key=lambda x: x[0], reverse=True)

    # print(clusters.cluster_centers_)
    # cl = np.uint8(clusters.cluster_centers_)
    # print("\nhebe\n")
    # print(cl)

    colors = list()
    for row in clusters.cluster_centers_:
        color = "#{0:02x}{1:02x}{2:02x}".format(clamp(row[2]), clamp(row[1]), clamp(row[0]))
        colors.append(color)

    return colors


def show(image):
    cv2.imshow("IMG", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


