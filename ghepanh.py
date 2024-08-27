from tkinter import *
import tkinter.filedialog as filedialog
from panorama import Panaroma
import imutils
import cv2

root = Tk()
root.title("Ghép ảnh panorama")
root.resizable(height=False, width=False)
root.minsize(height=200, width=400)


def input():
    input_path = filedialog.askopenfilenames()
    input_entry.delete(0, END)
    input_entry.insert(0, input_path)


def giai():
    filename = []
    filename = input_entry.get().split()

    images = []

    for i in range(len(filename)):
        images.append(cv2.imread(filename[i]))

    for i in range(len(images)):
        images[i] = imutils.resize(images[i], width=400)
        images[i] = imutils.resize(images[i], height=400)

    no_of_images = len(images)

    panaroma = Panaroma()
    if no_of_images == 2:
        (result, matched_points) = panaroma.image_stitch([images[0], images[1]], match_status=True)
    else:
        (result, matched_points) = panaroma.image_stitch([images[no_of_images - 2], images[no_of_images - 1]],
                                                         match_status=True)
        for i in range(no_of_images - 2):
            (result, matched_points) = panaroma.image_stitch([images[no_of_images - i - 3], result], match_status=True)

    for i in range(no_of_images):
        cv2.imshow("Image {k}".format(k=i + 1), images[i])

    cv2.imshow("Keypoint Matches", matched_points)
    cv2.imshow("Panorama", result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


top_frame = Frame(root)
bottom_frame = Frame(root)
line = Frame(root, height=1, width=400, bg="grey80", relief='groove')
top_frame.pack(side=TOP)
line.pack(pady=10)
bottom_frame.pack(side=BOTTOM)
input_path = Label(top_frame, text="Đường dẫn ảnh:")
input_entry = Entry(top_frame, text="", width=40)
browse1 = Button(top_frame, text="Chọn ảnh", command=input)
input_path.pack(pady=5)
input_entry.pack(pady=5)
browse1.pack(pady=5)
button = Button(bottom_frame, text='Ghép ảnh', command=giai)
button.pack(pady=20, fill=X)
root.mainloop()


