# House Remodeling Supply Tracker

A Python web application using Flask and SQLAlchemy to track supplies, costs, and requirements for remodeling rooms in a house. This application enables users to input detailed remodeling information, view cost breakdowns, and visualize costs across rooms with Seaborn bar graphs.

---

## Objective

The project aims to:
- Track and manage room-specific remodeling needs and associated supplies.
- Calculate and display total remodeling costs, including a breakdown for flooring, tiling, and supplies.
- Provide data visualizations to compare remodeling expenses across rooms.

---

## Key Features

1. **Room and Supply Management**
   - Add and edit room details, including floor and tiling specifics.
   - Track individual supplies required for each room.
   - Calculate total costs based on user inputs.

2. **Data Visualization**
   - Display a Seaborn bar graph comparing remodeling costs across rooms.

3. **Unit Testing**
   - Use PyTest to ensure accuracy in calculations and application functionality.

---

## Project Requirements

### 1. SQLAlchemy Models

The application uses two main models for data organization:

#### Room Model
Defines remodeling specifics for each room.
- **Fields**:
  - `id`: Primary key.
  - `name`: Name of the room.
  - `surface_area`: Room area in square feet.
  - `flooring_type`: Type of flooring (e.g., Hardwood, Tile).
  - `flooring_cost_per_sqft`: Flooring cost per square foot.
  - **Optional Tiling Fields**:
    - `is_tiling_needed`: Boolean indicating if tiling is required.
    - `tile_type`: Type of tile (e.g., Ceramic, Porcelain).
    - `tile_cost_per_sqft`: Tiling cost per square foot.
    - `tiling_area`: Area requiring tiling.
- **Calculated Fields**:
  - `total_tile_cost`: Tiling cost (`tiling_area * tile_cost_per_sqft`).
  - `total_flooring_cost`: Flooring cost (`surface_area * flooring_cost_per_sqft`).
  - `total_remodel_cost`: Total remodeling cost, calculated as:
    - `total_flooring_cost + total_tile_cost + sum(supply.total_supply_cost for each supply)`

#### Supply Model
Tracks individual supplies for each room.
- **Fields**:
  - `id`: Primary key.
  - `room_id`: Foreign key linking to Room.
  - `name`: Supply name.
  - `quantity`: Quantity required.
  - `cost_per_item`: Cost per item.
  - `total_supply_cost`: Total cost of the supply (`quantity * cost_per_item`).

---

### 2. Web Application Pages

#### Home Page
- Lists all rooms being remodeled with their total remodeling costs.

#### Add Room Page
- Form to add a new room, capturing:
  - Room name
  - Surface area
  - Flooring type and cost
  - Optional tiling details (tile type, cost, and area if applicable)

#### Edit Room Page
- Form pre-filled with room data for editing.

#### Room Details Page
- Shows room details including flooring, tiling, and associated supply costs.
- Displays total remodeling cost, calculated as:
  - `total_remodel_cost = total_flooring_cost + total_tile_cost + sum(supply.total_supply_cost for each supply)`

#### Add Supply Page
- Form to add supplies for a room, capturing:
  - Supply name
  - Quantity
  - Cost per item

#### Supply Details Page
- Displays details of a specific supply, including total cost.

---

### 3. Calculations

#### Total Room Remodeling Cost
- Calculated as:
  - `total_remodel_cost = total_flooring_cost + total_tile_cost + sum(supply.total_supply_cost for each supply)`
- Includes:
  - Flooring cost (`surface_area * flooring_cost_per_sqft`)
  - Tiling cost (`tiling_area * tile_cost_per_sqft` if tiling is needed)
  - Supply costs (`quantity * cost_per_item` for each supply)

---

### 4. Data Visualization

The application includes a Seaborn bar graph to compare costs between rooms:
- **X-axis**: Room names
- **Y-axis**: Total tiling or total remodeling cost
- Helps users visualize and compare expenses quickly.

---

### 5. Unit Testing with PyTest

- Develop unit tests to validate all major calculations and functionalities.
- Aim for ~80% test coverage to ensure robust application performance.

---

## Getting Started

### Prerequisites
- Python 3.x
- Flask
- SQLAlchemy
- Seaborn
- PyTest

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/house_remodeling_tracker.git
   cd house_remodeling_tracker
