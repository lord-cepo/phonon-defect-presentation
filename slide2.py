from manim import *
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.colors import Normalize
from manim_slides import Slide

FAST = False
formula = {
    'lattice_function': r"f(R_1, R_2) = f(R_1 + R, R_2+R)",
    'tau': r"\tau = 1 \\ \alpha = 1",
}

# save only the imshow central image to an image object
def construct_imshow(filename, function=None, extent=None, n_pixels=None):
    x_vals = np.linspace(extent[0], extent[1], n_pixels)
    y_vals = np.linspace(extent[2], extent[3], n_pixels)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = function(X, Y)

    norm = Normalize(vmin=np.min(Z), vmax=np.max(Z))
    Z_normalized = norm(Z)

    # Get RGB using colormap
    colored_image = plt.get_cmap('viridis')(Z_normalized)

    # Create a fading mask based on distance from center
    distances = np.zeros((4, x_vals.size, y_vals.size))
    distances[0,:,:] = np.abs(X-extent[0])
    distances[1,:,:] = np.abs(Y-extent[2])
    distances[2,:,:] = np.abs(extent[1]-X)
    distances[3,:,:] = np.abs(extent[3]-Y)
    alpha_mask = np.arctan(np.min(distances, axis=0) * 2) / np.pi
    # Apply mask to alpha channel
    colored_image[..., 3] = alpha_mask  # Set alpha channel

    window_1d = np.hanning(n_pixels)
    window_2d = np.outer(window_1d, window_1d)
    Z *= window_2d
    # Compute the 2D Fourier Transform
    # Z -= np.mean(Z)  # Remove the DC component
    fft_result = np.fft.fft2(Z)  # Perform the 2D FFT
    fft_shifted = np.fft.fftshift(fft_result)  # Shift the zero frequency to the center
    # fft_result -= np.mean(fft_result)
    fftZ = np.abs(fft_shifted)  # Compute the magnitude of the FFT
    print(np.min(fftZ), np.max(fftZ))
    norm = Normalize(vmin=np.min(fftZ), vmax=np.max(fftZ))
    Z_normalized = norm(fftZ)
    fft_image = plt.get_cmap('viridis')(fftZ)
    fft_image[..., 3] = alpha_mask  # Set alpha channel


    plt.imsave("fft_"+filename, fft_image, cmap='viridis', origin='lower')
    plt.imsave(filename, colored_image, cmap='viridis', origin='lower')

def f(x,y):
    return np.exp(-((x-y)*5)**6) * np.cos(np.pi/6 * (x-y)) + \
        np.exp(-((x-y-0.8)*5)**6) * np.cos(np.pi/6 * (x-y)) * (1-np.exp(-((x+y)*3)**2)/10)
        # np.exp(-(x-y + 1)**4) * np.cos(np.pi/9 * (x-y - 1)) + \
        # np.exp(-(x-y + 1)**2) * np.cos(np.pi/3 * (x-y + 1))

