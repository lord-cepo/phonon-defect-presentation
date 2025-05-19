from manim import *
from manim_slides import Slide

physics = TexTemplate()
physics.add_to_preamble(r"\usepackage{physics}")

class DynamicalMatrix(Slide):
    def construct(self):
        title = Tex(r"Dynamical matrix $D(q, q') = D(q, -q)$ {{$\delta_{q',-q}$}}"
            ).to_edge(UP)
        title[1].set_color(BLUE)

        hyp1 = Tex(r"$\bullet$ $f$ is constant in a direction $\rightarrow$ it is diagonal in the $q$-basis"
            ).scale(0.6).next_to(title, DOWN).to_edge(LEFT).set(color=BLUE)
        # Define the size of the matrix
        n = 4

        # Create the matrix data (all zeros)
        matrix_data = [["0"] * n for _ in range(n)]
        for i in range(n-2):
            matrix_data[i][i] = rf"\omega^{2}_{i+1}"
        matrix_data[n-2][n-2] = r"..."
        matrix_data[n-1][n-1] = r"\omega^{2}_{N}"

        # Create row and column labels
        row_labels = VGroup([MathTex(f" q_{i+1}") for i in range(n)])
        col_labels = VGroup([MathTex(f"-q_{i+1}") for i in range(n)])
        row_labels[-2] = MathTex(r"...")
        col_labels[-2] = MathTex(r"...")
        row_labels[-1] = MathTex(r"q_{N}")
        col_labels[-1] = MathTex(r"-q_{N}")
        row_labels.scale(0.7)
        col_labels.scale(0.7)

        # Create the MathTable
        matrix = Matrix(matrix_data)
        matrix.shift(DOWN)

        first_col = matrix.get_columns()[0]
        x = matrix.get_left()[0] - 0.5
        first_row = matrix.get_rows()[0]
        y = matrix.get_top()[1] + 0.5
        for i, label in enumerate(row_labels):
            label.move_to((x, first_col[i].get_center()[1], 0))

        for i, label in enumerate(col_labels):
            label.move_to((first_row[i].get_center()[0], y, 0))

        # Center the table
        self.next_slide()

        self.add(title)
        self.add(hyp1)
        # Add everything to the scene
        self.play(FadeIn(matrix), Write(row_labels), Write(col_labels))
        self.next_slide()

        matrix_data = [[VMobject() for _ in range(n)] for _ in range(n)]
        s = Square(side_length=matrix.width/n, color=YELLOW, fill_opacity=0.5)
        for i in range(n):
            if i == n-2:
                matrix_data[i][i] = VGroup(VMobject(), Tex(r"..."))
            elif i == n-1:
                matrix_data[i][i] = VGroup(s.copy(), MathTex(f"q_N"))
            else:
                matrix_data[i][i] = VGroup(s.copy(), MathTex(f"q_{i+1}"))

        block_diag = MobjectMatrix(matrix_data, v_buff=matrix.width/n)
        position = (block_diag.get_rows()[-3][-3].get_center() + \
            block_diag.get_rows()[-1][-1].get_center())/2

        block_diag.get_rows()[-2][-2].move_to(position)

        block_diag.scale(0.7).shift(DOWN)
        self.play(FadeOut(col_labels), FadeOut(row_labels))

        hyp2 = Tex(r"$\bullet$ $\alpha$ and $\tau \neq 1$ $\rightarrow$ adding $3N_{at}$ d.o.f. $\rightarrow$ $N$ block-diagonal $3 N_{at}\times 3 N_{at}$ matrices"
        ).scale(0.6).next_to(hyp1, DOWN).to_edge(LEFT)#.set(color=BLUE)
        self.play(Write(hyp2))
        self.next_slide()
        self.play(ReplacementTransform(matrix, block_diag))
        self.next_slide()

        diag_label = MathTex(r"D(q, -q) \ket{qs} = \omega^2_{qs} \ket{qs}",
            tex_template=physics).scale(0.6).next_to(block_diag.get_rows()[0][0], RIGHT).to_edge(RIGHT)

        next_label = VGroup(
            Tex(r"like time independent"),
            Tex(r"Schrodinger equation of"),
            MathTex(r"\partial^2 / \partial t^2 \ket{qs} = D(q,-q) \ket{qs}", tex_template=physics)
        ).scale(0.6
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.2
        ).next_to(diag_label, DOWN, buff=0.2, aligned_edge=RIGHT)


        arrow = Arrow(
            start=block_diag.get_rows()[0][0].get_right(),
            end= diag_label.get_left(),
            color=YELLOW,
            buff=0.5
        )
        self.play(Create(arrow), Write(diag_label))
        self.play(Write(next_label))
        self.next_slide()


        title_out = Tex(r"What about defects?").to_edge(DOWN)
        self.play(Write(title_out))
        self.next_slide()

        g = VGroup(diag_label, arrow, hyp1, hyp2)
        self.play(
            FadeOut(g),
            FadeOut(next_label),
            title_out.animate.to_edge(UP),
            title.animate.shift(UP*2)
        )
        self.next_slide()


