import tkinter as tk
from tkinter import messagebox, ttk
import requests
import geocoder
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageTk

API_KEY = "a03925489d4ab7889a4e0135802714d2"


# ---------------- FUNCTIONS ----------------

def get_weather_by_city():
    city = city_entry.get().strip()
    if city:
        fetch_weather(city)
        fetch_forecast(city)
        add_recent_city(city)
    else:
        messagebox.showwarning("Warning", "Please enter a city name.")


def use_current_location():
    g = geocoder.ip("me")
    if g.ok:
        lat, lon = g.latlng
        fetch_weather_by_coords(lat, lon)
        fetch_forecast_by_coords(lat, lon)
    else:
        messagebox.showerror("Error", "Unable to detect current location.")


def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        res = requests.get(url)
        data = res.json()

        city_label.config(text=f"{data['name']} ({datetime.now().strftime('%Y-%m-%d')})")
        temp_label.config(text=f"Temperature: {data['main']['temp']}°C")
        wind_label.config(text=f"Wind: {data['wind']['speed']} M/S")
        humidity_label.config(text=f"Humidity: {data['main']['humidity']}%")
        desc_label.config(text=data['weather'][0]['description'])

        icon_url = f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
        icon_data = requests.get(icon_url).content
        icon_img = Image.open(BytesIO(icon_data))
        icon_photo = ImageTk.PhotoImage(icon_img)
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo

        current_frame.pack(pady=10, fill="x")
    except Exception:
        messagebox.showerror("Error", "Failed to fetch weather data.")


def fetch_weather_by_coords(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    fetch_weather_from_url(url)


def fetch_weather_from_url(url):
    try:
        res = requests.get(url)
        data = res.json()
        city_label.config(text=f"{data['name']} ({datetime.now().strftime('%Y-%m-%d')})")
        temp_label.config(text=f"Temperature: {data['main']['temp']}°C")
        wind_label.config(text=f"Wind: {data['wind']['speed']} M/S")
        humidity_label.config(text=f"Humidity: {data['main']['humidity']}%")
        desc_label.config(text=data['weather'][0]['description'])

        icon_url = f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
        icon_data = requests.get(icon_url).content
        icon_img = Image.open(BytesIO(icon_data))
        icon_photo = ImageTk.PhotoImage(icon_img)
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo

        current_frame.pack(pady=10, fill="x")
    except Exception:
        messagebox.showerror("Error", "Failed to fetch weather data.")


def fetch_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    fetch_forecast_from_url(url)


def fetch_forecast_by_coords(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    fetch_forecast_from_url(url)


def fetch_forecast_from_url(url):
    try:
        res = requests.get(url)
        data = res.json()
        for widget in forecast_frame.winfo_children():
            widget.destroy()

        daily = {}
        for entry in data["list"]:
            date = entry["dt_txt"].split(" ")[0]
            if "12:00:00" in entry["dt_txt"] and date not in daily:
                daily[date] = entry

        for i, (date, entry) in enumerate(list(daily.items())[:5]):
            frame = tk.Frame(forecast_frame, bg="#1e293b", bd=2, relief="ridge")
            frame.pack(side="left", padx=5, pady=5)

            icon_url = f"http://openweathermap.org/img/wn/{entry['weather'][0]['icon']}@2x.png"
            icon_data = requests.get(icon_url).content
            icon_img = Image.open(BytesIO(icon_data))
            icon_photo = ImageTk.PhotoImage(icon_img)

            tk.Label(frame, text=f"{date}", bg="#1e293b", fg="white").pack()
            tk.Label(frame, image=icon_photo, bg="#1e293b").pack()
            tk.Label(frame, text=f"Temp: {entry['main']['temp']}°C", bg="#1e293b", fg="white").pack()
            tk.Label(frame, text=f"Wind: {entry['wind']['speed']} M/S", bg="#1e293b", fg="white").pack()
            tk.Label(frame, text=f"Humidity: {entry['main']['humidity']}%", bg="#1e293b", fg="white").pack()

            frame.image = icon_photo  # keep a reference

        forecast_label.pack()
        forecast_frame.pack(pady=10)
    except Exception:
        messagebox.showerror("Error", "Failed to fetch forecast data.")


def add_recent_city(city):
    if city not in recent_cities:
        recent_cities.insert(0, city)
        if len(recent_cities) > 5:
            recent_cities.pop()
        update_recent_dropdown()


def update_recent_dropdown():
    recent_menu["values"] = recent_cities


def select_recent(event):
    city = recent_menu.get()
    if city:
        fetch_weather(city)
        fetch_forecast(city)
        city_entry.delete(0, tk.END)
        city_entry.insert(0, city)


# ---------------- GUI SETUP ----------------

root = tk.Tk()
root.title("Weather Dashboard")
root.geometry("700x600")
root.config(bg="#dbeafe")

title = tk.Label(root, text="Weather Dashboard", bg="#2563eb", fg="white", font=("Arial", 18, "bold"), pady=10)
title.pack(fill="x")

input_frame = tk.Frame(root, bg="#dbeafe")
input_frame.pack(pady=10)

city_entry = tk.Entry(input_frame, width=25, font=("Arial", 12))
city_entry.grid(row=0, column=0, padx=10)

search_btn = tk.Button(input_frame, text="Search", bg="#2563eb", fg="white", command=get_weather_by_city)
search_btn.grid(row=0, column=1, padx=5)

location_btn = tk.Button(input_frame, text="Use Current Location", bg="#374151", fg="white", command=use_current_location)
location_btn.grid(row=0, column=2, padx=5)

recent_cities = []
recent_menu = ttk.Combobox(input_frame, values=recent_cities, width=25)
recent_menu.grid(row=0, column=3, padx=5)
recent_menu.set("Recently Searched")
recent_menu.bind("<<ComboboxSelected>>", select_recent)

# Current Weather Display
current_frame = tk.Frame(root, bg="#bfdbfe", padx=10, pady=10)
city_label = tk.Label(current_frame, text="", font=("Arial", 14, "bold"), bg="#bfdbfe")
city_label.pack()
temp_label = tk.Label(current_frame, text="", bg="#bfdbfe")
temp_label.pack()
wind_label = tk.Label(current_frame, text="", bg="#bfdbfe")
wind_label.pack()
humidity_label = tk.Label(current_frame, text="", bg="#bfdbfe")
humidity_label.pack()
desc_label = tk.Label(current_frame, text="", bg="#bfdbfe")
desc_label.pack()
icon_label = tk.Label(current_frame, bg="#bfdbfe")
icon_label.pack()

# Forecast Section
forecast_label = tk.Label(root, text="5-Day Forecast", font=("Arial", 12, "bold"), bg="#dbeafe")
forecast_frame = tk.Frame(root, bg="#dbeafe")

root.mainloop()
