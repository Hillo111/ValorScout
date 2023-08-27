import qrcode
import cv2 as cv
from PIL import Image

def scan_qr_code():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    qcd = cv.QRCodeDetector()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Display the resulting frame
        cv.imshow('frame', frame)

        retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(gray)
        if retval and (decoded_info[0] != ''):
            break

        if cv.waitKey(1) == ord('q'):
            break
        
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

    print(decoded_info)
    return decoded_info[0]

def make_qr_code(data) -> Image:
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image()


if __name__ == '__main__':
    import json
    make_qr_code(
        json.dumps(
            {
                'the': {
                    'type': 'counter'
                }, 
                'world': {
                    'type': 'counter'
                }, 
                'morons': {
                    'type': 'text'
                }, 
                'stop!!': {
                    'type': 'selector', 
                    'options': ['left', 'right', 'center']
                }
            }
        )
    ).save('form.png')
    # scan_qr_code()