import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import calculations as calc


def remove_mesh_points(X, Y, h1, h2, K, W, L):
    h = calc.get_h(h1, h2, K, W, L, X[0])

    if calc.get_h_max(h1, h2, K, W, L) >= 0:
        for i in range(len(X)):
            for j in range(len(X[0])):
                if Y[i][j] > h[j]:
                    X[i][j] = None
                    Y[i][j] = None
    else:
        for i in range(len(X)):
            for j in range(len(X[0])):
                if Y[i][j] > h[j]:
                    X[i][j] = None
                    Y[i][j] = None

    return [X, Y]

def get_topography_line(x, h):
    shift = [5, 5.5, 5.8, 6.0, 5.8, 5.5, 6.3, 6.8, 7.0, 7.4, 7.8, 8.2, 8, 7.5, 6.8, 5, 4]*3
    x_top = np.linspace(0, len(x), 17)
    y_top = max(h) + shift

    topography_line = go.Scatter(x=x_top, y=y_top, mode='lines', line=dict(color='Sienna'), name="topography")
    return topography_line

def initialize_elevation_plot(h1, h2, K, W, L, arrow_visibility):
    elevation_plot = go.Figure()
    # Initializing traces with plot.add_trace
    x = np.linspace(0, L, 1000)  # should go to the max L value
    h = calc.get_h(h1, h2, K, W, L, x)
    q = calc.get_q(h1, h2, K, W, L, x)
    d = calc.get_d(h1, h2, K, W, L)

    # elevation plot
    elevation_plot.add_trace(go.Scatter(x=x, y=h, line=dict(color='MediumTurquoise'), name="h"))

    index = min(range(len(x)), key=lambda i: abs(x[i] - d))
    elevation_plot.add_trace(
        go.Scatter(x=[d, d], y=[0, h[index]], mode='lines', line=dict(color='FireBrick'), name="d"))

    elevation_plot.update_layout(xaxis_title='x (m)', yaxis_title="Water Table Elevation (m)")
    elevation_plot.update_xaxes(range=[0, L])
    elevation_plot.layout.title = "Elevation Plot"
    elevation_plot.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    # elevation_plot.update_layout(annotations=get_arrows(h1, L, q, x))

    if 'visible' in arrow_visibility:
        # quiver plot
        x_quiver = np.linspace(L / 8, L - (L / 8), 8)
        y_quiver = np.linspace(0, (5 / 6) * max(h), 5)  # go to max y value
        X, Y = np.meshgrid(x_quiver, y_quiver)
        X, Y = remove_mesh_points(X, Y, h1, h2, K, W, L)
        u = calc.get_q(h1, h2, K, W, L, X) * 20
        v = Y * 0
        quiver_plot = ff.create_quiver(X, Y, u, v, arrow_scale=0.3, angle=np.pi / (9 * 16), name="qx")
        elevation_plot.add_traces(data=quiver_plot.data)

    #topography line
    elevation_plot.add_trace(get_topography_line(x, h))

    elevation_plot.add_hrect(y0=-4, y1=0, line_width=0, fillcolor="grey", opacity=1)

    return elevation_plot


def initialize_q_plot(h1, h2, K, W, L):
    q_plot = go.Figure()
    # Initializing traces with plot.add_trace
    x = np.linspace(0, L, 1000)  # should go to the max L value
    h = calc.get_h(h1, h2, K, W, L, x)
    q = calc.get_q(h1, h2, K, W, L, x)
    d = calc.get_d(h1, h2, K, W, L)

    # q plot
    q_plot.add_trace(go.Scatter(x=x, y=q, line=dict(color='MediumPurple'), name="q"))

    q_plot.add_trace(go.Scatter(x=[x[0], x[-1]], y=[0, 0], mode='lines', line=dict(color='FireBrick'), name="0"))

    q_plot.update_layout(xaxis_title='x (m)', yaxis_title="qx (m^2/day)")
    q_plot.update_xaxes(range=[0, L])
    q_plot.layout.title = "q Plot"
    q_plot.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    return q_plot


def update_elevation_plot(h1, h2, K, W, L, arrow_visibility, elevation_plot):
    x = np.linspace(0, L, 1000)
    h = calc.get_h(h1, h2, K, W, L, x)
    d = calc.get_d(h1, h2, K, W, L)

    # Updating specific traces using their index in plot.data
    # elevation plot
    elevation_plot.data[0].x = x
    elevation_plot.data[0].y = h

    index = min(range(len(x)), key=lambda i: abs(x[i] - d))
    elevation_plot.data[1].x = [d, d]
    elevation_plot.data[1].y = [0, h[index]]

    elevation_plot.update_xaxes(range=[0, L])

    if 'visible' in arrow_visibility:
        # quiver plot
        x_quiver = np.linspace(L / 8, L - (L / 8), 8)
        y_quiver = np.linspace(0, (5 / 6) * max(h), 5)  # go to max y value
        X, Y = np.meshgrid(x_quiver, y_quiver)
        X, Y = remove_mesh_points(X, Y, h1, h2, K, W, L)
        u = calc.get_q(h1, h2, K, W, L, X) * 20
        v = Y * 0
        quiver_plot = ff.create_quiver(X, Y, u, v, arrow_scale=0.3, angle=np.pi / (9 * 16))

        elevation_plot.data[2].x = quiver_plot.data[0].x
        elevation_plot.data[2].y = quiver_plot.data[0].y
    else:
        elevation_plot.data[2].x = []
        elevation_plot.data[2].y = []


    # topography line
    topography_plot = get_topography_line(x, h)
    elevation_plot.data[3].x = topography_plot.x
    elevation_plot.data[3].y = topography_plot.y

    return elevation_plot


def update_q_plot(h1, h2, K, W, L, q_plot):
    x = np.linspace(0, L, 1000)
    q = calc.get_q(h1, h2, K, W, L, x)

    # q plot
    q_plot.data[0].x = x
    q_plot.data[0].y = q

    q_plot.update_xaxes(range=[0, L])

    return q_plot