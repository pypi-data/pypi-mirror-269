import math
import numpy as np
import cv2


def normalize_landmarks(landmarks):
    features = ['LeftEye', 'RightEye', 'Nose', 'LeftLipCorner', 'RightLipCorner']
    if isinstance(landmarks, list) and all([isinstance(p, float) for p in landmarks]):
        norm = []
        pnt = []
        i = 0
        for p in landmarks:
            pnt.append(p)
            if len(pnt) == 2:
                norm.append({
                    'category_id': i,
                    'connect': [],
                    'label': features[i],
                    'landmark': pnt,
                    'score': 1.0
                })
                pnt = []
                i += 1
        return norm
    elif isinstance(landmarks, list) and any(['label' not in pnt for pnt in landmarks]):
        return [{'category_id': i,
                 'connect': [],
                 'label': features[pnt['category_id']],
                 'landmark': pnt['landmark'],
                 'score': 1.0} for i, pnt in enumerate(landmarks)]
    else:
        return landmarks


def get_face_img(src_image, bbox, landmarks=None, margin: float = 0.0, aspect: float = -1., use_normalization: bool = False):
    bbox1 = bbox.copy()
    if landmarks is None:
        use_normalization = False

    x_max, y_max, _ = src_image.shape
    x_max -= 1
    y_max -= 1

    x0 = 0.5*(bbox1[0] + bbox1[2])
    y0 = 0.5*(bbox1[1] + bbox1[3])
    dx = bbox1[2] - bbox1[0]
    dy = bbox1[3] - bbox1[1]
    if aspect <= 0.0:
        aspect = dx / dy
    dy = (0.5 + margin) * dy
    dx = aspect * dy
    bbox1[0] = max(0,     x0 - dx)
    bbox1[2] = min(x_max, x0 + dx)
    bbox1[1] = max(0, y0 - dy) # from the "chin" level up
    bbox1[3] = min(y_max-1, y0 + dy)

    if landmarks is None:
        use_normalization = False

    if use_normalization:
        face_shift = np.array([bbox[0], bbox[1]])

        flt = lambda feature: [lm['landmark'] for lm in landmarks if lm['label'] == feature][0]
        src_face_mask = np.array([flt('LeftEye'),
                                  flt('RightEye'),
                                  flt('Nose'),
                                  flt('LeftLipCorner'),
                                  flt('RightLipCorner')])

        face_shift = np.array([src_face_mask[2][0], src_face_mask[2][1]])

        dst_face_mask = np.array(
            [[38.2946, 51.6963], [73.5318, 51.5014], [56.0252, 71.7366],
             [41.5493, 92.3655], [70.7299, 92.2041]],
            dtype=np.float32)
        dst_face_mask += (face_shift - np.array([dst_face_mask[2][0], dst_face_mask[2][1]]))

        M, _ = cv2.estimateAffinePartial2D(src_face_mask, dst_face_mask)

        s = math.sqrt(M[0, 0]*M[1, 1] - M[0, 1]*M[1, 0])
        sn = M[0, 1] / s

        rows, cols, _ = src_image.shape
        dst_image = cv2.warpAffine(src_image, M, (cols, rows))

        x1 = np.array([bbox1[0], bbox1[1], 1])
        x2 = np.array([bbox1[2], bbox1[1], 1])
        x3 = np.array([bbox1[2], bbox1[3], 1])
        x4 = np.array([bbox1[0], bbox1[3], 1])
        xt1 = M @ x1
        xt2 = M @ x2
        xt3 = M @ x3
        xt4 = M @ x4

        bbox2 = [
            min(xt1[0], xt2[0], xt3[0], xt4[0]),
            min(xt1[1], xt2[1], xt3[1], xt4[1]),
            max(xt1[0], xt2[0], xt3[0], xt4[0]),
            max(xt1[1], xt2[1], xt3[1], xt4[1])
        ]

        d = 0.1*abs(bbox1[3] - bbox1[1])*abs(sn)
        bbox2 = [ max(0, bbox2[0]+2.5*d), max(0, bbox2[1]+d),
                  min(x_max, bbox2[2]-2.5*d), min(y_max, bbox2[3]-d)]

        if 0 <= bbox2[0] < bbox2[2] <= x_max and 0 <= bbox2[1] < bbox2[3] <= y_max:
            face_img_rotated = dst_image[int(bbox2[1]):int(bbox2[3]), int(bbox2[0]):int(bbox2[2])]
        else:
            face_img_rotated = src_image[int(bbox1[1]):int(bbox1[3]), int(bbox1[0]):int(bbox1[2])]
    else:
        face_img_rotated = src_image[int(bbox1[1]):int(bbox1[3]), int(bbox1[0]):int(bbox1[2])]

    face_img = src_image[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]

    return face_img_rotated, face_img


