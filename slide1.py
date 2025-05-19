from manim import *
from random import random
from numpy import sign
from manim_slides import Slide

SCALE = 2
SIZE_SI = 0.2
MAX_LEN = 4

formula = {
     'force constants':  r"    F \begin{pmatrix} R_1 & R_2 \\ \tau_1 & \tau_2 \\ \alpha_1  & \alpha_2 \end{pmatrix} = \frac{\partial^2 E}{\partial u(R_1, \tau_1, \alpha_1) \ \partial u(R_1, \tau_2, \alpha_2)}",
     'force constants1': r"    F \begin{pmatrix} R_1 & R_2 \\ \tau_1 & \tau_2 \\ 1  & 1 \end{pmatrix} = \frac{\partial^2 E}{\partial u(R_1, \tau_1, 1) \ \partial u(R_2, \tau_2, 1)}",
     'lattice_matrix': r"F \begin{pmatrix} R_1 & R_2 \\ \tau_1 & \tau_2 \\ \alpha_1  & \alpha_2  \end{pmatrix} = F \begin{pmatrix} R_1+R & R_2 +R \\ \tau_1 & \tau_2 \\ \alpha_1  & \alpha_2 \end{pmatrix}",
     'lattice_function': r"f(R_1, R_2) = f(R_1 + R, R_2+R)",
}

