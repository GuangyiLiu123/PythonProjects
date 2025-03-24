import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import geopandas as gpd
import random
from shapely.geometry import Point
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Create a plot of the world map using Cartopy
fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection=ccrs.PlateCarree())

# Set extent to only show the middle third of the world map
ax.set_extent([-40, 60, -40, 40], crs=ccrs.PlateCarree())

# Add land and country borders
ax.add_feature(cfeature.BORDERS, edgecolor='black', linewidth=1)
ax.add_feature(cfeature.COASTLINE, edgecolor='black', linewidth=1)
ax.add_feature(cfeature.LAND, facecolor='lightgray')

# Read shapefile
africa = gpd.read_file(r'') # replace this with a respective shp file for map

# Detect column case-insensitively
columns_lower = [col.lower() for col in africa.columns]
if 'adm0_name' in columns_lower:
    name_column = 'ADM0_NAME'
elif 'adm0_name'.upper() in africa.columns:
    name_column = 'ADM0_NAME'.upper()
else:
    raise ValueError("Could not find 'ADM0_NAME' in the shapefile columns")

# Extract a list of countries from the shapefile
country_names = africa[name_column].unique().tolist()

# Initialize game variables
current_country = None
score = 0
total_questions = 10
question_count = 0

# Function to select a random country to guess
def choose_new_country():
    global current_country, question_count
    if question_count < total_questions:
        current_country = random.choice(country_names)
        print(f"New target country: {current_country}")
        question_count += 1
    else:
        ax.set_title(f"Game Over! Your final score is {score}/{total_questions}", fontsize=14, fontweight='bold')
        fig.canvas.mpl_disconnect(cid)

# Function to check if the clicked country is the current target
def on_click(event):
    global current_country, score, question_count
    
    if event.inaxes != ax:
        return
    
    click_point = Point(event.xdata, event.ydata)
    
    for i, row in africa.iterrows():
        if row['geometry'].contains(click_point):
            clicked_country = row[name_column]
            
            if clicked_country == current_country:
                print(f"Correct! You clicked on {clicked_country}")
                score += 1
                color = 'green'
            else:
                print(f"Wrong! You clicked on {clicked_country}, but we wanted {current_country}")
                color = 'red'
            
            highlight_country(row['geometry'], color=color)
            
            if question_count < total_questions:
                choose_new_country()
            else:
                ax.set_title(f"Game Over! Your final score is {score}/{total_questions}", fontsize=14, fontweight='bold')
                fig.canvas.mpl_disconnect(cid)
            update_title()
            break

# Function to highlight the country that was clicked
def highlight_country(geometry, color='green'):
    ax.add_geometries([geometry], ccrs.PlateCarree(), facecolor=color, edgecolor='black', linewidth=2, alpha=0.6)
    plt.draw()

# Function to update the title at the top
def update_title():
    ax.set_title(f"Find: {current_country} | Score: {score}/{total_questions} | Question {question_count}/{total_questions}", 
                 fontsize=14, fontweight='bold')

# Function to reset the game
def reset_game(event):
    global score, question_count, current_country
    
    # Reset game variables
    score = 0
    question_count = 0
    
    # Clear map content (without affecting button and title)
    for collection in ax.collections[:]:  # Only clear plotted geometries, not title or button
        collection.remove()
    for patch in ax.patches[:]:  # Clear any highlighted countries
        patch.remove()
    for artist in ax.artists[:]:  # Remove artists if any
        artist.remove()

    # Reset the map extent and redraw it
    ax.set_extent([-40, 60, -40, 40], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    
    # Start a new round
    choose_new_country()
    update_title()
    plt.draw()

# Set up the first question
choose_new_country()
update_title()

# Connect the click event to the on_click function
cid = fig.canvas.mpl_connect('button_press_event', on_click)

# **Create a separate axis for the reset button**
ax_button = plt.axes([0.8, 0.02, 0.1, 0.05])  # [x, y, width, height]
button = Button(ax_button, 'Reset')
button.on_clicked(reset_game)

plt.show()