class DefectMatrix(Slide):
    def construct(self):
        title = Tex(r"What about defects?").to_edge(UP)
        n = 4

        hyps = VGroup(
            Tex(r"$\bullet$ A single defect disrupts the periodicity of the lattice"),
            Tex(r"$\bullet$ if defect SC has same periodicity as force constants $\rightarrow$ all off-diagonal blocks available"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2
        ).scale(0.6).next_to(title, DOWN).to_edge(LEFT)
        matrix_data = [[VMobject() for _ in range(n)] for _ in range(n)]
        s = Square(side_length=1.30745115, color=YELLOW, fill_opacity=0.5)
        for i in range(n):
            if i == n-2:
                matrix_data[i][i] = VGroup(VMobject(), Tex(r"..."))
            elif i == n-1:
                matrix_data[i][i] = VGroup(s.copy(), MathTex(f"q_N"))
            else:
                matrix_data[i][i] = VGroup(s.copy(), MathTex(f"q_{i+1}"))

        block_diag = MobjectMatrix(matrix_data, v_buff=1.30745115)
        position = (block_diag.get_rows()[-3][-3].get_center() + \
            block_diag.get_rows()[-1][-1].get_center())/2

        block_diag.get_rows()[-2][-2].move_to(position)
        block_diag.scale(0.7).shift(DOWN)

        self.add(title)
        self.add(block_diag)

        first_square = block_diag.get_rows()[0][0]
        s = Square(side_length=first_square.width, color=ORANGE, fill_opacity=0.5)
        s.next_to(first_square, RIGHT, buff=0)

        label_s = VGroup(
            MathTex(r"q_1"),
            MathTex(r"-q_2"),
        ).arrange(DOWN, buff=0.2
        ).scale(0.7
        ).move_to(s.get_center())
        s = VGroup(s, label_s)


        self.next_slide()

        self.play(Write(hyps[0]))
        self.play(Create(s))
        self.next_slide()
        self.play(Write(hyps[1]))
        self.next_slide()

        new_eq = MathTex(r"D(q_1, -q_2) \ket{q_2} \sim \ket{q_1}",
            tex_template=physics
            ).scale(0.6).next_to(first_square, RIGHT).to_edge(RIGHT)

        arrow = Arrow(
            start=s.get_right(),
            end=new_eq.get_left(),
            color=ORANGE,
            buff=0.5
        )

        new_eq = VGroup(new_eq, arrow)
        self.play(Write(new_eq))
        self.next_slide()


        title_out = Tex(r"Perturbation theory").to_edge(DOWN)
        self.play(Write(title_out))
        self.next_slide()

        self.play(
            FadeOut(hyps),
            FadeOut(new_eq),
            title_out.animate.to_edge(UP),
            title.animate.shift(UP*2),
            FadeOut(s),
            FadeOut(block_diag),
        )

        self.next_slide()


def sin_func(t):
    return np.array([t, 0.1*np.sin(10*t), 0])


class PerturbationTheory(Slide):
    def construct(self):
        title = Tex(r"Perturbation theory").to_edge(UP)
        self.add(title)

        hyps = VGroup(
            MathTex(r"\ \bullet D({{q}}, -{{q'}}) := D^{(0)}({{q}}, -{{q}}) + V({{q}}, -{{q'}}),\ E := \omega^2"),
            Tex(r"$\bullet$ real part of energy gives an \textbf{energy shift}"),
            Tex(r"$\bullet$ imaginary part of energy gives a \textbf{decay rate}"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2
        ).scale(0.6).next_to(title, DOWN).to_edge(LEFT)
        hyps[0][1].set_color(RED)
        hyps[0][3].set_color(BLUE)
        hyps[0][5].set_color(RED)
        hyps[0][7].set_color(RED)
        hyps[0][9].set_color(RED)
        hyps[0][11].set_color(BLUE)

        self.next_slide()
        for hyp in hyps:
            self.play(Write(hyp))
            self.next_slide()

        subtitle = Tex(r"1st order").next_to(hyps, DOWN)

        eq = MathTex(r"E_{qs}^{(1)} = \bra{qs} {{V(q, -q)}} \ket{qs} \textit{is real, why?}",
            tex_template=physics
            ).scale(0.6).next_to(subtitle, DOWN).to_edge(LEFT)
        self.play(Write(subtitle))
        self.play(Write(eq))
        self.next_slide()

        subtitle2 = Tex(r"2nd order").next_to(eq, DOWN).align_to(subtitle, LEFT)

        eq2 = VGroup(MathTex(r"E_{qs}^{(2)} = \bra{qs}  \sum_{q's'} \left[ {{V(q, -q')}} {{ G(E_{qs}^{(0)} , q's') }} {{V(q', -q)}} \right] \ket{qs}",
            tex_template=physics),
            MathTex(r"{{G(E_{qs}^{(0)}, q's')}} := \frac{\ket{q's'}\bra{q's'}}{E_{qs}^{(0)} - E_{q's}^{(0)}}", tex_template=physics)
        ).scale(0.6
        ).arrange(DOWN, aligned_edge=LEFT
        ).next_to(subtitle2, DOWN
        ).to_edge(LEFT)
        # eq2[1][0].set_color(YELLOW)

        self.play(Write(subtitle2))
        self.play(Write(eq2))
        self.next_slide()

        subtitle3 = Tex(r"$n$th order").next_to(eq2, DOWN).align_to(subtitle, LEFT)

        eq3 = MathTex(r"E_{qs}^{(n)} = \bra{qs} \sum {{V}} {{G}} {{V}} {{G}} ... {{V}} \ket{qs}",
            tex_template=physics
            ).scale(0.6).next_to(subtitle3, DOWN).to_edge(LEFT)

        self.play(Write(subtitle3))
        self.play(Write(eq3))
        self.next_slide()

        self.play(
            eq[1].animate.set(color=ORANGE),
            eq2[0][1].animate.set(color=ORANGE),
            eq2[0][3].animate.set(color=YELLOW),
            eq2[0][5].animate.set(color=ORANGE),
            eq2[1][0].animate.set(color=YELLOW),
            eq3[1].animate.set(color=ORANGE),
            eq3[3].animate.set(color=YELLOW),
            eq3[5].animate.set(color=ORANGE),
            eq3[7].animate.set(color=YELLOW),
            eq3[9].animate.set(color=ORANGE)
        )
        self.next_slide()

        # line = Line(
        #     start=eq.get_right(),
        #     end=eq.get_right() + RIGHT*2,
        #     color=YELLOW,
        #     stroke_width=2,

        # ).to_edge(RIGHT, buff=0.5)

        wave = ParametricFunction(sin_func, t_range=[-np.pi/2, np.pi/2], dt=0.01
            ).scale(0.25
            )#.set(color=YELLOW)

        cross = Cross(color=ORANGE).scale(0.1)


        G1 = wave.copy()
        G2 = wave.copy().next_to(G1, RIGHT, buff=0)
        G3 = wave.copy().next_to(G2, RIGHT, buff=0)
        V1 = cross.copy().move_to(G1.get_right())
        V2 = cross.copy().move_to(G2.get_right())
        three_points = Tex(r"...").next_to(G3, RIGHT, buff=0.5)
        G4 = wave.copy().next_to(three_points, RIGHT, buff=0.5)
        V3 = cross.copy().move_to(G4.get_left())

        f1 = VGroup(G1.copy(), G2.copy(), V1.copy()).next_to(eq, RIGHT).to_edge(RIGHT, buff=1.5)

        f2 = VGroup(
            G1.copy(),
            G2.copy().set(color=YELLOW),
            G3.copy(),
            V1.copy(),
            V2.copy(),
        ).next_to(eq2, RIGHT).to_edge(RIGHT, buff=1.5)


        f3 = VGroup(
            G1.copy(),
            G2.copy().set(color=YELLOW),
            G3.copy().set(color=YELLOW),
            G4.copy(),
            V1.copy(),
            V2.copy(),
            V3.copy(),
            three_points,
        ).next_to(eq3, RIGHT).to_edge(RIGHT, buff=1.5)

        for f in [f1,f2,f3]:
            self.play(Create(f))
            self.next_slide()

        all_terms = VGroup(f1, f2, f3, subtitle2, subtitle3, eq2, eq3)

        shift = UP * (subtitle.get_center() - subtitle2.get_center())[1]
        self.play(all_terms.animate.shift(shift),
            subtitle.animate.shift(shift), eq.animate.shift(shift),
            FadeOut(eq), FadeOut(subtitle))

        subtitle4 = Tex(r"all orders").next_to(eq3, DOWN).align_to(subtitle, LEFT)
        self.play(Write(subtitle4))

        eq4 = MathTex(r"E_{qs} = \bra{qs} \sum (1 + VG + (VG)^2 + ...) V \ket{qs} = \bra{qs} (1-VG)^{-1} V \ket{qs}",
            tex_template=physics
            ).scale(0.6).next_to(subtitle4, DOWN).to_edge(LEFT)
        self.play(Write(eq4))
        self.next_slide()

        new_eq2 = VGroup(
            MathTex(r"E_{qs}^{(2)} = \sum_{q's'} \frac{|\bra{q's'} V (q', -q) \ket{qs}|^2}{E_{qs}^{(0)} - E_{q's}^{(0)}}", tex_template=physics),
            MathTex(r"\Gamma_{qs}^{(2)} = \Im{E_{qs}^{(2)}} = \sum_{q's'} |\bra{q's'} V (q', -q) \ket{qs}|^2 \delta(E_{qs}^{(0)} - E_{q's}^{(0)})", tex_template=physics)
            ).scale(0.6
            ).arrange(DOWN, aligned_edge=LEFT
            ).next_to(subtitle2, DOWN
            ).to_edge(LEFT)
        self.play(Transform(eq2, new_eq2))
        self.next_slide()

        title_out = Tex(r"Practical implementation").to_edge(UP)
        self.play(FadeOut(all_terms), FadeOut(subtitle4), FadeOut(eq4), FadeOut(hyps), ReplacementTransform(title, title_out))
        self.next_slide()

