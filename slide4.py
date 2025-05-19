from manim import *
from imshow import construct_imshow
from manim_slides import Slide

def create_label(labels):
    labs = [Tex(label).scale(0.6) for label in labels]
    height = max([lab.height for lab in labs])
    width = max([lab.width for lab in labs])
    rect = Rectangle(
        height=height+0.4,
        width=width+0.6,
        color=WHITE,
        fill_opacity=0.1,
    )

    return VGroup( [VGroup(lab, rect.copy()) for lab in labs])



class WorkFlow(Slide):
    def construct(self):
        title = Tex("Practical implementation").to_edge(UP)
        self.add(title)
        self.next_slide()
        labels = [
            "relaxation",
            "phonons in UC and defect SC",
            r"$V(R, R')$",
            r"$V(q, q')$",
            "perturbation theory",
            r"linewidths $\Gamma_{qs}$",
            r"thermal conductivity $\kappa_{\alpha\alpha'}$",
        ]
        chart = create_label(labels
            ).arrange(DOWN, buff=0.2
            ).next_to(title, DOWN, buff=0.5
            ).to_edge(LEFT, buff=0.5
            )

        labels_right = VGroup(
            Tex(r"Follow forces from \texttt{pw.x} till they're zero"),
            Tex(r"Calculate \texttt{ph.x} dynamical matrices for a $q$-grid in UC and at $\Gamma$ in SC"),
            Tex("Difference between the real-space transform of the dynamical matrices (**)"),
            Tex("Double Fourier transform"),
            Tex(r"\begin{flushleft} Fermi Golden rule or non-perturbative from matrix elements and non perturbet kets (*) \end{flushleft} "),
            Tex("Calculate the imaginary part of the energy"),
            Tex("directly from the linewidths"),
        ).scale(0.5)

        for label, label_right in zip(chart, labels_right):
            label_right.next_to(label, RIGHT, buff=0.5)

        for i in range(len(labels_right)-1, -1, -1):
            self.play(
                FadeIn(chart[i]),
                FadeIn(labels_right[i]),
            )
            self.next_slide()

        title_out = Tex("Fourier interpolation").to_edge(UP)
        self.play(
            FadeOut(labels_right),
            FadeOut(chart),
            Transform(title, title_out),
        )
        self.next_slide()

