# reading an image
# # imread function of cv2 is used to read an image
# img = cv2.imread("Resources/profile_photo.jpeg")
# # imshow function outputs the image
# cv2.imshow("Output",img)
# # waitKey function is used to add some wait to the output image
# # waitKey(0) means an infinite wait
# cv2.waitKey(0)

# # Reading from a video
# cap = cv2.VideoCapture("Resources/test_video.mp4")
# while True:
#     # saving the image in img variable 
#     # success would denote whether this was done successfully or not
#     # success is a boolean variable
#     success,vid = cap.read()
#     cv2.imshow("Video",vid)
#     # adding a delay and exiting the video on pressing q button
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break