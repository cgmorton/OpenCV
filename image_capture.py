import argparse
import ctypes
import datetime
import logging
import os

import cv2
import cv2.cv as cv
import pyHook
import pythoncom


def main(output_folder='Capture', width=1280, height=720, fps=30):
    """Capture image from webcam everytime spacebar is pressed"""
    logging.info('Image capture')
    logging.info('CV2 version: {}'.format(cv2.__version__))
    logging.info('Output folder: {}'.format(output_folder))

    # Build the output folder if necessary
    output_ws = os.path.join(os.getcwd(), output_folder)
    if not os.path.isdir(output_ws):
        os.mkdir(output_ws)

    #
    cap = cv2.VideoCapture(0)

    # Set the capture properties
    cap.set(3, width)
    cap.set(4, height)
    cap.set(5, fps)

    logging.info(
        '\nUser Options:\n' +
        '  "space" to capture an image\n' +
        '  "/" to display an image on the screen\n' +
        '  "Esc or ctrl-c" to quit\n')

    def ShowImage():
        """"""
        cv2.destroyAllWindows()

        # On windows, there is a 1 image buffer that needs to get skipped
        ret, img = cap.read()
        ret, img = cap.read()
        # logging.debug(ret)

        # Burn the timestemp on the image
        image_dt = datetime.datetime.now()
        cv2.putText(
            img, image_dt.isoformat(), (10, height-10),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)

        # Show the image
        cv2.imshow('frame', img)
        # cv2.destroyAllWindows()
        del ret, img

    def CaptureImage(output_ws):
        """"""
        cv2.destroyAllWindows()

        # On windows, there is a 1 image buffer that needs to get skipped
        ret, img = cap.read()
        ret, img = cap.read()

        # Burn the timestemp on the image
        image_dt = datetime.datetime.now()
        cv2.putText(
            img, image_dt.isoformat(), (10, height-10),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)

        # Save the image
        output_path = os.path.join(
            output_ws, image_dt.strftime('%Y_%m_%d_%H_%M_%S_%f') + '.jpg')
        cv2.imwrite(output_path, img)
        cv2.destroyAllWindows()
        del ret, img

    def OnKeyboardEvent(event):
        """"""
        if event.Ascii == 32:
            # Space key
            print('Capture')
            CaptureImage(output_ws)
        elif event.Ascii == ord('/'):
            print('Display')
            ShowImage()
        elif event.Ascii in [3, 27]:
            # Ctrl-C OR Escape
            print('Quit')
            ctypes.windll.user32.PostQuitMessage(0)
        # elif event.Ascii in [ord('q'), ord('Q')]:
        #     # q, Q
        #     print('Quit')
        #     ctypes.windll.user32.PostQuitMessage(0)
        return True

    hm = pyHook.HookManager()
    hm.KeyDown = OnKeyboardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages()
    cap.release()


def arg_parse():
    """"""
    parser = argparse.ArgumentParser(
        description='Image Capture',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--output', default='Capture', metavar='PATH',
        help='Capture folder name')
    parser.add_argument(
        '--width', default=1280, help='Image Width')
    parser.add_argument(
        '--height', default=720, help='Image Height')
    parser.add_argument(
        '-f', '--fps', default=30, help='Frames Per Second (FPS)')
    parser.add_argument(
        '--debug', default=logging.INFO, const=logging.DEBUG,
        help='Debug level logging', action="store_const", dest="loglevel")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = arg_parse()
    logging.basicConfig(level=args.loglevel, format='%(message)s')


    main(args.output, args.width, args.height, args.fps)
