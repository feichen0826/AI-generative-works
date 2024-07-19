import functools
import os
import tensorflow as tf
import matplotlib.pyplot as plt
from matplotlib import gridspec
import tensorflow_hub as hub

# Define functions from previous code
def crop_center(image):
    """Returns a cropped square image."""
    shape = image.shape
    new_shape = min(shape[1], shape[2])
    offset_y = max(shape[1] - shape[2], 0) // 2
    offset_x = max(shape[2] - shape[1], 0) // 2
    image = tf.image.crop_to_bounding_box(
        image, offset_y, offset_x, new_shape, new_shape)
    return image

@functools.lru_cache(maxsize=None)
def load_image(image_url, image_size=(256, 256), preserve_aspect_ratio=True):
    """Loads and preprocesses images."""
    # Cache image file locally.
    image_path = tf.keras.utils.get_file(os.path.basename(image_url)[-128:], image_url)
    # Load and convert to float32 numpy array, add batch dimension, and normalize to range [0, 1].
    img = tf.io.decode_image(
        tf.io.read_file(image_path),
        channels=3, dtype=tf.float32)[tf.newaxis, ...]
    img = crop_center(img)
    img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
    return img

def show_n(images, titles=('',)):
    n = len(images)
    image_sizes = [image.shape[1] for image in images]
    w = (image_sizes[0] * 6) // 320
    plt.figure(figsize=(w * n, w))
    gs = gridspec.GridSpec(1, n, width_ratios=image_sizes)
    for i in range(n):
        plt.subplot(gs[i])
        plt.imshow(images[i][0], aspect='equal')
        plt.axis('off')
        plt.title(titles[i] if len(titles) > i else '')
    plt.show()

# Load example images
content_image_url = 'https://images.unsplash.com/photo-1570129476815-ba368ac77013?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
style_image_url = 'https://images.squarespace-cdn.com/content/v1/603b4ec9b81d5532a0a57e30/780666c7-f57a-4bb9-aab1-3326a0c12f87/2FDF8F5F-FFA6-4D2C-84C9-0458AD10B939.jpeg?format=1000w'
output_image_size = 384

# The content image size can be arbitrary.
content_img_size = (output_image_size, output_image_size)
# The style prediction model was trained with image size 256 and it's the
# recommended image size for the style image (though, other sizes work as
# well but will lead to different results).
style_img_size = (256, 256)

# Load and preprocess the content and style images
content_image = load_image(content_image_url, content_img_size)
style_image = load_image(style_image_url, style_img_size)
style_image = tf.nn.avg_pool(style_image, ksize=[3,3], strides=[1,1], padding='SAME')

# Display the content and style images
show_n([content_image, style_image], ['Content image', 'Style image'])

# Load TF Hub module
hub_handle = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
hub_module = hub.load(hub_handle)

# Stylize the content image with the style image using the loaded TF Hub module
# outputs = hub_module(content_image, style_image)
# stylized_image = outputs[0]

# # Display the stylized image
# plt.figure(figsize=(8, 8))
# plt.imshow(stylized_image[0])
# plt.axis('off')
# plt.show()
# Stylize content image with given style image
outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
stylized_image = outputs[0]

# Visualize input images and the generated stylized image
show_n([content_image, style_image, stylized_image], titles=['Original content image', 'Style image', 'Stylized image'])