class Centering(Slide):
    def construct(self):
        title = Tex("Fourier interpolation").to_edge(UP)
        self.add(title)

        hyps = VGroup(
            Tex(r"$\bullet$ Fourier series work if $\frac{1}{N} \sum_{n=1}^{N} e^{2\pi i q n} = \delta_{q,0}$"),
            Tex(r"$\bullet$ We have to bring $N\rightarrow \infty$"),
            Tex(r"$\bullet$ Apart from electrostatic effects, FC decay {{exponentially}}"),
            Tex(r"\mbox{$\bullet$ but how do we center? $\rightarrow$ minimizing the distance between $R=0$ and $R' + N$}")
            ).scale(0.6
            ).arrange(DOWN, buff=0.2, aligned_edge=LEFT
            ).next_to(title, DOWN, buff=0.5
            ).to_edge(LEFT, buff=0.5
            )
        # hyps[2][1].set(color=ORANGE)

        graph = Axes(
            x_range=[0, 1, 0.25],
            y_range=[0, 1.2],
            tips=False,
            axis_config={"include_numbers": False},
            # axis_config={"color": BLUE},
            ).scale(0.6
            ).next_to(hyps, DOWN, buff=0.3
            ).to_edge(LEFT, buff=0.5
            )
        xlabel = graph.get_x_axis_label("q", edge=RIGHT).scale(0.6)
        label4 = (MathTex(r"N=4")
            ).scale(0.6
            ).set(color=RED
            ).move_to(graph.c2p(0.2, 0.8)
            )
        label100 = (MathTex(r"N=100")
            ).scale(0.6
            ).set(color=BLUE
            ).next_to(label4, DOWN, buff=0.2
            )
        frac_labels = {
            0: "0",
            0.25: MathTex(r"\tfrac{1}{4}"),
            0.5: MathTex(r"\tfrac{2}{4}"),
            0.75: MathTex(r"\tfrac{3}{4}"),
            1: "1",
        }

        # add them to the x_axis
        labels = graph.get_x_axis().add_labels(frac_labels)
        coordinates = [graph.c2p(x, 4 if x == 0 else 0) for x in np.arange(0,1,0.25)] # + [graph.c2p(x, 4) for x in [0, 1]]

        points = VGroup(
            *[Dot(point, color=YELLOW) for point in coordinates]
        )

        f = lambda x, N : np.real(np.sum(np.exp(2*np.pi*1j*x * np.arange(1, N+1)))) / N
        f4 = lambda x: f(x, 4)
        f100 = lambda x: f(x, 100)
        curve = graph.plot(f4, color=RED)
        curve100 = graph.plot(f100, color=BLUE)

        label_valid = Tex(r"valid only if {{$q = m/N$}}"
            ).scale(0.6
            ).move_to(graph
            )
        label_valid[1].set(color=YELLOW)

        fc_graph = Axes(
            x_range=[-0.5, 4.5, 1],
            y_range=[0, 0.6, 0.5],
            tips=False,
            axis_config={"include_numbers": False},
            ).scale(0.6
            ).next_to(hyps, DOWN, buff=0.3
            ).to_edge(LEFT, buff=0.5
            )
        fc_tot = VGroup(
            fc_graph,
            fc_graph.get_x_axis_label("R'", edge=RIGHT).scale(0.6)

        )
        g = lambda x: np.exp(-x**2)
        fc_points = VGroup([Dot(fc_graph.c2p(x,
            (g(x+4) + g(x) + g(x-4))/2
            ), color=YELLOW)
            for x in range(0,5)])


        arrow = DoubleArrow(
            start = fc_points[0].get_center(),
            end=fc_points[-1].get_center(),
            buff=0.2,
            color=YELLOW,
        )
        arrow_label = MathTex(r"F(0,R') = F(0,R'+N)"
            ).scale(0.6
            ).next_to(arrow, UP, buff=0
            ).set(color=YELLOW
            )
        arrow = VGroup(arrow, arrow_label)


        center_graph = Axes(
            x_range=[-6.5, 6.5, 1],
            y_range=[0, 0.6, 0.5],
            tips=False,
            axis_config={"include_numbers": False},
            ).scale(0.6
            ).next_to(hyps, DOWN, buff=0.3
            ).to_edge(LEFT, buff=0.5
            )
        center_tot = VGroup(
            center_graph,
            graph.get_x_axis_label("R", edge=RIGHT).scale(0.6)
        )
        center_points = VGroup([Dot(center_graph.c2p(x,
            (g(x+4) + g(x) + g(x-4))/2
            ), color=YELLOW)
            for x in range(-2,3)])
        new_range = list(range(-6,-2)) + list(range(3,7))
        new_points = VGroup([Dot(center_graph.c2p(x,0), color=ORANGE)
            for x in new_range]).set_z_index(2)


        uc = Square(
            side_length = 1,
            ).scale(0.6
            # ).to_edge(LEFT, buff=3.5
            # ).shift(2*DOWN
            )

        label_uc = Tex("UC").scale(0.6).move_to(uc)
        sc = Square(
            side_length=uc.side_length*4
            ).align_to(uc, LEFT + DOWN)
        label_sc = Tex("SC").scale(0.6).move_to(sc)
        dashes = VGroup()
        origin = uc.get_corner(DOWN+LEFT)
        for i in range(1,4):
            dashes.add(DashedLine(
                start=origin + i*uc.side_length*RIGHT,
                end=origin+sc.side_length*UP+i*uc.side_length*RIGHT
                ))
            dashes.add(DashedLine(
                start=origin + i*uc.side_length*UP,
                end=origin+sc.side_length*RIGHT+i*uc.side_length*UP
                ))



        atoms = VGroup()
        origin = uc.get_center()
        base = np.array([
            [0.1, 0.15, 0],
            [-0.15, -0.15, 0]
        ])
        radii = [0.1, 0.05]
        for i in range(4):
            for j in range(4):
                for coord, r in zip(base, radii):
                    atoms.add(Dot(origin + uc.side_length * (i * RIGHT + j * UP) + coord, radius=r, color=WHITE))

        periodic_replicas = VGroup()
        origin = atoms[29].get_center()
        for i in range(-2,2):
            for j in range(-1,2):
                    periodic_replicas.add(Dot(origin + sc.side_length * (i * RIGHT + j * UP), color=BLUE))

        lines = VGroup([Line(
            start=atoms[0].get_center(),
            end=p.get_center(),
            color=YELLOW,
            stroke_opacity=0.2,
            stroke_width=np.exp(-0.2 * np.linalg.norm(atoms[0].get_center() - p.get_center()))*20
        ) for p in periodic_replicas]).set_z_index(-100)
        nearer = np.argmax(np.array([p.stroke_width for p in lines]))

        lattice2d = VGroup(
            uc, sc, dashes, label_uc, label_sc,
            atoms, lines, periodic_replicas
            ).move_to(ORIGIN
            ).shift(DOWN*0.9
            )

        lim = 3
        defect_graph = Axes(
            x_range=[-1, lim, 1],
            y_range=[-1, lim, 1],
            tips=False,
            x_length=4*lim,
            y_length=4*lim,
            axis_config={"include_numbers": False},
            ).scale_to_fit_width(self.camera.frame_width / 3
            # ).next_to(hyps[0], DOWN, buff=0.6
            # ).to_edge(RIGHT, buff=1
            ).shift(DOWN*0.6
        ).set_z_index(-2)
        x_label = MathTex("R").scale(0.6).next_to(defect_graph.x_axis.get_end(), RIGHT, buff=0.2)
        y_label = MathTex("R'").scale(0.6).next_to(defect_graph.y_axis.get_end(), RIGHT, buff=0.2)
        explain_label = Tex(r"1D, {{defect}}").scale(0.6).next_to(defect_graph.y_axis.get_start(), RIGHT, buff=0.2)
        explain_label[1].set(color=ORANGE)

        # sigma_plus = 1
        # sigma_minus = 0.1
        # gauss_periodic = lambda x, y: np.exp(-(x-y)**2/sigma_minus) + np.exp(-(x-y-2)**2/sigma_minus) + \
        #     np.exp(-(x-y+2)**2/sigma_minus)
        # gauss = lambda x, y: np.exp(-(x-y)**2/sigma_minus - (x+y)**2/sigma_plus) + np.exp(-(x-y-2)**2/sigma_minus - (x+y-2)**2/sigma_plus) + \
        #     np.exp(-(x-y+2)**2/sigma_minus - (x+y-2)**2/sigma_plus) + np.exp(-(x-y)**2/sigma_minus - (x+y-4)**2/sigma_plus)
        # extent = [-1, lim, -1, lim]
        # construct_imshow("gauss.png", gauss, extent, 800, mapp='magma')
        # construct_imshow("gauss_periodic.png", gauss_periodic, extent, 800, mapp='magma')


        def create_replicas(obj, t):
            tx = t * (defect_graph.c2p(1,0) - defect_graph.c2p(0,0))
            ty = t * (defect_graph.c2p(0,1) - defect_graph.c2p(0,0))
            return VGroup(
                *[obj.copy().shift(tx * x + ty * y) for x in range(2) for y in range(2)]
            )

        x_pos = -0.3
        y_pos = -0.5
        defect_points = create_replicas(Dot(defect_graph.c2p(0,0), radius=0.1, color=ORANGE), 2).set_z_index(2)[:-1]
        other_points = create_replicas(Dot(defect_graph.c2p(x_pos, y_pos), radius=0.06, color=WHITE), 2)

        bisettrice = defect_graph.plot(lambda x: x, color=WHITE, stroke_width=0.8)
        img_periodic = ImageMobject("gauss_periodic.png"
            ).move_to(defect_graph
            ).scale_to_fit_width(defect_graph.width
        )
        img = ImageMobject("gauss.png"
            ).move_to(defect_graph
            ).scale_to_fit_width(defect_graph.width
        )

        def create_distances(x_pos, y_pos):
            return VGroup(
                Line(
                    start=defect_graph.c2p(x_pos,0),
                    end=defect_graph.c2p(x_pos,y_pos),
                    color=RED,
                    stroke_width=6,
                ),
                Line(
                    start=defect_graph.c2p(0,y_pos),
                    end=defect_graph.c2p(x_pos,y_pos),
                    color=BLUE,
                    stroke_width=6,
                ),
                Line(
                    start=defect_graph.c2p((x_pos+y_pos)/2,(x_pos+y_pos)/2),
                    end=defect_graph.c2p(x_pos,y_pos),
                    color=GREEN,
                    stroke_width=6,
                ),
            ).set_z_index(-1)

        y_points = VGroup(
            *[Dot(defect_graph.c2p(0, y_pos + y*2), radius=0.06, color=WHITE) for y in range(2)]
        )
        ydistance0 = create_distances(0, y_pos)[-1]
        ydistance1 = create_distances(0, y_pos + 2)[-1]


        distances0 = create_distances(x_pos, y_pos)
        length0 = np.sum([np.linalg.norm(p.get_start() - p.get_end()) for p in distances0])
        circle0 = Circle(
            radius=length0/2/np.pi,
            color=YELLOW,
            stroke_width=6,
        ).move_to(defect_graph.c2p(x_pos,y_pos))
        distances1 = create_distances(x_pos + 2, y_pos + 2)
        length1 = np.sum([np.linalg.norm(p.get_start() - p.get_end()) for p in distances1])
        circle1 = Circle(
            radius=length1/2/np.pi,
            color=YELLOW,
            stroke_width=6,
        ).move_to(defect_graph.c2p(x_pos+2,y_pos+2))

        t = Triangle(
            stroke_width=0
        )

        triangle_points = VGroup(
            [Dot(p, radius=0.06) for p in t.get_vertices()]
        )
        triangle_points[0].set(color=ORANGE).set(radius=0.1)
        triangle_labels = [
            MathTex("R").scale(0.6).next_to(triangle_points[2], DOWN, buff=0.2),
            MathTex("R'").scale(0.6).next_to(triangle_points[1], DOWN, buff=0.2),
            MathTex("D", color=ORANGE).scale(0.6).next_to(triangle_points[0], UP, buff=0.2),
        ]
        A, B, C = t.get_vertices()
        e1 = Line(A, B, color=RED,   stroke_width=4).set_z_index(-1)
        e2 = Line(B, C, color=GREEN, stroke_width=4).set_z_index(-1)
        e3 = Line(C, A, color=BLUE,  stroke_width=4).set_z_index(-1)

        triangle = VGroup(t, triangle_points, e1, e2, e3, triangle_labels
            ).move_to(defect_graph
            ).to_edge(LEFT, buff=2
            )

        # s0_img = ImageMobject("fc.png"
        #     ).scale(0.5
        #     ).move_to(DOWN*1.1
        #     )

        graph1 = VGroup(
            graph, curve, curve100, label_valid, points, labels,
            xlabel, label4, label100
        ).move_to(ORIGIN).to_edge(DOWN, buff=0.5)
        axes1 = VGroup(
            graph, labels, xlabel
        )
        self.next_slide()
        self.play(Write(hyps[0]))
        self.next_slide()

        self.play(Create(axes1))
        self.play(Create(points))
        self.next_slide()

        self.play(Create(curve), Write(label4))
        self.play(Write(label_valid))
        self.next_slide()

        self.play(Write(hyps[1]))
        self.play(Create(curve100), Write(label100))
        self.next_slide()
        self.play(FadeOut(graph1))

        self.play(Write(hyps[2]))
        self.next_slide()

        l = Tex("1D, pristine").scale(0.6).next_to(fc_tot, RIGHT, buff=0.2)
        self.play(Create(fc_tot))
        self.play(Create(fc_points))
        self.play(Write(l))
        self.next_slide()

        self.play(FadeIn(arrow))
        self.next_slide()

        self.play(FadeOut(arrow))
        self.next_slide()

        self.play(ReplacementTransform(
            VGroup(fc_tot, fc_points),
            VGroup(center_tot, center_points)),
            )
        self.next_slide()

        self.play(Create(new_points), hyps[2][1].animate.set(color=ORANGE))
        self.next_slide()

        self.play(FadeOut(new_points), FadeOut(center_points), FadeOut(center_tot), FadeOut(l))
        self.play(Write(hyps[3]))
        self.next_slide()

        self.play(
            hyps[2].animate.move_to(hyps[0], aligned_edge=LEFT),
            hyps[3].animate.move_to(hyps[1], aligned_edge=LEFT),
            FadeOut(hyps[:2]))
        l = Tex("2D, pristine").scale(0.6).next_to(lattice2d, RIGHT, buff=0.2)
        self.play(Create(l))
        self.play(Create(uc), Write(label_uc))
        self.play(Create(sc), Write(label_sc))
        self.next_slide()

        self.play(FadeOut(label_uc), FadeOut(label_sc), Create(dashes))
        self.play(Create(atoms))
        self.next_slide()

        self.play(atoms[29].animate.set(color=BLUE), atoms[0].animate.set(color=RED))
        self.next_section()

        self.play(Create(periodic_replicas))
        self.play(Create(lines))
        self.play(lines[nearer].animate.set_stroke(opacity=0.8))
        self.next_slide()

        lattice2d.remove(label_uc, label_sc)
        self.play(FadeOut(lattice2d), FadeOut(l))

        # self.play(FadeIn(s0_img))
        # self.next_slide()

        # self.play(FadeOut(s0_img))


        self.play(hyps[3].animate.move_to(hyps[0], aligned_edge=LEFT), FadeOut(hyps[2]))
        l = Tex("1D, pristine, two $R$").scale(0.6).next_to(defect_graph.y_axis.get_start(), RIGHT, buff=0.2)
        self.play(Create(defect_graph), Write(l), Write(x_label), Write(y_label)) #, defect_points, other_points)
        self.next_slide()

        self.play(FadeIn(img_periodic), Create(bisettrice))
        self.next_slide()
        self.play(Indicate(defect_graph.y_axis))
        self.next_slide()

        self.play(Create(y_points))
        self.play(Create(ydistance0), Create(ydistance1))
        self.next_slide()

        self.play(Indicate(y_points[0]))
        self.next_slide()


        self.play(FadeOut(ydistance0), FadeOut(ydistance1), FadeOut(y_points))
        self.play(ReplacementTransform(img_periodic, img), ReplacementTransform(l, explain_label))
        self.play(Create(defect_points))
        self.next_slide()


        self.play(Create(other_points))
        self.next_slide()

        self.play(Indicate(other_points[0]), Indicate(other_points[-1]))
        self.next_slide()

        self.play(Create(triangle))
        self.play(Create(distances0))
        self.play(Create(distances1))

        final_hyp = Tex(r"\mbox{$\bullet$ but how do we center? $\rightarrow$ minimizing the perimeter of the triangle $(R,R',D) for all replicas of $(R,R')$")

        self.next_slide()


        group = VGroup(
            defect_graph, defect_points, other_points,
            distances0, distances1, triangle, bisettrice,
            explain_label, x_label, y_label
        )
        self.play(FadeOut(group), FadeOut(img))
        self.next_slide()
