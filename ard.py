from __future__ import print_function
import serial
import cv2, time
import pyzbar.pyzbar as pyzbar
import numpy as np
from math import sin, cos, sqrt, atan2, radians
import csv
latitude = [18.65204,18.65078,18.646,18.63448]
longitude = [73.76133,73.78544,73.80225,73.8288 ]
places = ["PCP","RMD College","Khandoba Mandir","IDBI Bank"]

fobj2 = open("curride.csv","w")
fobj2.close()
flag = 0

def decode(im) :
  # Find barcodes and QR codes
  decodedObjects = pyzbar.decode(im)

  # Print results
  for obj in decodedObjects:
    print('Type : ', obj.type)
    print('Data : ', str(obj.data),'\n')

  return decodedObjects

# Display barcode and QR code location
def display(im, decodedObjects):

  # Loop over all decoded objects
  for decodedObject in decodedObjects:
    points = decodedObject.polygon

    # If the points do not form a quad, find convex hull
    if len(points) > 4 :
      hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
      hull = list(map(tuple, np.squeeze(hull)))
    else :
      hull = points;

    # Number of points in the convex hull
    n = len(hull)

    # Draw the convext hull
    for j in range(0,n):
      cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)

  # Display results
  cv2.imshow("Results", im);
  cv2.waitKey(0);


# Main
if __name__ == '__main__':
    
        # Camera 0 is the integrated web cam on my netbook
        camera_port = 0
                     
        #Number of frames to throw away while the camera adjusts to light levels
        ramp_frames = 30
                     
        # Now we can initialize the camera capture object with the cv2.VideoCapture class.
        # All it needs is the index to a camera port.
        camera = cv2.VideoCapture(camera_port)
        arduinoSerialData = serial.Serial('com4',9600) #Create Serial port object called arduinoSerialData
        lol = 2
        R = 6373.0
        i =0
        a = 0

        #current stop co-ordinates
        lat1 = radians(latitude[1])
        lon1 = radians(longitude[1])
        
        while (1==1):
            flag = 0
            if (arduinoSerialData.inWaiting()>0):
                myData = arduinoSerialData.readline()
                if(float(myData) < 2.0):
                        if a != 0:
                            # Captures a single image from the camera and returns it in PIL format
                            def get_image():
                             # read is the easiest way to get a full image out of a VideoCapture object.
                             retval, im = camera.read()
                             return im
                            
                            # Ramp the camera - these frames will be discarded and are only used to allow v4l2
                            # to adjust light levels, if necessary
                            for i in range(ramp_frames):
                             temp = get_image()
                            print("Taking image...")
                            # Take the actual image we want to keep
                            camera_capture = get_image()
                            file = "sample1.png"
                            # A nice feature of the imwrite method is that it will automatically choose the
                            # correct format based on the file extension you provide. Convenient!
                            cv2.imwrite(file, camera_capture)
                             
                            # You'll want to release the camera, otherwise you won't be able to create a new
                            # capture object until your script exits
                            time.sleep(2)
                            # Read image
                            im = cv2.imread('sample1.png')
                            decodedObjects = decode(im)
                            i=0
                            with open('curride.csv') as csv_file:
                                csv_reader = csv.reader(csv_file, delimiter=',')
                                line_count = 0
                                for row in csv_reader:
                                  if row[0] == str(obj.data):
                                    flag = 1
                                    line_count += 1
                            if flag == 1:
                              print("\n-------USER Already Exists-------\n")
                              
                            if decodedObjects:
  
                                while i < 4:
                                    lat2 = radians(latitude[i])
                                    lon2 = radians(longitude[i])
                                    dlon = lon2 - lon1
                                    dlat = lat2 - lat1
                                    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                                    c = 2 * atan2(sqrt(a), sqrt(1 - a))
                                    distance = R * c
                                    if i==0:
                                        dis = distance
                                        name = places[i]
                                    elif dis > distance:
                                        dis = distance
                                        name = places[i]
                                    i+=1

                                    
                                if flag != 1:    
                                  for obj in decodedObjects:
                                    fobj = open("curride.csv","a")
                                    fobj.write(str(obj.data) + "," + str(obj.type) + "," + name + "," + "Enter" + "\n")
                                    fobj.close()
                                  print("\n_----------\nCurrent Stop:", name)
                                
                                with open('data.csv') as csv_file:
                                    csv_reader = csv.reader(csv_file, delimiter=',')
                                    line_count = 0
                                    for row in csv_reader:
                                      if row[0] == str(obj.data):
                                        print(f'\tUser:- {row[0]} uses:- {row[1]} has Due:-  {row[2]}.')
                                        line_count += 1
                                    print(f'Processed {line_count} lines.')

                            print (myData)    
                            a = a + 1
                            key = cv2.waitKey(1)
                            if key == ord('q'):
                                break
                        else:
                            print("READY")
                            a = a + 1
                            
