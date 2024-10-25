import cv2
import numpy as np

def fisheye_transform(image, strength):
    """
    Applies a fisheye distortion to the input image.

    :param image: Input image as a NumPy array.
    :param strength: Controls the strength of the fisheye effect. Smaller values mean stronger distortion.
    :return: Fisheye-distorted image.
    """
    height, width = image.shape[:2]
    # Create a new image with the same size and type as the input
    fisheye = np.zeros_like(image)

    # Calculate the center of the image
    cx = width / 2
    cy = height / 2

    # Maximum radius is the distance from the center to a corner
    max_radius = np.sqrt(cx**2 + cy**2)

    for y in range(height):
        for x in range(width):
            # Shift coordinates to center
            dx = x - cx
            dy = y - cy

            # Calculate distance from center
            r = np.sqrt(dx**2 + dy**2)

            # Normalize the radius
            r_norm = r / max_radius

            # Apply the fisheye transformation
            theta = np.arctan2(dy, dx)
            r_fisheye = r_norm + strength * (r_norm**2)

            # Ensure r_fisheye does not exceed 1
            if r_fisheye > 1:
                r_fisheye = 1

            # Map back to Cartesian coordinates
            src_x = cx + r_fisheye * max_radius * np.cos(theta)
            src_y = cy + r_fisheye * max_radius * np.sin(theta)

            # Bilinear interpolation
            if 0 <= src_x < width-1 and 0 <= src_y < height-1:
                x0 = int(np.floor(src_x))
                y0 = int(np.floor(src_y))
                dx_frac = src_x - x0
                dy_frac = src_y - y0

                for c in range(3):  # For each color channel
                    value = (image[y0, x0, c] * (1 - dx_frac) * (1 - dy_frac) +
                             image[y0, x0 + 1, c] * dx_frac * (1 - dy_frac) +
                             image[y0 + 1, x0, c] * (1 - dx_frac) * dy_frac +
                             image[y0 + 1, x0 + 1, c] * dx_frac * dy_frac)
                    fisheye[y, x, c] = np.clip(value, 0, 255)
            else:
                # Assign black to out-of-bounds pixels
                fisheye[y, x] = [0, 0, 0]

    return fisheye.astype(np.uint8)

def main():
    input_image_path = 'profile.jpeg'  
    image = cv2.imread(input_image_path)

    if image is None:
        print("Error: Image not found or unable to read.")
        return

    fisheye_image = fisheye_transform(image, strength=1.0)  

    output_image_path = './fisheye_output.jpg'
    cv2.imwrite(output_image_path, fisheye_image)
    print("Fisheye image saved to " + output_image_path)

    cv2.imshow('Original Image', image)
    cv2.imshow('Fisheye Image', fisheye_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
