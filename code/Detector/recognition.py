#!/usr/bin/python

import base64
import json
import os
import sys
import http.client as httplib
# To annotate test images a recent version of Pillow is required. Under OS X
# or Windows install via `pip install Pillow`. Under linux install the
# `python-imaging` package.
from PIL import Image, ImageDraw, ImageFont

# Set this variable to True to print all server responses.
_print_responses = False

# Your Sighthound Cloud token. More information at
# https://www.sighthound.com/support/creating-api-token
_cloud_token = "SsMRMThzZBDQ0ApxNVQUDEcXweJdWVax51qg"

# The cloud server to use, here we set the development server.
_cloud_host = "dev.sighthoundapi.com"

# A set in which to gather object names during step 1.
_object_ids = set()

# The name of the group to which we will add objects (step 2), train (step 3),
# and test with (step 4).
_group_name = "family"

# The directory where annotated test images will be written.
_output_folder = "out"


###############################################################################
def send_request(request_method, request_path, params):
    """A utility function to send API requests to the Sighthound Cloud server.

    This function will abort the script with sys.exit(1) on API errors.
    
    @param  request_method  The request method, "PUT" or "POST".
    @param  request_path    The URL path for the API request.
    @param  params          The parameters of the API request, if any.
    @return response_body   The body of the response.
    """
    # Send the request.
    headers = {"Content-type": "application/json",
               "X-Access-Token": _cloud_token}
    conn = httplib.HTTPSConnection(_cloud_host)
    conn.request(request_method, request_path, params, headers)

    # Process the response.
    response = conn.getresponse()
    body = response.read()
    error = response.status not in [200, 204]

    if _print_responses or error:
        print(response.status, body)

    if error:
        sys.exit(1)

    return body


###############################################################################
def is_image(filename):
    """A naive utility function to determine images via filename extension.

    @param  filename  The filename to examine.
    @return is_image  True if the file appears to be an image.
    """
    return filename.endswith('.png') or filename.endswith('.jpeg') or \
            filename.endswith('.jpg') or filename.endswith('.bmp')


###############################################################################
def step4_test(test_path):
    """Send images to our newly trained group to test its recognition."""
    print("Step 4: Beginning tests")
    # Create the output directory.
    if not os.path.exists(_output_folder):
        os.mkdir(_output_folder)


    # Submit all images in the test directory for recognition.
    for test_file in os.listdir(test_path):
        file_path = os.path.join(test_path, test_file)
        if not is_image(file_path):
            continue

        print("  Submitting test image " + test_file)
        base64_image = base64.b64encode(open(file_path).read())
        params = json.dumps({"image": base64_image})
        url_path = "/v1/recognition?&objectType=vehiclegroupId=" + _group_name
        response = json.loads(send_request("POST", url_path, params))

        # Annotate the image
        image = Image.open(file_path)
        font = ImageFont.load_default
        draw = ImageDraw.Draw(image)

        for face in response['objects']:
            # Retrieve and draw a bounding box for the detected face.
            json_vertices = face['faceAnnotation']['bounding']['vertices']
            vert_list = [(point['x'], point['y']) for point in json_vertices]
            draw.polygon(vert_list)

            # Retrieve and draw the id and confidence of the recongition.
            name = face['objectId']
            confidence = face['faceAnnotation']['recognitionConfidence']
            draw.text(vert_list[0], "%s - %s" % (name, confidence))

        image.save(os.path.join(_output_folder, test_file))

    print("Step 4 complete\n")


###############################################################################
if __name__ == '__main__':
    # The entry point for the recogntion sample. This expects to be called
    # with the "images" directory provided with this sample, or a directory
    # of identical structure.
    if len(sys.argv) != 2:
        print("Usage: python recognition.py <path to images directory>")
        sys.exit(2)

    root_dir = sys.argv[1]

    step4_test(os.path.join(root_dir, "reco-test"))