class FourierRotation(Slide):
    def construct(self):
        x_range = [-3, 3, 1]
        title = MathTex(formula['lattice_function']).to_edge(UP)
        self.add(title)

        t = Text("Hypotheses").scale(0.5).to_edge(UP).to_edge(LEFT).shift(DOWN)
        hyp = MathTex(formula['tau']).next_to(t, DOWN, buff=0.2)

        self.next_slide()
        self.play(Write(t), Write(hyp))
        axis = NumberLine(
            x_range=x_range,
        ).shift(DOWN*2.1)
        # Create a 2D coordinate system
        axes = Axes(
            x_range=x_range,
            x_length=axis.length,
            y_length=axis.length,
            y_range=x_range,
            axis_config={"include_tip": True, "tip_length": 0.2},  # Add arrowheads to the axes
            # background_line_style={"stroke_color": BLUE, "stroke_width": 1, "stroke_opacity": 0.5}
        ).shift(DOWN*0.8)

        x_label = MathTex("R_1").next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
        y_label = MathTex("R_2").next_to(axes.y_axis.get_end(), RIGHT, buff=0.2)

        three_dots_left = VGroup(
            Dot(axis.n2p(x_range[0] - 0.3), color=GRAY, radius=0.03),
            Dot(axis.n2p(x_range[0] - 0.2), color=GRAY, radius=0.03),
            Dot(axis.n2p(x_range[0] - 0.1), color=GRAY, radius=0.03)
        )

        atoms = VGroup()
        xatoms = VGroup()
        yatoms = VGroup()
        for i in range(x_range[0]+1, x_range[1]):
            atoms.add(Dot(axis.n2p(i), color=RED, radius=0.1))
            xatoms.add(Dot(axes.c2p(i, 0), color=RED, radius=0.1))
            yatoms.add(Dot(axes.c2p(0, i), color=RED, radius=0.1))

        three_dots_right = VGroup(
            Dot(axis.n2p(x_range[1] + 0.1), color=GRAY, radius=0.03),
            Dot(axis.n2p(x_range[1] + 0.2), color=GRAY, radius=0.03),
            Dot(axis.n2p(x_range[1] + 0.3), color=GRAY, radius=0.03),
        )

        self.play(Create(axis))
        self.play(FadeIn(three_dots_left), FadeIn(atoms), FadeIn(three_dots_right))
        self.next_slide()

         # Animate the creation of the dots
        self.play(ReplacementTransform(axis,axes),
                  ReplacementTransform(atoms, xatoms),
                  FadeOut(three_dots_left),
                  FadeOut(three_dots_right))  # Animate the creation of the axes
        self.play(Create(x_label), Create(y_label))
        self.play(FadeIn(yatoms))
        self.next_slide()

        self.play(FadeOut(xatoms), FadeOut(yatoms))
        self.next_slide()

        # Create a 3x3 grid of points
        # grid_points = VGroup()
        labels = VGroup()
        for i in range(3):  # x-coordinates: 0, 1, 2
            # Create a point at (i, j)
            # point = Dot(axes.c2p(i, j), color=RED)  # Convert (i, j) to scene coordinates
            # grid_points.add(point)

            # Add a label (e.g., function value) on top of the point
            value = round(f(i,0), 1)  # Example function: f(x, y) = x + y
            label = MathTex(f"{value:.1f}").scale(0.5).next_to(axes.c2p(i, 0), UP+RIGHT, buff=0.1)
            labels.add(label)

        translation = Arrow(
            start=axes.c2p(2, 2),
            end=axes.c2p(3, 3),
            color=YELLOW,
            buff=0.2
        )

        translation_label = MathTex(r"(R,R)", color=YELLOW).scale(0.5
        ).next_to(translation, LEFT+UP, buff=0).rotate(PI/4).shift((RIGHT+DOWN)*0.4)

        # # Add the points and labels to the scene
        # self.play(FadeIn(grid_points))

        self.play(Create(translation), Create(translation_label))  # Animate the creation of the arrow
        self.play(FadeIn(labels))
        self.next_slide()
        self.play(FadeOut(translation_label))

        dots = VGroup()
        for i in range(3):
            value = float(labels[i].get_tex_string())  # Get the value from the label
            for j in range(1,3-i):
                # color = RED if value > 0 else BLUE
                self.play(translation.animate.move_to(axes.c2p(i+j-0.3, j-0.3)))
                # self.play(FadeIn(dots[-1]))
                dots.add(Dot(axes.c2p(i+j, j), color=WHITE, radius=0.02))
                label = MathTex(f"{value}").scale(0.5).next_to(axes.c2p(i+j, j), UP+RIGHT, buff=0.1)
                labels.add(label)
                self.play(FadeIn(label), FadeIn(dots[-1]), run_time=0.5)  # Transform the label to the new position
                self.next_slide()


        self.play(FadeOut(translation))
        self.play(FadeOut(labels), FadeOut(dots))

        if not os.path.exists("fc.png") or FAST is False:
            construct_imshow("fc.png", function=f, extent=[-3, 3, -3, 3], n_pixels=800)

        imshow = ImageMobject("fc.png").move_to(axes).scale_to_fit_width(axes.width)
        self.play(FadeIn(imshow))
        self.next_slide()

        s2 = 1/np.sqrt(2) * x_range[1]
        new_x = axes.c2p(s2, -s2)
        new_y = axes.c2p(s2, s2)
        new_x_label = MathTex("R_1 - R_2").next_to(new_x, RIGHT, buff=0.2)
        new_y_label = MathTex("R_1 + R_2").next_to(new_y, RIGHT, buff=0.2)

        kwargs = {
            "color": WHITE,
            "stroke_width": axes.stroke_width,
            "stroke_opacity": 0.5
        }
        line_angle = Line(axes.c2p(0, 0), axes.c2p(0, 1), **kwargs)
        angle = Arc(
            radius=0.8,
            arc_center=axes.c2p(0, 0),
            start_angle=PI/4,
            angle=PI/4,
            **kwargs
        )
        angle.points = angle.points[::-1]
        angle_label = MathTex(r"\pi/4").scale(0.5).next_to(angle, UP+RIGHT*0.2, buff=0.1)

        self.add(line_angle)
        self.play(
            Create(angle),
            Write(angle_label),
            axes.animate.rotate(-PI/4),
            ReplacementTransform(x_label, new_x_label),
            ReplacementTransform(y_label, new_y_label),
        )
        self.next_slide()


        new_fc = MathTex(r"f'(R_1-R_2, R_1+R_2) = f'(R_1-R_2)").to_edge(UP)
        self.play(ReplacementTransform(title, new_fc))
        self.next_slide()


        self.play(
            FadeOut(angle),
            FadeOut(angle_label),
            FadeOut(line_angle),
            FadeOut(hyp),
        )
        real_axis = Group(axes, new_x_label, new_y_label, imshow)
        self.play(
            real_axis.animate.scale(0.5).to_edge(RIGHT)
        )

        qaxes = axes.copy().to_edge(LEFT)
        qimshow = ImageMobject("fft_fc.png").move_to(qaxes).scale_to_fit_width(qaxes.width * np.sqrt(2))
        qx_label = MathTex("q_1 - q_2").scale(0.5).next_to(qaxes.x_axis.get_end(), RIGHT, buff=0.2)
        qy_label = MathTex("q_1 + q_2").scale(0.5).next_to(qaxes.y_axis.get_end(), RIGHT, buff=0.2)
        self.play(FadeIn(qaxes), FadeIn(qx_label), FadeIn(qy_label))

        arrow = DoubleArrow(
            start=axes.get_edge_center(LEFT),
            end=qaxes.get_edge_center(RIGHT),
            color=YELLOW,
            buff=1,
        )
        arrow_label = Text("Fourier Transform", color=YELLOW).scale(0.5).next_to(arrow, UP, buff=0.2)
        self.play(Create(arrow), Write(arrow_label), FadeIn(qimshow))
        self.next_slide()


        hyp1 = Tex(r"$\bullet$ Rotations conserve integration volume: $d(U q_1) d(U q_2) = dq_1 dq_2$").scale(0.6).next_to(new_fc, DOWN, buff=0.4).to_edge(LEFT)
        hyp2 = Tex(r"$\bullet$ Scalar product is rotationally invariant: $e^{i Uq \cdot UR} = e^{i q \cdot R}$").scale(0.6).next_to(hyp1, DOWN, buff=0.2).to_edge(LEFT)
        self.play(Unwrite(t))
        self.play(Write(hyp1), Write(hyp2))
        all = Group(qaxes, qimshow, qx_label, qy_label, arrow, arrow_label)
        self.next_slide()
        self.play(FadeOut(real_axis), FadeOut(all))
        self.next_slide()


