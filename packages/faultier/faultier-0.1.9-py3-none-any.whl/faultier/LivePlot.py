        
import plotly.graph_objs as go
def update_vline_position(fig, old_x, new_x):
    for shape in fig.layout.shapes:
        if shape.type == 'line' and shape.x0 == old_x and shape.x1 == old_x:
            shape.update(x0=new_x, x1=new_x)
            break

class LivePlot:
    def __init__(self):
        self.fig = go.FigureWidget(data=[go.Scatter(y=[])])
        self.fig.update_layout(yaxis=dict(range=[0, 1]))
        self.fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
        )
        vline = self.fig.add_vline(x=200, line_width=1, line_dash="dash", line_color="red")
        self.vline_x = 200
        display(self.fig)
    
    def update(self, data):
        """
        Updates the live figure.

        :param data: Takes the data in the format [5, 3, 2, 1, ...]
        """

        self.fig.data[0].y = data

    def update_vline(self, x):
        """
        Updates the vertical marker on the graph.

        :param data: Takes in the X position on which to place the marker.
        """

        update_vline_position(self.fig, old_x=self.vline_x, new_x=x)
        self.vline_x = x

class LiveMarkerPlot:
    def __init__(self):
        self.fig = go.FigureWidget(data=[
            go.Scatter(x=[0], y=[0], mode="markers"),
            go.Scatter(x=[0], y=[0], mode="markers")
        ])
        # self.fig.update_layout(yaxis=dict(range=[0, 1]))
        self.fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="Delay",
            yaxis_title="Pulse"
        )
        # vline = self.fig.add_vline(x=200, line_width=1, line_dash="dash", line_color="red")
        self.vline_x = 200
        display(self.fig)
    
    def update(self, data):
        """
        Updates the live figure.

        :param data: Takes the scatters in the format [[4000, 8], [3950, 4]]
        """
        
        x_values = [point[0] for point in data[0]]
        y_values = [point[1] for point in data[0]]

        self.fig.data[0].x = x_values
        self.fig.data[0].y = y_values

        x_values = [point[0] for point in data[1]]
        y_values = [point[1] for point in data[1]]

        self.fig.data[1].x = x_values
        self.fig.data[1].y = y_values

    # def update_vline(self, x):
    #     pass
    #     # update_vline_position(self.fig, old_x=self.vline_x, new_x=x)
    #     # self.vline_x = x