class Lattice1D(Slide):
    def construct(self):
        lim = 5
        indices_fc = [6,15]

        title = Tex("Force contants and lattice translations").to_edge(UP)

        axes = NumberLine(
            x_range=[-lim, lim, 1],  # x-axis range: from -1 to 4 with step size 1
            # background_line_style={"stroke_color": BLUE, "stroke_width": 1, "stroke_opacity": 0.5}
        ).shift(DOWN * 0.5)

        origin_label = MathTex("0").scale(0.7).next_to(axes.n2p(0), DOWN, buff=0.2)
        origin_tick = Line(
            start=origin_label.get_center() + DOWN * 0.23,
            end=origin_label.get_center() + DOWN,
            color=WHITE,
            stroke_width=1.5,
            stroke_opacity=10,
        )

        # axes_origin = VGroup(axes, origin_label)

        three_dots_left = VGroup(
            Dot(axes.n2p(-lim - 0.3), color=GRAY, radius=0.03),
            Dot(axes.n2p(-lim - 0.2), color=GRAY, radius=0.03),
            Dot(axes.n2p(-lim - 0.1), color=GRAY, radius=0.03)
        )

        atoms = VGroup()
        for i in range(-lim, lim):
            at1 = Dot(axes.n2p(i+0.2), color=RED, radius=0.1)
            at2 = Dot(axes.n2p(i+0.6), color=BLUE, radius=0.2)
            atoms.add(at1, at2)
        atoms.set_z_index(1)
        three_dots_right = VGroup(
            Dot(axes.n2p(lim + 0.1), color=GRAY, radius=0.03),
            Dot(axes.n2p(lim + 0.2), color=GRAY, radius=0.03),
            Dot(axes.n2p(lim + 0.3), color=GRAY, radius=0.03),
        )

        force_constants = MathTex(formula['force constants']
                            ).scale(0.5).move_to(UP)
        force_constants1 = MathTex(formula['force constants1']
                            ).scale(0.5).move_to(UP)

        selected_atoms = VGroup([atoms[i].copy() for i in indices_fc])

        selected_arrows = VGroup(
            [Arrow(
                start=axes.n2p(0),
                end=a.get_center() + LEFT * a.radius * sign(a.get_center()[0]),
                color=GREEN,
                buff=0
            ).shift(DOWN) for a in selected_atoms])

        selected_arrows_lab = VGroup(
            [MathTex(rf"R_{i+1} + \tau_{i+1}").scale(0.5).next_to(a, DOWN, buff=0.1).shift(DOWN)
                for i,a in enumerate(selected_atoms)])

        selected_arrows_lab_after = VGroup(
            [MathTex(rf"R_{i+1} + \tau_{i+1}" + r"{{+ R}}").scale(0.5).next_to(a, DOWN, buff=0.1).shift(DOWN)
                for i,a in enumerate(selected_atoms)])
        selected_arrows_lab_after[0][1].set(color=YELLOW)
        selected_arrows_lab_after[1][1].set(color=YELLOW)

        # selected_atoms_lab = VGroup(
        #     [MathTex(rf"\alpha_{i+1} = 1").scale(0.5).next_to(a, DOWN, buff=0.1)
        #         for i,a in enumerate(selected_atoms)])

        translation_arrow = Arrow(
            start=axes.n2p(-lim - 0.6),
            end=axes.n2p(-lim - 1.6),
            color=YELLOW,
            buff=0
        )

        translations = VGroup(
            translation_arrow.copy().shift(UP*0.3),
            translation_arrow.copy(),
            translation_arrow.copy().shift(DOWN*0.3),
        )

        translations_lab = VGroup(
            MathTex(r"R", color=YELLOW).next_to(translations[0], UP, buff=0.1),
        )

        # self.play(FadeIn(left_points))
        self.add(title)
        self.add(axes, three_dots_left, three_dots_right, atoms)
        # self.play(AnimationGroup(*[
        #     FadeIn(dot) for dot in three_dots_left], lag_ratio=0.1, run_time=0.5))
        # self.play(AnimationGroup(*[
        #     FadeIn(atom) for atom in atoms], lag_ratio=0.1))
        # self.play(AnimationGroup(*[
        #     FadeIn(dot) for dot in three_dots_right], lag_ratio=0.1, run_time=0.5))

        self.play(FadeIn(origin_label))
        self.play(FadeIn(force_constants))
        self.next_slide()
        self.play(Transform(force_constants, force_constants1))
        self.next_slide()

        self.play([a.animate.shift(DOWN) for a in selected_atoms])
        # self.play([FadeIn(a) for a in selected_atoms_lab])
        self.play(FadeIn(origin_tick), [FadeIn(a) for a in selected_arrows])
        self.play([FadeIn(a) for a in selected_arrows_lab])
        self.next_slide()

        axes_red = NumberLine(x_range=[0,1,1], length=2).move_to(LEFT * 5 + UP * 2)
        axes_blue = axes_red.copy().shift(DOWN)
        red = Dot(axes_red.n2p(0.2), color=RED, radius=0.2)
        blue = Dot(axes_blue.n2p(0.6), color=BLUE, radius=0.4)
        # arr_red = Arrow(start=axes_red.n2p(0), end=red.get_center() + red.radius*LEFT, color=RED, buff=0)
        # arr_blue = Arrow(start=axes_blue.n2p(0), end=blue.get_center() + blue.radius*LEFT, color=BLUE, buff=0)
        red_lab = MathTex(r"\tau_1").next_to(red, UP, buff=0.1).set_color(RED)
        blue_lab = MathTex(r"\tau_2").next_to(blue, UP, buff=0.1).set_color(BLUE)
        self.play(FadeIn(axes_red), FadeIn(axes_blue))
        self.play(FadeIn(red), FadeIn(blue))
        # self.play(Create(arr_red), Create(arr_blue))
        self.play(Write(red_lab), Write(blue_lab))
        self.next_slide()
        self.play(FadeOut(axes_red), FadeOut(axes_blue),
                  FadeOut(red), FadeOut(blue),
                  FadeOut(red_lab), FadeOut(blue_lab))

        self.play(FadeIn(translations), FadeIn(translations_lab))
        self.next_slide()

        self.play(three_dots_left.animate.shift(LEFT),
                    origin_label.animate.shift(LEFT),
                    axes.animate.shift(LEFT),
                    origin_tick.animate.shift(LEFT),
                    atoms.animate.shift(LEFT),
                    three_dots_right.animate.shift(LEFT),
                    FadeOut(translations),
                    FadeOut(translations_lab),
                    *[Transform(a,b) for a,b in
                      zip(selected_arrows_lab, selected_arrows_lab_after)],
        )
        self.next_slide()

        self.play([a.animate.shift(UP) for a in selected_atoms],
                  FadeOut(selected_arrows),
                  FadeOut(selected_arrows_lab),
                  FadeOut(origin_tick)
        )
        self.next_slide()

        # self.play(*[FadeOut(t) for t in translations],
        #           *[atoms[i].animate.shift(UP) for i in indices_fc])

        lattice_matrix = MathTex(formula['lattice_matrix']
                            ).scale(0.7).to_edge(DOWN)
        lattice_function = MathTex(formula['lattice_function']
                            ).to_edge(DOWN)
        self.play(Write(lattice_matrix))
        self.next_slide()

        self.play(ReplacementTransform(lattice_matrix, lattice_function))

        self.next_slide()
        self.play(FadeOut(force_constants),
                  FadeOut(three_dots_left),
                  FadeOut(three_dots_right),
                  FadeOut(atoms),
                  FadeOut(origin_label),
                  FadeOut(axes),
                  FadeOut(selected_atoms)
        )
        self.play(lattice_function.animate.to_edge(UP),
                  title.animate.shift(2*UP),
        )



