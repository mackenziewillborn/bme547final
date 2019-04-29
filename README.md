# BME547 Final Project - Image Processing Server
## Mackenzie Willborn,   Kelsey Li,   Connor Johnson


This repository hosts the code for our final project. We have created a database hosting user information, raw images, processed images, and image metadata. Using our user-friendly GUI, information is sent through the server to be posted on the database and retreived for use later on.

Our server is deployed on the following virtual machine:

### Our VCM
[link] vcm

By running the im_process_GUI.py program, you can enter your username and raw files you would like to be processed. You can then pick your preffered processing type. After posting this information to the database, our program will return to you the time uploaded, total processing time, image size, histogram data, and give you the option to see your images. In the case that you upload a group of pictures, the last photo's information will be displayed back to te user after all of the information is collected and stored. 

A video demonstration of how to use our Image Processing Server can be found at the link below:


### Our Video Demo 
[link] video demo


Future Work: 
In the future, we would take this server farther by adding zip file opener functionality. This would allow the user to upload an entire zip archive of photos under their name, and get all of the images filtered at once.
