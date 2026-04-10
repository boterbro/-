from textwrap import wrap

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["mathtext.fontset"] = "dejavusans"


TITLE = "Шпаргалка по физике: 1 курс"
SUBTITLE = "Краткий набор самых нужных формул по стандартным темам первого курса"
OUTPUT = "physics_formula_sheet_ru.pdf"


SECTIONS = [
    (
        "Основные константы и обозначения",
        [
            "• $g \\approx 9.8\\,\\mathrm{m/s^2}$",
            "• $k = \\dfrac{1}{4\\pi\\varepsilon_0} \\approx 9\\cdot10^9\\,\\mathrm{N\\,m^2/C^2}$",
            "• $R = 8.31\\,\\mathrm{J/(mol\\,K)}$",
            "• $N_A = 6.02\\cdot10^{23}\\,\\mathrm{mol^{-1}}$",
            "• $c \\approx 3\\cdot10^8\\,\\mathrm{m/s}$",
            "• $\\varepsilon_0 = 8.85\\cdot10^{-12}\\,\\mathrm{F/m}$",
            "• $\\mu_0 = 4\\pi\\cdot10^{-7}\\,\\mathrm{H/m}$",
        ],
    ),
    (
        "Кинематика",
        [
            "Равномерное движение:",
            "• $x = x_0 + vt$, $s = vt$",
            "Равноускоренное движение:",
            "• $v = v_0 + at$",
            "• $x = x_0 + v_0 t + \\dfrac{at^2}{2}$",
            "• $s = v_0 t + \\dfrac{at^2}{2}$",
            "• $v^2 - v_0^2 = 2as$",
            "Движение по окружности:",
            "• $\\omega = \\dfrac{d\\varphi}{dt}$, $v = \\omega R$",
            "• $a_n = \\dfrac{v^2}{R} = \\omega^2 R$",
            "• $T = \\dfrac{2\\pi}{\\omega}$, $\\nu = \\dfrac{1}{T}$",
        ],
    ),
    (
        "Динамика",
        [
            "• $\\sum \\vec F = m\\vec a$",
            "• $\\vec P = m\\vec g$",
            "• $F_{\\mathrm{upr}} = N$",
            "• $F_{\\mathrm{tr}} = \\mu N$",
            "• $F_{\\mathrm{upr,el}} = kx$",
            "• $F = G\\dfrac{m_1 m_2}{r^2}$",
            "• $a_{\\mathrm{centr}} = \\dfrac{v^2}{R}$",
            "• $F_{\\mathrm{centr}} = m\\dfrac{v^2}{R}$",
        ],
    ),
    (
        "Работа, энергия, мощность",
        [
            "• $A = Fs\\cos\\alpha$",
            "• $N = \\dfrac{A}{t} = Fv\\cos\\alpha$",
            "• $E_k = \\dfrac{mv^2}{2}$",
            "• $E_{p,\\,g} = mgh$",
            "• $E_{p,\\,pr} = \\dfrac{kx^2}{2}$",
            "• $E = E_k + E_p$",
            "• $A_{12} = -(E_{p2} - E_{p1}) = -\\Delta E_p$",
            "• Закон сохранения энергии: $E_{\\mathrm{full}} = const$",
        ],
    ),
    (
        "Импульс и столкновения",
        [
            "• $\\vec p = m\\vec v$",
            "• $\\vec F = \\dfrac{d\\vec p}{dt}$",
            "• $\\vec J = \\int \\vec F\\,dt$, при $F = const$: $\\vec J = \\vec F\\,\\Delta t$",
            "• $\\vec J = \\Delta \\vec p$",
            "• Закон сохранения импульса: $\\sum \\vec p = const$",
        ],
    ),
    (
        "Вращательное движение",
        [
            "• $\\omega = \\omega_0 + \\varepsilon t$",
            "• $\\varphi = \\varphi_0 + \\omega_0 t + \\dfrac{\\varepsilon t^2}{2}$",
            "• $\\omega^2 - \\omega_0^2 = 2\\varepsilon \\Delta\\varphi$",
            "• $M = Fl$",
            "• $M = I\\varepsilon$",
            "• $L = I\\omega$",
            "• $E_{\\mathrm{rot}} = \\dfrac{I\\omega^2}{2}$",
        ],
    ),
    (
        "Колебания и волны",
        [
            "Гармонические колебания:",
            "• $x = A\\cos(\\omega t + \\varphi_0)$",
            "• $v = -A\\omega\\sin(\\omega t + \\varphi_0)$",
            "• $a = -\\omega^2 x$",
            "• $\\omega = 2\\pi\\nu = \\dfrac{2\\pi}{T}$",
            "Пружинный маятник:",
            "• $T = 2\\pi\\sqrt{\\dfrac{m}{k}}$",
            "Математический маятник:",
            "• $T = 2\\pi\\sqrt{\\dfrac{\\ell}{g}}$",
            "Волна:",
            "• $v = \\lambda \\nu = \\dfrac{\\lambda}{T}$",
            "• $k = \\dfrac{2\\pi}{\\lambda}$",
        ],
    ),
    (
        "Молекулярная физика и МКТ",
        [
            "• $\\nu = \\dfrac{m}{M}$, $N = \\nu N_A$",
            "• $pV = \\nu RT$",
            "• $p = nkT$",
            "• $\\rho = \\dfrac{m}{V}$",
            "• $\\overline{E} = \\dfrac{i}{2}kT$",
            "• $U = \\dfrac{i}{2}\\nu RT$",
            "Изопроцессы:",
            "• изотерма: $pV = const$",
            "• изобара: $\\dfrac{V}{T} = const$",
            "• изохора: $\\dfrac{p}{T} = const$",
        ],
    ),
    (
        "Термодинамика",
        [
            "• $Q = \\Delta U + A$",
            "• $A = \\int p\\,dV$, при $p = const$: $A = p\\Delta V$",
            "• $C = \\dfrac{Q}{\\Delta T}$, $c = \\dfrac{Q}{m\\Delta T}$",
            "• $Q = cm\\Delta T$",
            "• $Q_{\\mathrm{pl}} = \\lambda m$",
            "• $Q_{\\mathrm{par}} = rm$",
            "• $C_p - C_v = R$",
            "• $\\gamma = \\dfrac{C_p}{C_v}$",
            "Адиабата:",
            "• $pV^\\gamma = const$",
            "• $TV^{\\gamma - 1} = const$",
            "КПД:",
            "• $\\eta = \\dfrac{A_{\\mathrm{pol}}}{Q_1} = \\dfrac{Q_1 - Q_2}{Q_1}$",
            "• $\\eta_{\\mathrm{Carnot}} = 1 - \\dfrac{T_2}{T_1}$",
        ],
    ),
    (
        "Электростатика",
        [
            "• $F = k\\dfrac{|q_1 q_2|}{r^2}$",
            "• $\\vec E = \\dfrac{\\vec F}{q}$",
            "• $E = k\\dfrac{|q|}{r^2}$",
            "• $\\varphi = k\\dfrac{q}{r}$",
            "• $U = q\\varphi$",
            "• $A = q(\\varphi_1 - \\varphi_2) = qU$",
            "• $C = \\dfrac{q}{U}$",
            "• $W = \\dfrac{CU^2}{2} = \\dfrac{qU}{2} = \\dfrac{q^2}{2C}$",
            "Соединение конденсаторов:",
            "• параллельно: $C = C_1 + C_2 + \\dots$",
            "• последовательно: $\\dfrac{1}{C} = \\dfrac{1}{C_1} + \\dfrac{1}{C_2} + \\dots$",
        ],
    ),
    (
        "Постоянный ток",
        [
            "• $I = \\dfrac{q}{t}$",
            "• $j = \\dfrac{I}{S}$",
            "• $j = nqv$",
            "• $U = IR$",
            "• $R = \\rho\\dfrac{\\ell}{S}$",
            "• $P = UI = I^2R = \\dfrac{U^2}{R}$",
            "• $A = UIt = I^2Rt = \\dfrac{U^2}{R}t$",
            "Для полной цепи:",
            "• $I = \\dfrac{\\mathcal{E}}{R + r}$",
            "• $U = \\mathcal{E} - Ir$",
            "Правила Кирхгофа:",
            "• $\\sum I = 0$",
            "• $\\sum \\mathcal{E} - \\sum IR = 0$",
        ],
    ),
    (
        "Магнитное поле и индукция",
        [
            "• $\\vec F_L = q\\,[\\vec v \\times \\vec B]$, $F_L = qvB\\sin\\alpha$",
            "• $F_A = B I \\ell \\sin\\alpha$",
            "• $B = \\mu_0\\dfrac{I}{2\\pi r}$ (длинный прямой провод)",
            "• $B = \\mu_0\\mu n I$ (соленоид)",
            "• $\\Phi = BS\\cos\\alpha$",
            "• $\\mathcal{E}_i = -\\dfrac{d\\Phi}{dt}$",
            "• $\\mathcal{E}_{\\mathrm{sam}} = -L\\dfrac{dI}{dt}$",
            "• $W_m = \\dfrac{LI^2}{2}$",
        ],
    ),
    (
        "Переменный ток и колебательный контур",
        [
            "• $q = q_0\\cos(\\omega t + \\varphi_0)$",
            "• $I = I_0\\cos(\\omega t + \\varphi_0)$",
            "• $X_L = \\omega L$",
            "• $X_C = \\dfrac{1}{\\omega C}$",
            "• $Z = \\sqrt{R^2 + (X_L - X_C)^2}$",
            "• $I = \\dfrac{U}{Z}$",
            "• $\\omega_0 = \\dfrac{1}{\\sqrt{LC}}$",
            "• $\\nu_0 = \\dfrac{1}{2\\pi\\sqrt{LC}}$",
            "• Резонанс: $X_L = X_C$",
        ],
    ),
    (
        "Оптика",
        [
            "• $n = \\dfrac{c}{v}$",
            "• $n_1\\sin\\alpha = n_2\\sin\\beta$",
            "• $\\dfrac{1}{F} = \\dfrac{1}{d} + \\dfrac{1}{f}$",
            "• $\\Gamma = \\dfrac{h'}{h} = -\\dfrac{f}{d}$",
            "Интерференция:",
            "• максимум: $\\Delta = m\\lambda$",
            "• минимум: $\\Delta = \\left(m + \\dfrac{1}{2}\\right)\\lambda$",
            "Дифракционная решетка:",
            "• $d\\sin\\varphi = m\\lambda$",
        ],
    ),
]


