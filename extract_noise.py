import argparse
import os
import ffmpeg
import numpy as np
import matplotlib.pyplot as plt
import glob
import cv2

def add_gaussian_noise(image, sigma):
    img = np.float64(np.copy(image))

    h = img.shape[0]
    w = img.shape[1]
    noise = np.random.randn(h, w) * sigma

    noisy_image = np.zeros(img.shape, np.float64)
    if len(img.shape) == 2:
        noisy_image = img + noise
    else:
        noisy_image[:,:,0] = img[:,:,0] + noise
        noisy_image[:,:,1] = img[:,:,1] + noise
        noisy_image[:,:,2] = img[:,:,2] + noise
    return noisy_image

def convert_to_uint8(image):
    img = np.float64(np.copy(image))
    cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX, dtype=-1)
    return img.astype(np.uint8)

def extract_frames_from_video(video_file):
    """
    Check if the video exists. Then check directory for output frames exists. If not, make one. 
    """
    if not os.path.isfile(video_file):
        print('File does not exist')
    else:
        video_directory = os.path.dirname(video_file)
        output_video_dir = video_directory + "frames"
        if not os.path.exists(output_video_dir):
            os.makedirs(output_video_dir)
    os.system('ffmpeg -i SampleVideo.mp4 frames/outputframe%03d.jpg')  # extract frames from the video


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Operation options')
    parser.add_argument('--extract', type=bool, default=False,
                        help="Extract frames from input video")
    parser.add_argument('--addnoise', type=bool, default=False,
                        help="Add Guassian noise to images")
    args = parser.parse_args()

    if args.extract: 
        video_file = "SampleVideo.mp4"
        extract_frames_from_video(video_file)

    if args.addnoise: 
        imagelist = glob.glob('frames/*.jpg')
        for img_dir in imagelist: 
            strsplit = img_dir.split('/')
            imagename = strsplit[1]
            img = cv2.imread(img_dir)
            noisy_image = add_gaussian_noise(img, 15)
            cv2.imwrite(imagename, noisy_image)


    # plt.imshow(convert_to_uint8(noisy_image))
    # plt.show()

    
