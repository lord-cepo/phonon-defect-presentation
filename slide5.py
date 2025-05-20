from manim import *
from imshow import physics
from manim_slides import Slide
# ricordati di mettere le fc che cadono in Centering

class Degeneracy(Slide, MovingCameraScene):
    def construct(self):
        title = Tex("Degeneracy and symmetries").to_edge(UP)

        hyps = VGroup(
            # Tex(r"Phosphorus doped Silicon in $4\times 4 \times 4$ SC"),
            # Tex("Weird zig-zag profile in degenerate branch"),
            Tex(r"$\bullet$ The defect breaks some space symmetries, lifting some degeneracies"),
            Tex(r"$\bullet$ Perturbation theory is \textbf{not} gauge invariant")
            ).scale(0.6
            ).arrange(DOWN, buff=0.2, aligned_edge=LEFT
            ).next_to(title, DOWN, buff=0.5
            ).to_edge(LEFT, buff=0.5
            )

        s0_img = ImageMobject("bands01.png").scale(0.4).shift(DOWN)
        s0_img_degen = ImageMobject("bands01_deg.png").scale(0.4).shift(DOWN)

        lim = 5
        s1_ax = NumberPlane(
            x_range=[-lim,lim,1],
            y_range=[-lim,lim,1],
            x_length=3,
            y_length=3,
            # tips=False,
            axis_config={"include_numbers": False}
            )
        s1_kets = VGroup(
            Vector(s1_ax.c2p(lim-1,0), color=RED),
            Vector(s1_ax.c2p(0,lim-1), color=BLUE),
        )
        s1_kets_labels = VGroup(
            MathTex(r"\ket{0}", tex_template=physics).scale(0.5).next_to(s1_kets[0], RIGHT, buff=0.4),
            MathTex(r"\ket{1}", tex_template=physics).scale(0.5).next_to(s1_kets[1], UP, buff=0.4),
        )

        s1_circle = Circle(radius=s1_kets[0].width, color=YELLOW, stroke_width=2).move_to(s1_ax.c2p(0,0))
        s1_1st_formula = MathTex(r"\bra{qs} V(q,-q) \ket{qs}", tex_template=physics)

        E1_deg = 0.03
        E1_0 = 0.06
        E1_1 = -0.02
        E0_0 = 1.2
        E0_1 = 1.2


        e1 = DecimalNumber(E0_0)
        e1_ = e1.copy()
        e2 = DecimalNumber(E0_1)
        e2_ = e2.copy()


        v1 = DecimalNumber(E1_deg)
        v1_ = DecimalNumber(E1_deg)
        v2 = DecimalNumber(E1_deg)
        v2_ = DecimalNumber(E1_deg)

        def get_e1(vector: Vector):
            coords = vector.get_end()[:2]
            coords = coords / np.linalg.norm(coords)
            return E1_0 * coords[0] + E1_1 * coords[1]


        s1_table = MobjectTable(
            [[e1, v1], [e2, v2]],
            col_labels=[MathTex(r"E^{(0)}"), MathTex(r"E^{(1)}")],
            row_labels=[MathTex(r"\langle V \rangle", color= RED, tex_template=physics),
                        MathTex(r"\langle V \rangle", color= BLUE, tex_template=physics)],
            # include_outer_lines=True,
            # num_decimal_places=2
            ).scale(0.6).next_to(s1_ax, RIGHT, buff=0.5)

        s1_group = VGroup(s1_ax, s1_table, s1_circle, s1_kets, s1_kets_labels)
        s1_group.move_to(ORIGIN).shift(DOWN*0.5)

        s1_group_label = Tex(r"degenerate: $\langle 0 | V | 0 \rangle = \langle 1 | V | 1 \rangle$"
            ).scale(0.6
            ).next_to(s1_group, DOWN, buff=0.2)
        s1_group.add(s1_group_label)

        s1_group_label_new = Tex(r"non-degenerate: $\langle 0 | V | 0 \rangle \neq \langle 1 | V | 1 \rangle$"
            ).scale(0.6
            ).move_to(s1_group_label
            )

        v1_update = always_redraw(lambda: v1_.set_value(get_e1(s1_kets[0])))
        v2_update = always_redraw(lambda: v2_.set_value(get_e1(s1_kets[1])))
        s1_table_update = MobjectTable(
            [[e1_, v1_update], [e2_, v2_update]],
            col_labels=[MathTex(r"E^{(0)}"), MathTex(r"E^{(1)}")],
            row_labels=[MathTex(r"\langle V \rangle", color= RED, tex_template=physics),
                        MathTex(r"\langle V \rangle", color= BLUE, tex_template=physics)],
            # include_outer_lines=True,
            # num_decimal_places=2
            ).scale(0.6
            ).move_to(s1_table
            )

        s1_end_label = Tex(r"Degeneracy = kets are garbage", color=YELLOW).scale(0.6).to_edge(DOWN, buff=0.5)
        s1_end_label1 = Tex(r"Diagonalizing the perturbation inside degenerate subspace, we get good kets or at least good energies at that order", color=YELLOW
            ).scale(0.6).to_edge(DOWN, buff=0.5)

        def create_label(label):
            rect = Rectangle(
                height=label.height+0.4,
                width=label.width+0.6,
                color=WHITE,
                fill_opacity=0.1,
            )
            return VGroup( label, rect.copy())


        s2_img = ImageMobject("lw_grid.png").scale(0.25).shift(DOWN)
        s2_img_deg = ImageMobject("lw_grid_deg.png").scale(0.25).shift(DOWN)

        s3_img = ImageMobject("lw_bands.png").scale(0.4).shift(DOWN)

        self.add(title)
        self.next_slide()

        self.play(Write(hyps))
        self.next_slide()

        self.next_slide()
        self.play(FadeIn(s0_img))
        zoom_point = s0_img.get_center() + RIGHT * 1.0 + UP * 0.9
        self.camera.frame.save_state()
        self.next_slide()

        self.play(
            self.camera.frame.animate.set(width=s0_img.width*0.3).move_to(zoom_point),
            run_time=3,
        )
        self.next_slide()


        self.play(ReplacementTransform(s0_img, s0_img_degen), run_time=0.5)
        self.next_slide()

        self.play(Restore(self.camera.frame))
        self.play(FadeOut(s0_img_degen))
        self.play(Create(s1_group))
        self.next_slide()

        self.play(Rotate(s1_kets, angle=2*np.pi, about_point=s1_ax.c2p(0,0)), run_time=4)
        self.next_slide()

        self.play(ReplacementTransform(s1_table, s1_table_update))
        self.play(ReplacementTransform(s1_group_label, s1_group_label_new))
        self.play(Rotate(s1_kets, angle=2*np.pi, about_point=s1_ax.c2p(0,0)), run_time=4)
        self.next_slide()

        self.play(Write(s1_end_label))
        self.next_slide()

        self.play(ReplacementTransform(s1_end_label, s1_end_label1))
        self.next_slide()

        self.play(FadeOut(s1_group), FadeOut(s1_end_label1))
        self.play(FadeIn(s2_img))
        self.next_slide()

        self.play(ReplacementTransform(s2_img, s2_img_deg))
        self.next_slide()

        self.play(FadeOut(s2_img_deg))
        self.play(FadeIn(s3_img))
        self.next_slide()

        self.play(FadeOut(s3_img), FadeOut(hyps), FadeOut(title))

        self.wait(3)