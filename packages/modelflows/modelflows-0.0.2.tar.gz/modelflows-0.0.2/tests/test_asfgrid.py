from modelflows.emulator import Emulator


emu = Emulator(grid='asfgrid')
samples = emu.sample(num_posterior_samples=1000, batch_sample_size=100000, observations=dict(teff=5400., teff_err=200., dnu = 17.47, dnu_err = 0.1, numax = 208.2, numax_err = 1.1, feh = -2.38, feh_err = 0.08 ), evstate = 0, calc_intervals=True, plot_posterior=True)