class Lattice(Scene):
    def construct(self):
        # Create a lattice of squares
        e1 = SCALE * RIGHT
        e2 = SCALE * UP
        arrow_e1 = Arrow(start=ORIGIN, end=e1, buff=SIZE_SI)
        arrow_e2 = Arrow(start=ORIGIN, end=e2, buff=SIZE_SI)

        label_e1 = MathTex(r"\vec{e}_1").next_to(arrow_e1, DOWN)
        label_e2 = MathTex(r"\vec{e}_2").next_to(arrow_e2, LEFT)
        lattice_vecs = VGroup(arrow_e1, arrow_e2, label_e1, label_e2)

        labels = VGroup()  # create a group to hold the labels
        circle = Dot(radius=SIZE_SI)  # create a circle
        circle.set_color(RED)
        atom2 = (e1 + e2) / 4
        circles = VGroup()  # create a group to hold the circles
        tot = 0
        grid = VGroup()
        for i in range(-3,4):
            grid.add(DashedLine(
                start=e1 * i - MAX_LEN * e2,
                end=e1 * i + MAX_LEN * e2,
                color=WHITE))
            for j in range(-2, 3):
                if i == 0:
                    grid.add(DashedLine(
                        start=e2 * j - MAX_LEN * e1,
                        end=e2 * j + MAX_LEN * e1,
                        color=WHITE))

                circle1 = circle.copy().move_to(e1 * i + e2 * j)
                circle2 = circle.copy().move_to(e1 * i + e2 * j + atom2)
                circles.add(circle1, circle2)


                label1 = Text(f"{tot}").scale(0.3).next_to(circle1, UP, buff=0.1)
                label2 = Text(f"{tot+1}").scale(0.3).next_to(circle2, UP, buff=0.1)
                labels.add(label1, label2)

                tot += 2

        self.play(FadeIn(grid))
        self.play(FadeIn(circles))
        self.play(FadeIn(lattice_vecs))


        # self.play(FadeIn(labels))
        atoms_ij = [12,27]
        index_ij = [r"\tau", r"\tau'"]
        self.play([circles[i].animate.set_color(BLUE) for i in atoms_ij])
        self.play([FadeIn(MathTex(index_ij[i], color=BLUE).scale(0.5).next_to(circles[index], UP, buff=0.1)) for i,index in enumerate(atoms_ij)])

        arrow_e1 = Arrow(start=ORIGIN, end=e2-e1 + atom2, buff=SIZE_SI)
        label_e1 = MathTex(r"\vec{R} + \vec{\tau}").rotate(arrow_e1.get_angle()).next_to(arrow_e1, RIGHT*0.2)
        arrow_e2 = Arrow(start=ORIGIN, end=-2*e1-e2, buff=SIZE_SI)
        label_e2 = MathTex(r"\vec{R'}").rotate(arrow_e2.get_angle()).next_to(arrow_e2, RIGHT)
        lattice_vecs_after = VGroup(arrow_e1, arrow_e2, label_e1, label_e2)
        self.play(Transform(lattice_vecs, lattice_vecs_after))

        arrows = VGroup()
        for i in atoms_ij:
            arrow = Arrow(
                start=circles[i].get_center(),
                end=circles[i].get_center() + RIGHT,
                color=GREEN,
                buff=SIZE_SI
            )
            # label = MathTex(rf"\alpha{"'" if i is 1 else ""} = 1").next_to(arrow, UP, buff=0.1)
            arrows.add(arrow)

        self.play(FadeIn(arrows))

        # Wait for a moment to show the lattice
        self.wait(2)


class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.1)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen

class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set color and transparency

        square = Square()  # create a square
        square.rotate(PI / 4)  # rotate a certain amount

        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, circle))  # interpolate the square into the circle
        self.play(FadeOut(square))  # fade out animation

class SquareAndCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency

        square = Square()  # create a square
        square.set_fill(BLUE, opacity=0.5)  # set the color and transparency

        square.next_to(circle, RIGHT, buff=0.5)  # set the position
        self.play(Create(circle), Create(square))  # show the shapes on screen

class DifferentRotations(Scene):
    def construct(self):
        left_square = Square(color=BLUE, fill_opacity=0.7).shift(2 * LEFT)
        right_square = Square(color=GREEN, fill_opacity=0.7).shift(2 * RIGHT)
        self.play(left_square.animate.rotate(PI), run_time=2)
        self.play(Rotate(right_square, angle=PI), run_time=2)
        self.wait()

class TwoTransforms(Scene):
    def transform(self):
        a = Circle()
        b = Square()
        c = Triangle()
        self.play(Transform(a, b))
        self.play(Transform(a, c))
        self.play(FadeOut(a))

    def replacement_transform(self):
        a = Circle()
        b = Square()
        c = Triangle()
        self.play(ReplacementTransform(a, b))
        self.play(ReplacementTransform(b, c))
        self.play(FadeOut(c))

    def construct(self):
        self.transform()
        self.wait(0.5)  # wait for 0.5 seconds
        self.replacement_transform()

class ExampleRotation(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        m1a = Square().set_color(RED).shift(LEFT)
        m1b = Circle().set_color(RED).shift(LEFT)
        m2a = Square().set_color(BLUE).shift(RIGHT)
        m2b = Circle().set_color(BLUE).shift(RIGHT)

        # points = m2a.points
        # points = np.roll(points, int(len(points)/4), axis=0)
        # m2a.points = points

        self.play(Transform(m1a,m1b),Transform(m2a,m2b), run_time=1)