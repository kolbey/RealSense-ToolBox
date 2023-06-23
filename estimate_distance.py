import pyrealsense2 as rs
import numpy as np
import cv2

# Initialize RealSense camera
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
pipeline.start(config)

# Get camera intrinsics
intrinsics = None
while intrinsics is None:
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    intrinsics = color_frame.profile.as_video_stream_profile().intrinsics

# Mouse callback function
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        depth_image = np.asanyarray(depth_frame.get_data())
        depth_value = depth_image[y, x]
        depth_sensor = pipeline.get_active_profile().get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        distance = depth_value * depth_scale
        print(f"Pixel (x, y): ({x}, {y}), Distance: {distance:.2f} meters")

# Create window and set mouse callback
cv2.namedWindow('RGB Image')
cv2.setMouseCallback('RGB Image', mouse_callback)

try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # Convert color image to numpy array
        color_image = np.asanyarray(color_frame.get_data())

        # Display the color image
        cv2.imshow('RGB Image', color_image)

        if cv2.waitKey(1) == ord('q'):
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()
