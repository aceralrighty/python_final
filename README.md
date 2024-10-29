# House Remodeling Supply Tracker

A Python web application built with Flask and SQLAlchemy to manage supplies, costs, and calculations required for remodeling various rooms in a house. Users can input detailed information about each room's remodeling needs, view cost breakdowns, and visualize expenses through data-driven insights.

---

## Objective

Create an application that:
- Tracks remodeling needs and supplies by room.
- Calculates and displays total remodeling costs, including a breakdown by flooring, tiling, and supplies.
- Offers data visualization using Seaborn to compare remodeling costs between rooms.

---

## Features

1. **Room & Supply Management**  
   - **Add and edit rooms** with remodeling specifics, including tiling and flooring costs.
   - **Track supply details** for each room, such as quantity, type, and total cost.
   - **Automatic cost calculation** based on room details and associated supplies.
   
2. **Data Visualization**  
   - Generate a Seaborn bar graph comparing total remodeling costs or tiling costs across rooms.

3. **Unit Testing**  
   - Unit tests with PyTest to validate functionality and ensure accuracy in cost calculations.

---

## Project Structure

### 1. SQLAlchemy Models

Define two primary models for structured data handling:

#### Room Model
Represents each room with its remodeling needs.
- **Fields**:
  - `id`: Integer, primary key.
  - `name`: String, name of the room.
  - `surface_area`: Float, room area in square feet.
  - `flooring_type`: String, type of flooring (e.g., Hardwood, Tile).
  - `flooring_cost_per_sqft`: Float, cost per square foot for flooring.
  - **Optional Fields** for Tiling:
    - `is_tiling_needed`: Boolean, indicates if tiling is required.
    - `tile_type`: String, type of tile (e.g., Ceramic, Porcelain).
    - `tile_cost_per_sqft`: Float, cost per square foot for tiling.
    - `tiling_area`: Float, area of the room requiring tiling.
- **Calculated Fields**:
  - `total_tile_cost`: Total tiling cost (tiling_area * tile_cost_per_sqft).
  - `total_flooring_cost`: Flooring cost (surface_area * flooring_cost_per_sqft).
  - `total_remodel_cost`: Total remodeling cost, calculated as:
    - `total_flooring_cost + total_tile_cost + sum(supply.total_supply_cost for each supply)`

#### Supply Model
Tracks materials associated with each room.
- **Fields**:
  - `id`: Integer, primary key.
  - `room_id`: Foreign key linking to Room.
  - `name`: String, name of the supply.
  - `quantity`: Integer, quantity of the supply needed.
  - `cost_per_item`: Float, cost per item.
  - `total_supply_cost`: Calculated as (quantity * cost_per_item).

### 2. Web Application Pages

#### Home Page
- List all rooms being remodeled and their total costs.

#### Add Room Page
- Form to add room details, including name, surface area, flooring type, and optional tiling information.

#### Edit Room Page
- Pre-filled form for updating an existing room's details.

#### Room Details Page
- Detailed view of a room’s remodeling information, including all cost breakdowns and supplies.

#### Add Supply Page
- Form to add new supplies to a room, including quantity and cost per item.

#### Supply Details Page
- Detailed view of a specific supply’s cost and quantity.

### 3. Calculations

- **Total Room Remodeling Cost**:
  - `total_remodel_cost = total_flooring_cost + total_tile_cost + sum(supply.total_supply_cost for each supply)`

- **Tile Cost Calculation** (if tiling is needed):
  - `total_tile_cost = tiling_area * tile_cost_per_sqft`

### 4. Seaborn Bar Graph Visualization

- A separate page will display a Seaborn bar graph comparing either total tiling or total remodeling costs across rooms.
  - **X-axis**: Room names
  - **Y-axis**: Total tiling or remodeling cost

### 5. Unit Testing with PyTest

- Unit tests for each critical function to validate cost calculations and data integrity. Aim for ~80% test coverage for robust code assurance.

---

## Getting Started

### Prerequisites
- Python 3.13
- Flask
- SQLAlchemy
- Seaborn
- PyTest

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/aceralrighty/python_final.git
   cd python_final
