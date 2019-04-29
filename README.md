# BME547 Final Project - Image Processing Server
## Mackenzie Willborn,   Kelsey Li,   Connor Johnson


This repository hosts the code for our final project. We have created a database hosting user information, raw images, processed images, and image metadata. Using our user-friendly GUI, information is sent through the server to be posted on the database and retreived for use later on.

Our server is deployed on the following virtual machine:

### Instructions on how to use the Image Processor
Enter the repository with the im_process_server.py code, and run ‘python3 im_process_server.py’ from the command line. Next, the im_process_GUI.py code should be run using ‘python3 im_process_GUI.py’ from the command line of a different terminal. The server code MUST be run before the client code.


### Our VCM
[link] vcm


By running the im_process_GUI.py program, you can enter your username and raw files you would like to be processed. You can then pick your preffered processing type. After posting this information to the database, our program will return to you the time uploaded, total processing time, image size, histogram data, and give you the option to see your images. In the case that you upload a group of pictures, the last photo's information will be displayed back to the user after all of the information is collected and stored. 

A video demonstration of how to use our Image Processing Server can be found at the link below:


### Our Video Demo 
Video 1: 
https://www.youtube.com/watch?v=7QLEyzB_IaU&list=UUxdHCy01O9jHalYY56hoMuA&index=4

Video 2:
https://www.youtube.com/watch?v=RRjM5IxGH3c&list=UUxdHCy01O9jHalYY56hoMuA&index=3 


### GUI Instructions
The first screen of the GUI asks for the user to input a username, which will act as their user ID in the image processing database. The user should then click on the "upload raw image(s)" button, which will open up a dialog box allowing them to choose image files from their local computer to upload. Users can upload multiple images or choose only one. Once they close out of this file dialog box, the GUI will display "X files uploaded" with X being the number of files they chose. The user should then click the "Continue" button to move on to the next screen.

The next screen in the GUI asks for the user to select an image processing step to perform on the image(s). The user can only choose one at a time, and this processing method will be utilized on all uploaded images. The user should again click "Continue" to move on to the next screen of the GUI.

The final screen in the GUI displays metadata for the images uploaded in the top left of the screen. It displays the time the images were uploaded, the amount of time it took to process, and the image size. If there are multiple images, it displays the image size of the last image in the list. The user can also click the "view raw and processed images" button to display the raw and processed images side by side. The "view histograms" button provides a window with the raw vs. processed histograms with R, G, and B all plotted on the same histograms for each. For both the images and histograms, if there are multiple images, the GUI will again choose the last one in the list to display. 

On the right side of the screen, the user then chooses the filetype that they would like to download the image as, and they can choose between JPEG, PNG, and TIFF file formats. After they click the download button, once the images are downloaded successfully, a message will pop up on the screen indicating successful download. The default download type is JPEG. If multiple files were uploaded, the processed images will be saved to a zip archive.

At this point, the user has multiple choices. They can download the processed images as a different file format by changing the type in the dropdown menu and clicking download once more. They can click "apply another processing method" to choose another method to the same photos. The "return to homepage" button sends the user back to the homepage where they can once again type in their username and choose different photos to process. Finally, if they are completely done with the image processor, they can click the "finish and exit" button to close out of the GUI. 

### Instructions on how to use the test_im_process.py module
To run unit testing on the im_process_server.py module, the user should execute ‘pytest -v’ from the terminal. This will return PASSED or FAILED corresponding to each unit test that was developed.

### Notes about the assignment
* Our server is deployed on http://vcm-9060.vm.duke.edu:5000
* Virtual Environment: A virtual environment called env was used for the project, and the associated requirements.txt file.
* Pep-8: To check if the modules comply with PEP-8 Style Guide, the command "pytest -v --pep8" can be typed into the terminal. TravisCI was enabled and used in the repository, and feature branches were merged with the master branch only after TravisCI reported a passing status.
* We tried to create Sphinx documentation and followed the same exact instructions as in lecture and that we followed for previous assignments. However, we were unable to get the documentation to work, and the interface and options seemed different for some reason. We pushed the docs folder regardless to show that we attempted the documentation.
* The histogram equalization processing method processes correctly in the server, but when the image is converted over to the GUI to be displayed or downloaded, it becomes just a black image. The data types and manipulation for histogram equalization are the same in our code as all of the other processing types, so we aren't sure why this is happening. We created an issue and discussed this with Dr. Ward who also didn't know what the root cause was.
* We included code in the GUI to accept zip files as input for the image processor. However, the function we were using only returned the file extension name rather than the entire file path, and we were unable to figure out how to find the full file path to integrate into our code.

### Status Badge

[![Build Status](https://travis-ci.org/mackenziewillborn/bme547final.svg?branch=master)](https://travis-ci.org/mackenziewillborn/bme547final)
