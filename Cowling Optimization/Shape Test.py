import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt
import aerosandbox.tools.pretty_plots as p

# Here, all distances are in meters and all angles are in degrees.
elliptical = asb.Airplane(
    name="Elliptical Cowling Shape",

    fuselages=[
        asb.Fuselage(
            name="Elliptical Cowling",
            xsecs=[
                asb.FuselageXSec(
                    xyz_c=[xi, 0, 0],
                    radius= 3 * np.sqrt(1 - (6.5-xi) ** 2/6.5**2)
                )
                for xi in np.cosspace(0, 6.5, 30)
            ]
        )
    ]
)

# Here, all distances are in meters and all angles are in degrees.
C = 0

haack = asb.Airplane(
    name="Example Airplane",

    fuselages=[
        asb.Fuselage(
            name="LV-Haack Cowling",
            xsecs=[
                asb.FuselageXSec(
                    xyz_c=[xi, 0, 0],
                    radius=(3/(np.sqrt(np.pi))) * np.sqrt(np.arccos(1-2*xi/6.5)-np.sin(2*np.arccos(1-2*xi/6.5))/2+C*(np.sin(np.arccos(1-2*xi/6.5)))**3)
                )
                for xi in np.cosspace(0, 6.5, 30)
            ]
        )
    ]
)

elliptical.draw_three_view()
haack.draw_three_view()

alpha = np.linspace(0, 60, 300)

test2 = asb.AeroBuildup(
    airplane=haack,
    op_point=asb.OperatingPoint(
        velocity=13.4112,
        alpha=alpha,
        beta=0
    ),
).run()

test3 = asb.AeroBuildup(
    airplane=elliptical,
    op_point=asb.OperatingPoint(
        velocity=13.4112,
        alpha=alpha,
        beta=0
    ),
).run()

fig, ax = plt.subplots(2, 2)

plt.sca(ax[0, 0])
plt.plot(alpha, test2["CL"], color = 'r', label = "Haack")
plt.plot(alpha, test3["CL"], color = 'b', label = "Elliptical")
plt.legend()
plt.xlabel(r"$\alpha$ [deg]")
plt.ylabel(r"$C_L$")
p.set_ticks(5, 1, 0.5, 0.1)

plt.sca(ax[0, 1])
plt.plot(alpha, test2["CD"], color = 'r', label = "Haack")
plt.plot(alpha, test3["CD"], color = 'b', label = "Elliptical")
plt.legend()
plt.xlabel(r"$\alpha$ [deg]")
plt.ylabel(r"$C_D$")
p.set_ticks(5, 1, 0.05, 0.01)
plt.ylim(bottom=0)

plt.sca(ax[1, 0])
plt.plot(alpha, test2["Cm"], color = 'r', label = "Haack")
plt.plot(alpha, test3["Cm"], color = 'b', label = "Elliptical")
plt.legend()
plt.xlabel(r"$\alpha$ [deg]")
plt.ylabel(r"$C_m$")
p.set_ticks(5, 1, 0.5, 0.1)

plt.sca(ax[1, 1])
plt.plot(alpha, test2["CL"] / test2["CD"], color = 'r', label = "Haack")
plt.plot(alpha, test3["CL"] / test3["CD"], color = 'b', label = "Elliptical")
plt.legend()
plt.xlabel(r"$\alpha$ [deg]")
plt.ylabel(r"$C_L/C_D$")
p.set_ticks(5, 1, 10, 2)

p.show_plot(
    "Elliptical Cone vs Haack Cone"
)