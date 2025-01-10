import numpy as np
import plotly.graph_objects as go

def initialize_matrix():
    """
    Initializes a 3x3x3 matrix with random ternary values (-1, 0, 1).

    Returns:
        DiceInteractions (np.ndarray): A 3x3x3 NumPy array with values -1, 0, or 1.
    """
    # Define possible values
    values = [-1, 0, 1]
    
    # Initialize a 3x3x3 matrix with random ternary values
    np.random.seed(0)  # For reproducibility
    DiceInteractions = np.random.choice(values, size=(3, 3, 3))
    
    return DiceInteractions

def get_color_mapping(opacity=0.6):
    """
    Defines the color mapping for ternary values with specified opacity.

    Parameters:
        opacity (float): Opacity level between 0 (transparent) and 1 (opaque).

    Returns:
        color_mapping (dict): Dictionary mapping ternary values to RGBA colors.
    """
    color_mapping = {
        -1: f'rgba(255, 0, 0, {opacity})',     # Red with specified opacity
         0: f'rgba(128, 128, 128, {opacity})', # Gray with specified opacity
         1: f'rgba(0, 255, 0, {opacity})'      # Green with specified opacity
    }
    return color_mapping

def create_cube_trace(x, y, z, color, size=1):
    """
    Creates a cube trace for Plotly.

    Parameters:
        x, y, z (int): The coordinates of the cube's origin.
        color (str): RGBA color string.
        size (int): The size of the cube.

    Returns:
        go.Mesh3d object representing the cube.
    """
    # Define the 8 vertices of the cube
    vertices = np.array([
        [x,     y,     z],
        [x + size, y,     z],
        [x + size, y + size, z],
        [x,     y + size, z],
        [x,     y,     z + size],
        [x + size, y,     z + size],
        [x + size, y + size, z + size],
        [x,     y + size, z + size]
    ])
    
    # Define the 12 triangles composing the cube
    I = [0, 0, 0, 1, 2, 4, 5, 6, 7, 3, 3, 3]
    J = [1, 3, 4, 2, 3, 5, 6, 7, 4, 7, 2, 6]
    K = [3, 4, 5, 3, 7, 6, 7, 4, 2, 6, 7, 1]
    
    return go.Mesh3d(
        x=vertices[:,0],
        y=vertices[:,1],
        z=vertices[:,2],
        i=I,
        j=J,
        k=K,
        color=color,
        opacity=1.0,
        name=f'Cube at ({x}, {y}, {z})'
    )

def plot_cubes_plotly(matrix, color_mapping):
    """
    Plots fully colored and semi-transparent cubes based on the 3D matrix using Plotly.

    Parameters:
        matrix (np.ndarray): 3D NumPy array with values -1, 0, 1.
        color_mapping (dict): Dictionary mapping ternary values to RGBA colors.
    """
    fig = go.Figure()
    
    # Iterate through the matrix and add each cube as a separate trace
    for x in range(matrix.shape[0]):
        for y in range(matrix.shape[1]):
            for z in range(matrix.shape[2]):
                value = matrix[x, y, z]
                color = color_mapping.get(value, 'rgba(0,0,0,0)')  # Transparent if not found
                
                # Add cube to the figure
                fig.add_trace(create_cube_trace(x, y, z, color))
    
    # Define the layout
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[0, 3], autorange=False),
            yaxis=dict(range=[0, 3], autorange=False),
            zaxis=dict(range=[0, 3], autorange=False),
            aspectratio=dict(x=1, y=1, z=1)
        ),
        title='3D Visualization of DiceInteractions with Fully Colored Cubes',
        showlegend=False
    )
    
    fig.show()

def main():
    # Step 1: Initialize the matrix
    DiceInteractions = initialize_matrix()
    print("DiceInteractions Matrix:")
    print(DiceInteractions)
    
    # Step 2: Define color mapping with desired opacity
    desired_opacity = 0.6  # Adjust between 0 (transparent) and 1 (opaque)
    color_mapping = get_color_mapping(opacity=desired_opacity)
    
    # Step 3: Plot the cubes with full volume coloring and opacity using Plotly
    plot_cubes_plotly(DiceInteractions, color_mapping)

if __name__ == "__main__":
    main()
