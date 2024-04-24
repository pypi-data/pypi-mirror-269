#pip install tensorflow tensorflow-hub
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt

# Function to load an image
def load_image(image_path):
    img = tf.io.read_file(image_path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = img[tf.newaxis, :]
    return img
# Function to display an image
def show_image(image):
    image = tf.squeeze(image, axis=0)
    plt.imshow(image)
    plt.title("Stylized Image")
# Load content and style images
content_image = load_image('content_image.jpg')
style_image = load_image('style_image.jpg')
# Load the style transfer model
hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
# Perform style transfer
stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]
# Display the images
show_image(stylized_image)
plt.show()

