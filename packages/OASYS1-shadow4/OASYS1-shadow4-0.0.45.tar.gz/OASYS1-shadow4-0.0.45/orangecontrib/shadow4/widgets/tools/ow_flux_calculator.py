import sys, numpy, os

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap

from matplotlib.patches import FancyArrowPatch, ArrowStyle

import orangecanvas.resources as resources

from orangewidget import gui
from orangewidget.widget import OWAction
from orangewidget.settings import Setting

from oasys.widgets.exchange import DataExchangeObject
from oasys.widgets import gui as oasysgui
from oasys.util.oasys_util import get_fwhm
# from orangecontrib.shadow.util.shadow_objects import ShadowBeam
# from orangecontrib.shadow.util.shadow_util import ShadowCongruence
# from orangecontrib.shadow.widgets.gui.ow_automatic_element import AutomaticElement

from syned.widget.widget_decorator import WidgetDecorator

from orangecontrib.shadow4.widgets.gui.ow_automatic_element import AutomaticElement
from orangecontrib.shadow4.util.shadow4_objects import ShadowData
from orangecontrib.shadow4.util.shadow4_util import ShadowCongruence

class FluxCalculator(AutomaticElement):

    name = "Flux Calculator"
    description = "Tools: Flux Calculator"
    icon = "icons/flux.png"
    maintainer = "Luca Rebuffi"
    maintainer_email = "lrebuffi(@at@)anl.gov"
    priority = 5
    category = "User Defined"
    keywords = ["data", "file", "load", "read"]

    inputs = [("Shadow Data", ShadowData, "set_shadow_data")]
    WidgetDecorator.append_syned_input_data(inputs)

    outputs = [{"name": "Shadow Data", "type": ShadowData, "doc": "", }]


    want_main_area = 1
    want_control_area = 1

    input_spectrum = None
    flux_index = -1

    bandwidth_calculation = Setting(0)

    e_min = Setting(0.0)
    e_max = Setting(0.0)
    n_bins = Setting(200)

    usage_path = os.path.join(resources.package_dirname("orangecontrib.shadow_advanced_tools.widgets.thermal"), "misc", "flux_calculator.png")

    input_data = None

    def __init__(self):
        super(FluxCalculator, self).__init__()

        # self.setMaximumWidth(self.CONTROL_AREA_WIDTH+10)
        # self.setMaximumHeight(660)

        box0 = gui.widgetBox(self.mainArea, "", orientation="horizontal")
        # box0 = gui.widgetBox(self.controlArea, "", orientation="horizontal")
        gui.button(box0, self, "Calculate Flux", callback=self.calculate_flux, height=45)

        tabs_setting = oasysgui.tabWidget(self.controlArea)
        # tabs_setting.setFixedHeight(510)
        # tabs_setting.setFixedWidth(self.CONTROL_AREA_WIDTH-8)

        tab_ban = oasysgui.createTabPage(tabs_setting, "Beam Bandwidth")
        tab_out = oasysgui.createTabPage(tabs_setting, "Flux Calculation Results")
        tab_usa = oasysgui.createTabPage(tabs_setting, "Use of the Widget")
        tab_usa.setStyleSheet("background-color: white;")

        bandwidth_box = oasysgui.widgetBox(tab_ban, "Bandwidth", addSpace=True, orientation="vertical")

        gui.comboBox(bandwidth_box, self, "bandwidth_calculation", label="BW Calculation Mode", labelWidth=260,
                     items=["Automatic", "Manual"], sendSelectedValue=False, orientation="horizontal", callback=self.set_bw_calculation_mode)

        self.bandwidth_box_1 = oasysgui.widgetBox(bandwidth_box, "", addSpace=True, orientation="vertical", height=90)
        self.bandwidth_box_2 = oasysgui.widgetBox(bandwidth_box, "", addSpace=True, orientation="vertical", height=90)

        oasysgui.lineEdit(self.bandwidth_box_1, self, "e_min", "Energy min", labelWidth=200, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.bandwidth_box_1, self, "e_max", "Energy max", labelWidth=200, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.bandwidth_box_1, self, "n_bins", "Number of Bins", labelWidth=200, valueType=int, orientation="horizontal")

        self.histo_energy = oasysgui.plotWindow(resetzoom=False,
                                                autoScale=False,
                                                logScale=False,
                                                grid=False,
                                                curveStyle=False,
                                                colormap=False,
                                                aspectRatio=False,
                                                yInverted=False,
                                                copy=False,
                                                save=False,
                                                print_=False,
                                                control=False,
                                                position=False,
                                                roi=False,
                                                mask=False,
                                                fit=False)
        self.histo_energy.setDefaultPlotLines(True)
        self.histo_energy._toolbar.setVisible(False)
        self.histo_energy._interactiveModeToolBar.setVisible(False)
        self.histo_energy._outputToolBar.setVisible(False)
        self.histo_energy.group.setVisible(False)
        self.histo_energy._colorbar.setVisible(False)
        self.histo_energy.setActiveCurveColor(color='blue')
        self.histo_energy.setMinimumWidth(380)

        tab_ban.layout().addWidget(self.histo_energy)

        self.set_bw_calculation_mode()

        self.text = oasysgui.textArea(width=self.CONTROL_AREA_WIDTH-22, height=470)

        tab_out.layout().addWidget(self.text)

        usage_box = oasysgui.widgetBox(tab_usa, "", addSpace=True, orientation="horizontal")

        label = QLabel("")
        label.setAlignment(Qt.AlignCenter)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setPixmap(QPixmap(self.usage_path))

        usage_box.layout().addWidget(label)

        gui.rubber(self.controlArea)

    def set_shadow_data(self, input_data):
        # self.not_interactive = self._check_not_interactive_conditions(input_data)

        # self._on_receiving_input()

        print(">>>> input_data: ", input_data)
        if ShadowCongruence.check_empty_data(input_data):
            self.input_data = input_data.duplicate()
            print(">>>> self.input_data: ", self.input_data)
            if self.is_automatic_run: self.calculate_flux()



    def receive_syned_data(self):
        pass

    def set_bw_calculation_mode(self):
        self.bandwidth_box_1.setVisible(self.bandwidth_calculation==1)
        self.bandwidth_box_2.setVisible(self.bandwidth_calculation==0)

    # def setBeam(self, beam):
    #     try:
    #         if ShadowCongruence.checkEmptyBeam(beam):
    #             if ShadowCongruence.checkGoodBeam(beam):
    #                 self.input_beam = beam
    #
    #                 if self.is_automatic_run: self.calculate_flux()
    #     except Exception as exception:
    #         QMessageBox.critical(self, "Error", str(exception), QMessageBox.Ok)
    #
    #         if self.IS_DEVELOP: raise exception

    def setSpectrumData(self, data):
        if not data is None:
            try:
                if data.get_program_name() == "XOPPY":
                    if data.get_widget_name() == "UNDULATOR_FLUX" or data.get_widget_name() == "XWIGGLER" or data.get_widget_name() == "WS":
                        self.flux_index = 1
                    elif data.get_widget_name() == "BM":
                        self.flux_index = 5
                    else:
                        raise Exception("Connect to one of the following XOPPY widgets: Undulator Spectrum, BM, XWIGGLER, WS")

                    self.input_spectrum = data.get_content('xoppy_data')
                elif data.get_program_name() == "SRW":
                    if data.get_widget_name() == "UNDULATOR_SPECTRUM":
                        self.flux_index = 1
                    else:
                        raise Exception("Connect to one of the following SRW widgets: Undulator Spectrum")

                    self.input_spectrum = data.get_content('srw_data')
                else:
                    raise ValueError("Widget accept data from the following Add-ons: XOPPY, SRW")

                if self.is_automatic_run: self.calculate_flux()
            except Exception as exception:
                QMessageBox.critical(self, "Error", str(exception), QMessageBox.Ok)

                if self.IS_DEVELOP: raise exception

    def calculate_flux(self):
        print(">>>>>>>>>>>>> in calculate_flux")

        spectrum_flux, spectrum_energy = self.input_data.beamline.get_light_source().get_flux()
        print(">>>>> spectrum:", spectrum_flux.shape, spectrum_energy.shape)

        if self.input_data is None: print(">>>> Missing beam")

        if True: # not self.input_data is None and not self.input_spectrum is None:
            if True: # try:
                if self.bandwidth_calculation==1:
                    if self.e_min >= self.e_max: raise ValueError("Energy min should be < Energy max")
                    if self.n_bins <= 0 : raise ValueError("Nr. bins should be > 0")

                    erange = [self.e_min, self.e_max]
                    nbins  = self.n_bins
                else:
                    erange = None
                    nbins  = 200

                self.plot_histo(shadow_data=self.input_data, erange=erange, nbins=nbins)
                flux_factor, resolving_power, energy, ttext = calculate_flux_factor_and_resolving_power(shadow_data=self.input_data, erange=erange, nbins=nbins)

                total_text = ttext

                # flux_at_sample, ttext = calculate_flux_at_sample(self.input_spectrum, self.flux_index, flux_factor, energy)

                # def calculate_flux_at_sample(spectrum_energy, spectrum_flux, energy, flux_factor=1.0):

                flux_at_sample, ttext = calculate_flux_at_sample(spectrum_energy, spectrum_flux, energy, flux_factor=flux_factor)

                ticket = self.input_data.beam.histo2(1, 3, nbins=100, nolost=1, ref=23)

                dx = ticket['fwhm_v'] *1000
                dy = ticket['fwhm_h'] *1000

                total_text += "\n" + ttext

                total_text += "\n\n ---> Integrated Flux : %g"%flux_at_sample + " ph/s"
                total_text += "\n ---> <Flux Density>  : %g"%(flux_at_sample/(dx*dy)) + " ph/s/mm^2"
                total_text += "\n ---> Resolving Power : %g"%resolving_power

                self.text.clear()
                self.text.setText(total_text)

                # self.send("Beam", self.input_beam)
                self.send("Shadow Data", self.input_data)

            else: # except Exception as exception:
                QMessageBox.critical(self, "Error", str(exception), QMessageBox.Ok)

                if self.IS_DEVELOP: raise exception

    def plot_histo(self, shadow_data, erange=None, nbins=200):
        self.histo_energy.clear()

        print(">>>>> histo", shadow_data.beam )
        ticket = shadow_data.beam.histo1(26, nbins=nbins, xrange=erange, nolost=1, ref=23)

        ticket['fwhm'], ticket['fwhm_quote'], ticket['fwhm_coordinates'] = get_fwhm(ticket['histogram'], ticket['bin_center'])

        histogram = ticket['histogram_path']
        bins = ticket['bin_path']
        if ticket['fwhm'] == None: ticket['fwhm'] = 0.0

        self.histo_energy.addCurve(bins, histogram, "Energy", symbol='', color='blue', replace=True) #'+', '^', ','
        self.histo_energy.setGraphXLabel("Energy")
        self.histo_energy.setGraphYLabel("Intensity")
        self.histo_energy.setGraphTitle("Bandwidth: " + str(round(ticket['fwhm'], 4)) + " eV")
        self.histo_energy.setInteractiveMode(mode='zoom')

        n_patches = len(self.histo_energy._backend.ax.patches)
        if (n_patches > 0): self.histo_energy._backend.ax.patches.remove(self.histo_energy._backend.ax.patches[n_patches-1])

        if not ticket['fwhm'] == 0.0:
            x_fwhm_i, x_fwhm_f = ticket['fwhm_coordinates']
            x_fwhm_i, x_fwhm_f = x_fwhm_i, x_fwhm_f
            y_fwhm             = ticket['fwhm_quote']


            self.histo_energy._backend.ax.add_patch(FancyArrowPatch([x_fwhm_i, y_fwhm],
                                                                    [x_fwhm_f, y_fwhm],
                                                                    arrowstyle=ArrowStyle.CurveAB(head_width=2, head_length=4),
                                                                    color='b',
                                                                    linewidth=1.5))
        if min(histogram) < 0: self.histo_energy.setGraphYLimits(min(histogram), max(histogram))
        else:                  self.histo_energy.setGraphYLimits(0, max(histogram))

        self.histo_energy.replot()