class Tree(Slide):
    def construct(self):
        scale = 0.7
        buff = 3
        new_fc = MathTex(r"f'(R_1-R_2, R_1+R_2) = f'(R_1-R_2)").to_edge(UP)
        hyp1 = Tex(r"$\bullet$ Rotations conserve integration volume: $d(U q_1) d(U q_2) = dq_1 dq_2$").scale(0.6).next_to(new_fc, DOWN, buff=0.4).to_edge(LEFT)
        hyp2 = Tex(r"$\bullet$ Scalar product is rotationally invariant: $e^{i Uq \cdot UR} = e^{i q \cdot R}$").scale(0.6).next_to(hyp1, DOWN, buff=0.2).to_edge(LEFT)
        hyp3 = Tex(r"$\bullet$ $f'$ is constant on the second coordinate", color=BLUE).scale(0.6).next_to(hyp2, DOWN, buff=0.2).to_edge(LEFT)

        f1 = MathTex(r"f(R_1, R_2)").scale(scale).to_edge(LEFT,  buff=buff).shift(UP*0.6)
        f2 = MathTex(r"f'(R_1-R_2, R_1+R_2)").scale(scale).next_to(f1, 0).shift(DOWN*3)
        f3 = MathTex(r"D(q_1, q_2)").scale(scale).to_edge(RIGHT, buff=buff).shift(UP*0.6)
        f4 = MathTex(r"D'(q_1-q_2, q_1+q_2)").scale(scale).next_to(f3, 0).shift(DOWN*3)

        f12 = Arrow(
            start=f1.get_bottom(),
            end=f2.get_top(),
            color=WHITE,
            buff=0.3
        )
        label12 = MathTex(r"U", color=WHITE).next_to(f12, LEFT, buff=0.2)
        f12 = VGroup(f12, label12)

        f34 = Arrow(
            start=f3.get_bottom(),
            end=f4.get_top(),
            color=WHITE,
            buff=0.3
        )
        label34 = MathTex(r"U", color=WHITE).next_to(f34, RIGHT, buff=0.2)
        f34 = VGroup(f34, label34)

        f13 = Arrow(
            start=f1.get_right(),
            end=f3.get_left(),
            color=WHITE,
            buff=0.3
        )
        label13 = MathTex(r"FT", color=WHITE).next_to(f13, UP, buff=0.2)
        f13 = VGroup(f13, label13)

        f24 = Arrow(
            start=f2.get_right(),
            end=f4.get_left(),
            color=YELLOW,
            stroke_width=20,
            buff=0.3
        )
        label24 = MathTex(r"FT", color=YELLOW).next_to(f24, UP, buff=0.2)
        f24 = VGroup(f24, label24)
        self.next_slide()

        self.add(new_fc)
        self.add(hyp1, hyp2)
        # self.play(Write(hyp1), Write(hyp2))
        self.next_slide()
        self.play(Write(f1), Write(f3))
        self.play(Create(f13))
        self.next_slide()

        self.play(Write(f2), Write(f4), Create(f12), Create(f34))
        self.next_slide()

        self.play(Create(f24), hyp1.animate.set(color=YELLOW), hyp2.animate.set(color=YELLOW))
        self.next_slide()

        self.play(FadeOut(f1), FadeOut(f3),
                  FadeOut(f12), FadeOut(f13), FadeOut(f34),
                  f2.animate.move_to(f1), f24.animate.move_to(f13), f4.animate.move_to(f3))
        self.next_slide()

        self.play(Write(hyp3))
        dyn = MathTex(r" D'(q_1 - q_2, q_1 + q_2) = D'(q_1 - q_2) {{ \delta_{q_1 + q_2,0} }}"
            ).to_edge(DOWN)
        dyn[1].set(color=BLUE)
        self.play(Write(dyn))
        self.next_slide()

        final = Tex(r"Dynamical matrix $D(q, q') = D(q, -q)$ {{$\delta_{q',-q}$}}"
            ).to_edge(DOWN)
        final[1].set(color=BLUE)
        self.play(ReplacementTransform(dyn, final))
        self.next_slide()

        hyp4 = Tex(r"$\bullet$ $f$ is constant in a direction $\rightarrow$ it is diagonal in the $q$-basis"
                   ).scale(0.6).next_to(new_fc, DOWN).to_edge(LEFT).set(color=BLUE)
        self.play(final.animate.to_edge(UP),
            new_fc.animate.shift(UP*2),
            FadeOut(f24), FadeOut(f2), FadeOut(f4), FadeOut(hyp1),
            FadeOut(hyp2), Transform(hyp3, hyp4))
        self.next_slide()