def add_wrapped_text(fig, x, y, text, fontsize=11, weight="normal", color="black"):
    if "$" in text:
        fig.text(x, y, text, fontsize=fontsize, fontweight=weight, color=color, va="top")
        return y - (0.027 if fontsize >= 13 else 0.023)
    width = 66 if fontsize >= 13 else 78
    lines = wrap(text, width=width, break_long_words=False, break_on_hyphens=False) or [text]
    for line in lines:
        fig.text(x, y, line, fontsize=fontsize, fontweight=weight, color=color, va="top")
        y -= 0.027 if fontsize >= 13 else 0.023
    return y


def new_page():
    fig = plt.figure(figsize=(8.27, 11.69))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    return fig


def render_pdf():
    pdf = PdfPages(OUTPUT)
    fig = new_page()
    y = 0.965
    fig.text(0.07, y, TITLE, fontsize=20, fontweight="bold", va="top")
    y -= 0.04
    fig.text(0.07, y, SUBTITLE, fontsize=11, color="#444444", va="top")
    y -= 0.045

    for title, lines in SECTIONS:
        needed_space = 0.04 + len(lines) * 0.024
        if y - needed_space < 0.06:
            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)
            fig = new_page()
            y = 0.96
        y = add_wrapped_text(fig, 0.07, y, title, fontsize=14, weight="bold", color="#0b3d91")
        for line in lines:
            if line.endswith(":") and "$" not in line:
                y = add_wrapped_text(fig, 0.09, y, line, fontsize=11, weight="bold")
            else:
                y = add_wrapped_text(fig, 0.10, y, line, fontsize=11)
        y -= 0.01

    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)
    pdf.close()


if __name__ == "__main__":
    render_pdf()
