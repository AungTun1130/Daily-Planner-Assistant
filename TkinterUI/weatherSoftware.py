from tkinter import *
from PIL import ImageTk, Image
import requests
import json

root = Tk()
root.title("weather")
root.geometry("400x100")

# https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=89129&distance=5&API_KEY=3267ADEF-E53C-45A1-B69A-47948B016E5C
def zipLookUp():

    try:
        api_request = requests.get(
            "https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=" + zip.get()+"&distance=5&API_KEY=3267ADEF-E53C-45A1-B69A-47948B016E5C")
        api = json.loads(api_request.content)
        Airquality_scale = [
            "Good",
            "Moderate",
            "Unhealthy for Sensitive Groups",
            "Unhealthy",
            "Very Unhealthy",
            "Hazardous"
                      ]
        Airquality_color = [
            'green',
            'yellow',
            'orange',
            'red',
            '#8f3f97',
            '#7e0023'
        ]

        city = api[0]['ReportingArea']
        quality = api[0]['AQI']
        category = api[0]['Category']['Name']
        # for testing
        # category = Airquality_scale[4]

        if category == Airquality_scale[0]:
            weather_color = Airquality_color[0]
        elif category == Airquality_scale[1]:
            weather_color = Airquality_color[1]
        elif category == Airquality_scale[2]:
            weather_color = Airquality_color[2]
        elif category == Airquality_scale[3]:
            weather_color = Airquality_color[3]
        elif category == Airquality_scale[4]:
            weather_color = Airquality_color[4]
        elif category == Airquality_scale[5]:
            weather_color = Airquality_color[5]
        myLabel = Label(root, text=city + " Air Quality " + str(quality) + " " + category, font=("Arial", 20),
                        background=weather_color)
        myLabel.grid(row = 1,column = 0,columnspan = 2)
        root.configure(background=weather_color)
    except Exception as e:
        api = "Error..."
        myLabel = Label(root, text=api, font=("Arial", 20),
                        background='green')
        myLabel.grid(row = 1,column = 0,columnspan = 2)

zip = Entry(root)
zip.grid(row = 0,column = 0,sticky = W+E+N+S)

zip_btn = Button(root,text = "lookup zipcode",command = zipLookUp)
zip_btn.grid(row = 0,column = 1,sticky = W+E+N+S)


root.mainloop()
