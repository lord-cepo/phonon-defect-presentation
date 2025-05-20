from manim_slides import Slide
from manim import *

amsmath = TexTemplate()
amsmath.add_to_preamble(r"\usepackage{amsmath}")

class Introduction(Slide):
    def construct(self):
        # Step 1: Display the question
        question = Text("Scattering of phonon-defect").to_edge(UP)
        self.play(Write(question))

        # Step 2: Display a list of possible answers
        answers = VGroup(
            Text("1. What is a phonon?").scale(0.6),
            Text("2. A brief link to perturbation theory").scale(0.6),
            Text("3. What is a defect?").scale(0.6),
            Text("4. Challenges and fine details").scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(question, DOWN, buff=0.5)

        self.next_slide()
        # Animate the appearance of the answers one by one
        for answer in answers:
            self.play(FadeIn(answer, shift=RIGHT))
            self.next_slide()

        title = Text("What is a phonon?").to_edge(UP)
        self.play(ReplacementTransform(question, title), FadeOut(answers))
        self.next_slide()

class Phonon(Slide):
    def construct(self):
        # Step 1: Display the question
        question = Text("What is a phonon?").to_edge(UP)
        self.add(question)

        self.next_slide()
        # Step 2: Display a list of possible answers
        hyp1 = Tex(r"$\bullet$ It is a vibration in a periodic lattice"
            ).scale(0.6).next_to(question, DOWN).to_edge(LEFT)

        nodes = VGroup(
            MathTex(r"H(x,p) = \frac{p^2}{2m} + V(x)").scale(0.6),
            MathTex(r"H(x,p) = \frac{p^2}{2m} + \frac{1}{2}kx^2").scale(0.6),
            MathTex(r"\omega^2 = \frac{k}{m}").scale(0.6),
        ).arrange(DOWN, buff=1.5).next_to(hyp1, DOWN, buff=0.5).to_edge(RIGHT, buff=1)

        arrows = VGroup(
            Arrow(start=nodes[0].get_bottom(), end=nodes[1].get_top(), buff=0.1),
            Arrow(start=nodes[1].get_bottom(), end=nodes[2].get_top(), buff=0.1),
        )
        self.play(Write(hyp1), run_time = 0.5)
        self.next_slide()
        self.play(Write(nodes), GrowArrow(arrows[0]), GrowArrow(arrows[1]))
        self.next_slide()


        atoms = VGroup()
        spacing = 1.5


        for i in range(-2,3):
            for j in range(-1,2):
                atom = Dot(radius=0.2, color=BLUE).shift(i*RIGHT*spacing + j*UP*spacing)
                atoms.add(atom)

        def set_springs(origin, atoms, shift):
            springs = VGroup()
            index = 0
            for i in range(-2,3):
                for j in range(-1,2):
                    if (i,j) != (0,0):
                        spring = Line(start=origin+shift, end=atoms[index].get_center(), color=YELLOW, stroke_width=50*np.exp(-np.linalg.norm(atoms[index].get_center()-origin)**1.4))
                        springs.add(spring)
                    index += 1
            springs.set_z_index(-1)
            return springs

        atoms[7].set_color(RED)
        atoms.to_corner(DOWN+LEFT, buff=0.5)
        springs = set_springs(atoms[7].get_center(), atoms, 0)

        self.play(Create(atoms))
        self.play(Create(springs))

        label_N = MathTex(r"N = 5 \times 3 = 15"
            ).scale(0.6).next_to(atoms, UP, aligned_edge=RIGHT, buff=0.3
            ).set(color=YELLOW)

        self.play(Write(label_N))
        # self.next_slide(auto_next=True)

        atom0 = atoms[7].copy()
        springs0 = springs.copy()
        shift = (UP+2*RIGHT)*0.3
        atom1 = atoms[7].copy().shift(shift)
        springs1 = set_springs(atoms[7].get_center(), atoms, shift)
        atomm1 = atoms[7].copy().shift(-shift)
        springsm1 = set_springs(atoms[7].get_center(), atoms, -shift)

        self.play(Transform(atoms[7], atom1),
            Transform(springs, springs1))

        self.next_slide(loop=True)
        self.play(Transform(atoms[7], atomm1),
            Transform(springs, springsm1))
        self.play(Transform(atoms[7], atom1),
            Transform(springs, springs1))
        self.next_slide()

        atoms[7].become(atom0)
        springs.become(springs0)
        # self.play(Transform(atoms[7], atom0),
        #         Transform(springs, springs0))

        # force_label = Tex("forces", color=YELLOW).scale(0.6).next_to(atoms, DOWN, aligned_edge=RIGHT, buff=0.3)
        # self.add(force_label)

        hyp2 = MathTex(r"\bullet\ {{k}}({{R_1}}, {{R_2}}) = \frac{\partial^2 E}{\partial u({{R_1}}) \partial u({{R_2}})} \text{\ is a } N\times N \text{ matrix}"
        ).scale(0.6).next_to(nodes, DOWN, buff=0.5).to_edge(LEFT)
        hyp2[1].set(color=YELLOW)
        hyp2[3].set(color=RED)
        hyp2[5].set(color=BLUE)
        hyp2[7].set(color=RED)
        hyp2[9].set(color=BLUE)
        hyp2.next_to(hyp1, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(hyp2))
        self.next_slide()

        nodes1 = VGroup(
            MathTex(r"H(x,p) = \frac{p^2}{2m} + V(x)").scale(0.6),
            MathTex(r"H(u,p) = \frac{p^2}{2m} + \frac{1}{2} \sum_{R_1 R_2} {{k}} ({{R_1}}, {{R_2}}) {{u_{R_1}}} {{u_{R_2}}}").scale(0.6),
            MathTex(r"\omega^2 = \text{diag} \left( \frac{1}{\sqrt{m_1 m_2}} {{k}} ( {{R_1}} , {{R_2}} ) \right)").scale(0.6),
        ).arrange(DOWN, buff=1.5).next_to(hyp1, DOWN, buff=0.5).to_edge(RIGHT, buff=1)
        nodes1[1][1].set(color=YELLOW)
        nodes1[1][3].set(color=RED)
        nodes1[1][5].set(color=BLUE)
        nodes1[1][7].set(color=RED)
        nodes1[1][9].set(color=BLUE)
        nodes1[2][1].set(color=YELLOW)
        nodes1[2][3].set(color=RED)
        nodes1[2][5].set(color=BLUE)
        arrows1 = VGroup(
            Arrow(start=nodes1[0].get_bottom(), end=nodes1[1].get_top(), buff=0.1),
            Arrow(start=nodes1[1].get_bottom(), end=nodes1[2].get_top(), buff=0.1),
        )
        self.play(Transform(nodes, nodes1), Transform(arrows, arrows1))
        self.next_slide()

        hyp3 = Tex(r"$\bullet$ $N$ frequencies found by diagonalizing the matrix"
            ).scale(0.6).next_to(hyp2, DOWN).to_edge(LEFT)
        self.play(Write(hyp3))
        self.next_slide()
        title_out = Tex("force constants and reciprocal space").to_edge(UP)
        self.play(Transform(question, title_out), FadeOut(hyp1),
            FadeOut(hyp2), FadeOut(hyp3), FadeOut(nodes), FadeOut(arrows), FadeOut(atoms),
            FadeOut(springs), FadeOut(label_N))

class ForceConstants(Slide):
    def construct(self):
        lim = 2
        title = Tex("force constants and reciprocal space").to_edge(UP)
        self.add(title)
        hyps = VGroup(
            Tex(r"\mbox{$\bullet$ $N_{at}$ atoms per unit cell can move along $3$ directions $\rightarrow$ $3N_{at}N$ basis vectors}"),
            Tex(r"$\bullet$ \textbf{FC}s as numerical derivatives of forces in a supercell of $N$ unit cells"),
            Tex(r"\mbox{$\bullet$ \textbf{FC}s as perturbation of the Hamiltonian for a $q$-grid of size $N$ (\textbf{Dynamical matrices})}"),
        ).scale(0.6).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(title, DOWN, buff=0.5).to_edge(LEFT)

        for hyp in hyps:
            self.play(Write(hyp))
            self.next_slide()

        axes = NumberLine(x_range=[-lim, lim], length=10, color=WHITE).shift(DOWN*2)
        arr = DoubleArrow(start=axes.n2p(-lim), end=axes.n2p(-lim+2), color=YELLOW, buff=0).shift(UP)
        arr_label = Tex(r"supercell", color=YELLOW).scale(0.6).next_to(arr, UP, buff=0.1)

        three_dots_left = VGroup(
            Dot(axes.n2p(-lim - 0.3), color=GRAY, radius=0.03),
            Dot(axes.n2p(-lim - 0.2), color=GRAY, radius=0.03),
            Dot(axes.n2p(-lim - 0.1), color=GRAY, radius=0.03)
        )

        atoms = VGroup()
        for i in range(-lim, lim):
            at1 = Dot(axes.n2p(i+0.2), color=RED, radius=0.2)
            at2 = Dot(axes.n2p(i+0.6), color=BLUE, radius=0.4)
            atoms.add(at1, at2)
        old_atoms = atoms.copy()
        three_dots_right = VGroup(
            Dot(axes.n2p(lim + 0.1), color=GRAY, radius=0.03),
            Dot(axes.n2p(lim + 0.2), color=GRAY, radius=0.03),
            Dot(axes.n2p(lim + 0.3), color=GRAY, radius=0.03),
        )

        self.play(Create(axes))
        self.play(AnimationGroup(*[
            FadeIn(dot) for dot in three_dots_left], lag_ratio=0.1, run_time=0.5))
        self.play(AnimationGroup(*[
            FadeIn(atom) for atom in atoms], lag_ratio=0.1))
        self.play(AnimationGroup(*[
            FadeIn(dot) for dot in three_dots_right], lag_ratio=0.1, run_time=0.5))
        self.next_slide()
        self.play(GrowArrow(arr), Write(arr_label))
        self.next_slide()

        vecs = []
        label_real = Tex(r"real space").scale(0.6)
        for i in range(4):
            vecs.append(MathTex(r"\left| \ \begin{matrix} R=" + str(i//2 + 1) + r"\\ \tau = " + str((i%2)+1) + r" \\ \alpha = 1 \end{matrix} \ \right\rangle",
                tex_template=amsmath
                ).scale(0.6).next_to(three_dots_right, UP).shift(UP*0.5))
            if i == 0:
                label_real.next_to(vecs[0], LEFT, buff=0.3)
                self.play(Create(vecs[0]), Write(label_real))
            else:
                self.play(ReplacementTransform(vecs[i-1], vecs[i]))
            self.play([atoms[j].animate.shift(RIGHT*0.3) for j in range(i, len(atoms), 4)], run_time=0.5)
            # self.next_slide(auto_next=True)
            self.next_slide(loop=True)
            self.play([atoms[j].animate.shift(LEFT*0.6) for j in range(i, len(atoms), 4)], run_time=0.5)
            self.play([atoms[j].animate.shift(RIGHT*0.6) for j in range(i, len(atoms), 4)], run_time=0.5)
            self.next_slide(auto_next=True)
            [atoms[j].move_to(old_atoms[j].get_center()) for j in range(i, len(atoms), 4)]

        label_reciprocal = Tex(r"reciprocal space").scale(0.6)
        xs = np.linspace(-lim, lim, 200)
        f0 = lambda x: -1
        f12 = lambda x: np.sin(x*np.pi)
        points0 = [axes.n2p(x) + UP * f0(x) for x in xs]
        points12 = [axes.n2p(x) + UP * f12(x) for x in xs]
        curve0 = VMobject(color=YELLOW)
        curve0.set_points_smoothly(points0)
        curve12 = VMobject(color=YELLOW)
        curve12.set_points_smoothly(points12)
        for i in range(4):
            if i < 2:
                q = "0"
                f = f0
            else:
                q = "1/2"
                f = f12
            vecs[i] = MathTex(r"\left| \ \begin{matrix} q=" + q + r"\\ \tau = " + str((i%2)+1) + r" \\ \alpha = 1 \end{matrix} \ \right\rangle",
                tex_template=amsmath
                ).scale(0.6).next_to(three_dots_right, UP).shift(UP*0.5)
            if i == 0:
                label_reciprocal.next_to(vecs[0], LEFT, buff=0.3)
                self.play(ReplacementTransform(vecs[-1], vecs[0]), ReplacementTransform(label_real, label_reciprocal))
                self.play(Create(curve0))
            else:
                self.play(ReplacementTransform(vecs[i-1], vecs[i]))
                if i == 2:
                    self.play(ReplacementTransform(curve0, curve12), arr.animate.shift(UP*0.5), arr_label.animate.shift(UP*0.5))
            self.next_slide()
            r = range(i%2, len(atoms), 2)
            shifts = [f(axes.p2n(atoms[j].get_center())) for j in r]
            self.play(*[atoms[j].animate.shift(RIGHT*0.3 * shift) for j, shift in zip(r, shifts)], run_time=0.5)
            # self.next_slide(auto_next=True)
            self.next_slide(loop=True)
            self.play(*[atoms[j].animate.shift(LEFT *0.6 * shift) for j, shift in zip(r, shifts)], run_time=0.5)
            self.play(*[atoms[j].animate.shift(RIGHT*0.6 * shift) for j, shift in zip(r, shifts)], run_time=0.5)
            self.next_slide()
            [atoms[j].move_to(old_atoms[j].get_center()) for j in r]


        self.play(FadeOut(curve12), FadeOut(vecs[-1]), FadeOut(label_reciprocal),
            FadeOut(arr), FadeOut(arr_label))

        group_old = VGroup(
            axes,
            three_dots_left,
            atoms,
            three_dots_right
        )
        lim = 5
        axes = NumberLine(
            x_range=[-lim, lim, 1],  # x-axis range: from -1 to 4 with step size 1
            # background_line_style={"stroke_color": BLUE, "stroke_width": 1, "stroke_opacity": 0.5}
        ).shift(DOWN * 0.5)

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

        three_dots_right = VGroup(
            Dot(axes.n2p(lim + 0.1), color=GRAY, radius=0.03),
            Dot(axes.n2p(lim + 0.2), color=GRAY, radius=0.03),
            Dot(axes.n2p(lim + 0.3), color=GRAY, radius=0.03),
        )

        group_last = VGroup(
            axes,
            three_dots_left,
            atoms,
            three_dots_right
        )

        self.play(ReplacementTransform(group_old, group_last))
        title_down = Tex("Force contants and lattice translations").to_edge(DOWN)
        self.play(Write(title_down))
        self.next_slide()
        self.play(title_down.animate.to_edge(UP), title.animate.shift(UP*2), FadeOut(hyps))
