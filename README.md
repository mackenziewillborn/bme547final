# BME547 Final Project - Image Processing Server
## Mackenzie Willborn,   Kelsey Li,   Connor Johnson


This repository hosts the code for our final project. We have created a database hosting user information, raw images, processed images, and image metadata. Using our user-friendly GUI, information is sent through the server to be posted on the database and retreived for use later on.

Our server is deployed on the following virtual machine:

### Our VCM
[link] vcm

By running the im_process_GUI.py program, you can enter your username and raw files you would like to be processed. You can then pick your preffered processing type. After posting this information to the database, our program will return to you the time uploaded, total processing time, image size, histogram data, and give you the option to see your images. In the case that you upload a group of pictures, the last photo's information will be displayed back to the user after all of the information is collected and stored. 

A video demonstration of how to use our Image Processing Server can be found at the link below:


### Our Video Demo 
[link] video demo


Future Work: 
In the future, we would take this server farther by adding zip file opener functionality. This would allow the user to upload an entire zip archive of photos under their name, and get all of the images filtered at once.

### GUI Instructions
The first screen of the GUI asks for the user to input a username, which will act as their user ID in the image processing database. The user should then click on the "upload raw image(s)" button, which will open up a dialog box allowing them to choose image files from their local computer to upload. Users can upload multiple images or choose only one. Once they close out of this file dialog box, the GUI will display "X files uploaded" with X being the number of files they chose. The user should then click the "Continue" button to move on to the next screen.

The next screen in the GUI asks for the user to select an image processing step to perform on the image(s). The user can only choose one at a time, and this processing method will be utilized on all uploaded images. The user should again click "Continue" to move on to the next screen of the GUI.

The final screen in the GUI displays metadata for the images uploaded in the top left of the screen. It displays the time the images were uploaded, the amount of time it took to process, and the image size. If there are multiple images, it displays the image size of the last image in the list. The user can also click the "view raw and processed images" button to display the raw and processed images side by side. The "view histograms" button provides a window with the raw vs. processed histograms with R, G, and B all plotted on the same histograms for each. For both the images and histograms, if there are multiple images, the GUI will again choose the last one in the list to display. 

On the right side of the screen, the user then chooses the filetype that they would like to download the image as, and they can choose between JPEG, PNG, and TIFF file formats. After they click the download button, once the images are downloaded successfully, a message will pop up on the screen indicating successful download. 

At this point, the user has multiple choices. They can download the processed images as a different file format by changing the type in the dropdown menu and clicking download once more. They can click "apply another processing method" to choose another method to the same photos. The "return to homepage" button sends the user back to the homepage where they can once again type in their username and choose different photos to process. Finally, if they are completely done with the image processor, they can click the "finish and exit" button to close out of the GUI. 

### Notes about the assignment
* We tried to create Sphinx documentation and followed the same exact instructions as in lecture and that we followed for previous assignments. However, we were unable to get the documentation to work, and the interface and options seemed different for some reason. We pushed the docs folder regardless to show that we attempted the documentation.
