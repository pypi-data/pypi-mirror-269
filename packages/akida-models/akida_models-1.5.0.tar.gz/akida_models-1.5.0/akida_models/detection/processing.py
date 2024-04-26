#!/usr/bin/env python
# ******************************************************************************
# Copyright 2020 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""
Processing tools for YOLO data handling.
"""

__all__ = ["BoundingBox", "load_image", "preprocess_image", "decode_output", "create_yolo_targets"]


import numpy as np
import tensorflow as tf
from .data_utils import Coord
from .box_utils import compute_center_wh, compute_center_xy


class BoundingBox:
    """ Utility class to represent a bounding box.

    The box is defined by its top left corner (x1, y1), bottom right corner
    (x2, y2), label, score and classes.
    """

    def __init__(self, x1, y1, x2, y2, score=-1, classes=None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.label = -1
        self.score = score
        self.classes = classes

    def __repr__(self):
        return "<BoundingBox({}, {}, {}, {}, {}, {}, {})>\n".format(
            self.x1, self.x2, self.y1, self.y2, self.get_label(),
            self.get_score(), self.classes)

    def get_label(self):
        """ Returns the label for this bounding box.

        Returns:
            Index of the label as an integer.
        """
        if self.label == -1:
            self.label = tf.argmax(self.classes)
        return self.label

    def get_score(self):
        """ Returns the score for this bounding box.

        Returns:
            Confidence as a float.
        """
        if self.score == -1:
            self.score = self.classes[self.get_label()]
        return self.score

    def iou(self, other):
        """ Computes intersection over union ratio between this bounding box and
        another one.

        Args:
            other (BoundingBox): the other bounding box for IOU computation

        Returns:
            IOU value as a float
        """

        def _interval_overlap(interval_1, interval_2):
            x1, x2 = interval_1
            x3, x4 = interval_2
            x1, x2, x3, x4 = (tf.cast(x1, dtype=tf.float32),
                              tf.cast(x2, dtype=tf.float32),
                              tf.cast(x3, dtype=tf.float32),
                              tf.cast(x4, dtype=tf.float32))

            if x3 < x1:
                if x4 < x1:
                    return tf.constant(0, dtype=tf.float32)
                return tf.minimum(x2, x4) - x1
            if x2 < x3:
                return tf.constant(0, dtype=tf.float32)
            return tf.minimum(x2, x4) - x3

        intersect_w = _interval_overlap([self.x1, self.x2],
                                        [other.x1, other.x2])
        intersect_h = _interval_overlap([self.y1, self.y2],
                                        [other.y1, other.y2])

        intersect = intersect_w * intersect_h

        w1, h1 = self.x2 - self.x1, self.y2 - self.y1
        w2, h2 = other.x2 - other.x1, other.y2 - other.y1

        union = w1 * h1 + w2 * h2 - intersect

        return tf.cast(intersect, dtype=tf.float32) / tf.cast(union, dtype=tf.float32)


def load_image(image_path):
    """ Loads an image from a path.

    Args:
        image_path (string): full path of the image to load

    Returns:
        a Tensorflow image Tensor
    """
    raw_image = tf.io.read_file(image_path)
    return tf.image.decode_jpeg(raw_image, channels=3)


def preprocess_image(image_buffer, output_size):
    """ Preprocess an image for YOLO inference.

    Args:
        image_buffer (tf.Tensor): image to preprocess
        output_size (tuple): shape of the image after preprocessing

    Returns:
        A resized and normalized image as a Numpy array.
    """
    # Resize
    width = tf.constant(output_size[0])
    height = tf.constant(output_size[1])
    image = tf.compat.v1.image.resize(image_buffer, [height, width],
                                      method=tf.image.ResizeMethod.BILINEAR,
                                      align_corners=False)
    return image.numpy()


def create_yolo_targets(objects,
                        grid_size,
                        num_classes,
                        anchors):
    """
    Creates YOLO-style targets tensor for the given objects.

    Args:
        objects (dict): Dictionary containing information about objects in the image,
            including labels and bounding boxes.
        grid_size (tuple): The grid size used for YOLO target generation.
        num_classes (int): The number of classes.
        anchors (list): List of anchor boxes.

    Returns:
        targets (tf.Tensor): The targets output tensor.
    """
    def _update_bbox_target(bbox, grid_y, grid_x, best_anchor, targets):
        for i in range(4):
            indices_bbox = [[grid_y, grid_x, best_anchor, i]]
            targets = tf.tensor_scatter_nd_update(targets, indices_bbox, updates=[bbox[i]])
        return targets

    def _update_confidence_target(grid_y, grid_x, best_anchor, targets):
        indices_confidence = [[grid_y, grid_x, best_anchor, 4]]
        return tf.tensor_scatter_nd_update(targets, indices_confidence, updates=[1.])

    def _update_class_target(grid_y, grid_x, best_anchor, obj_indx, targets):
        indices_class = [[grid_y, grid_x, best_anchor, tf.cast(5 + obj_indx, tf.int32)]]
        return tf.tensor_scatter_nd_update(targets, indices_class, updates=[1.])

    n_anchors = len(anchors)
    anchors = [BoundingBox(0, 0, anchors[i][0], anchors[i][1]) for i in range(len(anchors))]
    targets = tf.zeros((grid_size[0], grid_size[1], n_anchors, 5 + num_classes),
                       dtype=tf.float32)
    num_objects = tf.shape(objects['label'])[0]

    for idx in range(num_objects):
        bbox = objects['bbox'][idx]
        if bbox[Coord.x2] > bbox[Coord.x1] and bbox[Coord.y2] > bbox[Coord.y1]:
            center_x, center_y = compute_center_xy(bbox, grid_size)

            # find grid index where the center is located
            grid_x = tf.cast(center_x, tf.int32)
            grid_y = tf.cast(center_y, tf.int32)

            if grid_x < grid_size[1] and grid_y < grid_size[0]:
                obj_indx = objects['label'][idx]

                center_w, center_h = compute_center_wh(bbox, grid_size)

                box = [center_x, center_y, center_w, center_h]
                # find the anchor that best predicts this box
                best_anchor = -1
                max_iou = tf.constant(-1, dtype=tf.float32)

                shifted_box = BoundingBox(0, 0, center_w, center_h)

                for anchor_id, anchor in enumerate(anchors):
                    iou = shifted_box.iou(anchor)

                    if max_iou < iou:
                        best_anchor = anchor_id
                        max_iou = iou

                targets = _update_bbox_target(box, grid_y, grid_x, best_anchor, targets)
                targets = _update_confidence_target(grid_y, grid_x, best_anchor, targets)
                targets = _update_class_target(grid_y, grid_x, best_anchor, obj_indx, targets)

    return targets


def decode_output(output, anchors, nb_classes, obj_threshold=0.5, nms_threshold=0.5):
    """ Decodes a YOLO model output.

    Args:
        output (tf.Tensor): model output to decode
        anchors (list): list of anchors boxes
        nb_classes (int): number of classes
        obj_threshold (float, optional): confidence threshold for a box. Defaults to 0.5.
        nms_threshold (float, optional): non-maximal supression threshold. Defaults to 0.5.

    Returns:
        List of `BoundingBox` objects
    """

    def _sigmoid(x):
        return 1. / (1. + np.exp(-x))

    def _softmax(x, axis=-1, t=-100.):
        x = x - np.max(x)

        if np.min(x) < t:
            x = x / np.min(x) * t

        e_x = np.exp(x)

        return e_x / e_x.sum(axis, keepdims=True)

    grid_h, grid_w, nb_box = output.shape[:3]

    boxes = []

    # decode the output by the network
    output[..., 4] = _sigmoid(output[..., 4])
    output[..., 5:] = output[..., 4][..., np.newaxis] * _softmax(output[..., 5:])
    output[..., 5:] *= output[..., 5:] > obj_threshold

    col, row, _ = np.meshgrid(np.arange(grid_w), np.arange(grid_h), np.arange(nb_box))

    x = (col + _sigmoid(output[..., 0])) / grid_w
    y = (row + _sigmoid(output[..., 1])) / grid_h
    w = np.array(anchors)[:, 0] * np.exp(output[..., 2]) / grid_w
    h = np.array(anchors)[:, 1] * np.exp(output[..., 3]) / grid_h

    x1 = np.maximum(x - w / 2, 0)
    y1 = np.maximum(y - h / 2, 0)
    x2 = np.minimum(x + w / 2, grid_w)
    y2 = np.minimum(y + h / 2, grid_h)

    confidence = output[..., 4]
    classes = output[..., 5:]
    mask = np.sum(classes, axis=-1) > 0
    indices = np.where(mask)

    for i in range(len(indices[0])):
        row_idx, col_idx, box_idx = indices[0][i], indices[1][i], indices[2][i]

        box = BoundingBox(x1[row_idx, col_idx, box_idx],
                          y1[row_idx, col_idx, box_idx],
                          x2[row_idx, col_idx, box_idx],
                          y2[row_idx, col_idx, box_idx],
                          confidence[row_idx, col_idx, box_idx],
                          classes[row_idx, col_idx, box_idx])

        boxes.append(box)

    # suppress non-maximal boxes
    for c in range(nb_classes):
        sorted_indices = np.argsort([box.classes[c] for box in boxes])[::-1]
        for ind, index_i in enumerate(sorted_indices):
            if boxes[index_i].score == 0 or boxes[index_i].classes[c] == 0:
                continue

            for j in range(ind + 1, len(sorted_indices)):
                index_j = sorted_indices[j]
                if boxes[index_j].score == 0:
                    continue

                # filter out redundant boxes (same class and overlapping too
                # much)
                if (boxes[index_i].iou(boxes[index_j]) >= nms_threshold) and (
                        c == boxes[index_i].get_label()) and (
                            c == boxes[index_j].get_label()):
                    boxes[index_j].score = 0

    # remove the boxes which are less likely than a obj_threshold
    boxes = [box for box in boxes if box.get_score() > obj_threshold]

    return boxes
