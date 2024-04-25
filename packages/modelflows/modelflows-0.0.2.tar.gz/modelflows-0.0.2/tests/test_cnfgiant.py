from modelflows.emulator import Emulator


emu = Emulator(grid='cnfgiant')
samples = emu.sample(num_posterior_samples=1000, batch_sample_size=100000, observations=dict(teff=5000., teff_err=50., dnu = 3, dnu_err = 0.1, numax = 30, numax_err = 1., feh = 0, feh_err = 0.1 ), calc_intervals=True, plot_posterior=True)