def calculate_flux_factor_and_resolving_power(shadow_data, nbins=200, erange=None):
    ticket = shadow_data.beam.histo1(26, nbins=nbins, xrange=None, nolost=1)

    energy_min = ticket['xrange'][0]
    energy_max = ticket['xrange'][-1]

    Denergy_source = numpy.abs(energy_max - energy_min)
    energy = numpy.average([energy_min, energy_max])

    if Denergy_source == 0.0:
        raise ValueError("This calculation is not possibile for a single energy value")

    ticket = shadow_data.beam.histo1(26, nbins=nbins, nolost=1, xrange=erange, ref=23)

    initial_intensity = len(shadow_data.beam.rays)
    final_intensity = ticket['intensity']
    efficiency = final_intensity/initial_intensity
    bandwidth = ticket['fwhm']

    print(">>>>>> bandwidth is: ", bandwidth)
    if bandwidth == 0.0 or bandwidth is None:
        raise ValueError("Bandwidth is 0.0 or None: calculation not possible")

    resolving_power = energy/bandwidth

    if Denergy_source < 4*bandwidth:
        raise ValueError("Source \u0394E (" + str(round(Denergy_source, 2)) + " eV) should be at least 4 times bigger than the bandwidth (" + str(round(bandwidth, 3)) + " eV)")

    text = "\n# SOURCE ---------\n"
    text += "\n Source Central Energy: %g"%round(energy, 2) + " eV"
    text += "\n Source Energy Range  : %g - %g"%(round(energy_min, 2), round(energy_max, 2)) + " eV"
    text += "\n Source \u0394E: %g"%round(Denergy_source, 2) + " eV"

    text += "\n\n# BEAMLINE ---------\n"
    text += "\n Shadow Intensity (Initial): %g"%initial_intensity
    text += "\n Shadow Intensity (Final)  : %g"%final_intensity
    text += "\n"
    text += "\n Efficiency: %g"%round(100*efficiency, 3) + "%"
    text += "\n Bandwidth (at the Image Plane): %g"%round(bandwidth, 3) + " eV"

    beamline_bandwidth = Denergy_source * efficiency

    flux_factor = beamline_bandwidth / (1e-3*energy)

    return flux_factor, resolving_power, energy, text

