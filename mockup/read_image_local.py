import cv2
import numpy as np
from sklearn.cluster import KMeans
import os
import json
from django.conf import settings


def read_image_local(image_name):
    try:
        hue_clusters_number = 4
        value_clusters_number = 4
        SAT_LIMIT = 25  # it determines how many pixel are colored and not
        CONTOUR_AREA_LIMIT = 1000  # If biggest contour area is lower than limit, eliminate
        HUE_LIMIT = 25
        VAL_LIMIT = 25

        image_ext = ".png"

        rel_output_folder = os.path.join('static', 'layers', 'temp')
        abs_output_folder = os.path.join(settings.BASE_DIR, 'static', 'layers', 'temp')

        layer_folder = os.path.join(settings.BASE_DIR, 'static', 'layers')

        if not os.path.exists(layer_folder):
            os.mkdir(layer_folder)
        if not os.path.exists(abs_output_folder):
            os.mkdir(abs_output_folder)
        print("Folder is established")

        files = os.listdir(abs_output_folder)
        if len(files):
            for file in files:
                os.remove(os.path.join(abs_output_folder, file))

        print("Image is reading")

        img = cv2.imread(os.path.join(settings.MEDIA_ROOT, image_name))
        print("Image is set up")

        img_copied = img.copy()

        img_alpha = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        Z_alpha = img_alpha.reshape(img_alpha.shape[0] * img_alpha.shape[1], 4)
        Z_alpha[:, 3] = 0

        hsv_img = cv2.cvtColor(img_copied, cv2.COLOR_BGR2HSV)
        Z_hsv = hsv_img.reshape(hsv_img.shape[0] * hsv_img.shape[1], 3)
        Z_hsv_cpy = Z_hsv.copy()
        Z_val = Z_hsv_cpy[Z_hsv_cpy[:, 1] <= SAT_LIMIT]  # saturation <= SAT_LIMIT. no color, gray space
        Z_hue = Z_hsv_cpy[Z_hsv_cpy[:, 1] > SAT_LIMIT]  # saturation > SAT_LIMIT. color

        image_size = img.shape[0] * img.shape[1]
        val_number = Z_val.shape[0]
        hue_number = Z_hue.shape[0]

        Z_val[:, 0] = 0  # hue
        Z_val[:, 1] = 0  # saturation

        Z_hue[:, 2] = 0  # value
        Z_hue[:, 1] = 0  # saturation

        flag_hue = False
        flag_val = False
        while True:

            if not flag_hue and hue_clusters_number:
                hue_clusters = KMeans(n_clusters=hue_clusters_number)
                hue_clusters.fit(Z_hue.copy())

            if not flag_val and value_clusters_number:
                value_clusters = KMeans(n_clusters=value_clusters_number)
                value_clusters.fit(Z_val.copy())

            flag_hue = True
            flag_val = True

            all_clusters_labels = Z_hsv[:, 1].copy()  # saturation values

            val_clusters_labels = value_clusters.labels_.copy()
            val_clusters_labels += hue_clusters_number

            all_clusters_labels[all_clusters_labels <= SAT_LIMIT] = val_clusters_labels
            all_clusters_labels[all_clusters_labels > SAT_LIMIT] = hue_clusters.labels_

            for i in range(hue_clusters_number + value_clusters_number):

                thresh = np.where(all_clusters_labels == i, 255, 0)
                thresh = thresh.astype("uint8")
                thresh = thresh.reshape(img.shape[0], img.shape[1])

                _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                biggest_cnt = max(contours, key=cv2.contourArea)
                biggest_cnt_area = cv2.contourArea(biggest_cnt)

                number = np.sum(all_clusters_labels == i)
                if i < hue_clusters_number:
                    if number < hue_number / HUE_LIMIT or biggest_cnt_area < image_size / CONTOUR_AREA_LIMIT:
                        flag_hue = False
                        hue_clusters_number -= 1
                        break
                else:
                    if number < val_number / VAL_LIMIT or biggest_cnt_area < image_size / CONTOUR_AREA_LIMIT:
                        flag_val = False
                        value_clusters_number -= 1
                        break

            print("Hue_cluster_number = {}".format(hue_clusters_number))
            print("Val_cluster_number = {}".format(value_clusters_number))
            print("\n")

            if flag_hue and flag_val:
                break

        json_dict = {
            'width': img.shape[1],
            'height': img.shape[0],
            'hue_number': hue_clusters_number,
            'val_number': value_clusters_number,
            'total_number': hue_clusters_number + value_clusters_number,
            'hue_image_list': list(),
            'val_image_list': list(),
        }
        for i in range(hue_clusters_number + value_clusters_number):
            tmp_alpha = Z_alpha.copy()
            k = tmp_alpha[all_clusters_labels == i]
            k[:, 3] = 255
            tmp_alpha[all_clusters_labels == i] = k
            image = tmp_alpha.reshape(img_alpha.shape)
            if i < hue_clusters_number:
                path = os.path.join(abs_output_folder, 'hue_{}.png'.format(i))
                static_path = os.path.join(rel_output_folder, 'hue_{}.png'.format(i))
                static_path = static_path.replace('\\', '/')
                json_dict['hue_image_list'].append(static_path)
                cv2.imwrite(path, image)
            else:
                path = os.path.join(abs_output_folder, 'val_{}.png'.format(i - hue_clusters_number))
                static_path = os.path.join(rel_output_folder, 'val_{}.png'.format(i - hue_clusters_number))
                static_path = static_path.replace('\\', '/')
                json_dict['val_image_list'].append(static_path)
                cv2.imwrite(path, image)

        with open(os.path.join(abs_output_folder, 'image.json'), 'w') as write_file:
            json.dump(json_dict, write_file)


    except Exception as e:
        print("error: ", e)
        return e

    else:
        return "True"