def calculate_flux_at_sample(spectrum_energy, spectrum_flux, energy, flux_factor=1.0):
    if energy < spectrum_energy[0] or energy > spectrum_energy[-1]: raise ValueError("Spectrum does not contained central energy")
    interpolated_flux = numpy.interp([energy],
                                     spectrum_energy,
                                     spectrum_flux,
                                     left=spectrum_flux[0],
                                     right=spectrum_flux[-1])[0]

    text = "\n# FLUX INTERPOLATION ---------\n"
    text += "\n Initial Flux from Source: %g"%interpolated_flux + " ph/s/0.1%bw"

    return interpolated_flux * flux_factor, text


if __name__ == "__main__":
    from shadow4.beamline.s4_beamline import S4Beamline
    import sys
    from orangecontrib.shadow4.util.shadow4_objects import ShadowData, PreReflPreProcessorData, VlsPgmPreProcessorData

    def get_test_beam():
        from shadow4.beamline.s4_beamline import S4Beamline

        beamline = S4Beamline()

        # electron beam
        from shadow4.sources.s4_electron_beam import S4ElectronBeam
        electron_beam = S4ElectronBeam(energy_in_GeV=6, energy_spread=0.001, current=0.2)
        electron_beam.set_sigmas_all(sigma_x=3.01836e-05, sigma_y=4.36821e-06, sigma_xp=3.63641e-06,
                                     sigma_yp=1.37498e-06)

        # magnetic structure
        from shadow4.sources.undulator.s4_undulator_gaussian import S4UndulatorGaussian
        source = S4UndulatorGaussian(
            period_length=0.042,  # syned Undulator parameter (length in m)
            number_of_periods=38.571,  # syned Undulator parameter
            photon_energy=5000.0,  # Photon energy (in eV)
            delta_e=10.0,  # Photon energy width (in eV)
            ng_e=100,  # Photon energy scan number of points
            flag_emittance=1,  # when sampling rays: Use emittance (0=No, 1=Yes)
            flag_energy_spread=0,  # when sampling rays: Use e- energy spread (0=No, 1=Yes)
            harmonic_number=1,  # harmonic number
            flag_autoset_flux_central_cone=1,  # value to set the flux peak
            flux_central_cone=681709040139326.4,  # value to set the flux peak
        )

        # light source
        from shadow4.sources.undulator.s4_undulator_gaussian_light_source import S4UndulatorGaussianLightSource
        light_source = S4UndulatorGaussianLightSource(name='GaussianUndulator', electron_beam=electron_beam,
                                                      magnetic_structure=source, nrays=15000, seed=5676561)
        beam = light_source.get_beam()

        beamline.set_light_source(light_source)

        # optical element number XX
        from shadow4.beamline.optical_elements.crystals.s4_plane_crystal import S4PlaneCrystal
        optical_element = S4PlaneCrystal(name='Plane Crystal',
                                         boundary_shape=None, material='Si',
                                         miller_index_h=1, miller_index_k=1, miller_index_l=1,
                                         f_bragg_a=False, asymmetry_angle=0.0,
                                         is_thick=1, thickness=0.001,
                                         f_central=1, f_phot_cent=0, phot_cent=5000.0,
                                         file_refl='bragg.dat',
                                         f_ext=0,
                                         material_constants_library_flag=0,
                                         # 0=xraylib,1=dabax,2=preprocessor v1,3=preprocessor v2
                                         )
        from syned.beamline.element_coordinates import ElementCoordinates
        coordinates = ElementCoordinates(p=1.9, q=0, angle_radial=1.164204424, angle_azimuthal=0,
                                         angle_radial_out=1.164204424)
        movements = None
        from shadow4.beamline.optical_elements.crystals.s4_plane_crystal import S4PlaneCrystalElement
        beamline_element = S4PlaneCrystalElement(optical_element=optical_element, coordinates=coordinates,
                                                 movements=movements, input_beam=beam)

        beam, mirr = beamline_element.trace_beam()

        beamline.append_beamline_element(beamline_element)

        # test plot
        if 0:
            from srxraylib.plot.gol import plot_scatter
            plot_scatter(beam.get_photon_energy_eV(nolost=1), beam.get_column(23, nolost=1),
                         title='(Intensity,Photon Energy)', plot_histograms=0)
            plot_scatter(1e6 * beam.get_column(1, nolost=1), 1e6 * beam.get_column(3, nolost=1),
                         title='(X,Z) in microns')

        return ShadowData(beam=beam, beamline=beamline)


    from PyQt5.QtWidgets import QApplication
    a = QApplication(sys.argv)

    ow = FluxCalculator()
    ow.set_shadow_data(get_test_beam())
    ow.show()
    a.exec_()
    ow.saveSettings()


