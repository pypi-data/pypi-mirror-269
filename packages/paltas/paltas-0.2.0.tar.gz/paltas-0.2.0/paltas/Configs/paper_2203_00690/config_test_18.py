from paltas.Configs.paper_2203_00690.config_val import *
config_dict = copy.deepcopy(config_dict)

config_dict['subhalo']['parameters']['sigma_sub'] = norm(loc=3.6e-3,
	scale=1.5e-4).rvs
config_dict['main_deflector']['parameters']['gamma'] = truncnorm(-196.1,
	np.inf,loc=1.961,scale=0.01).rvs
config_dict['main_deflector']['parameters']['theta_E'] = truncnorm(-73.4,
	np.inf,loc=1.101,scale=0.015).rvs
config_dict['main_deflector']['parameters']['e1'] = norm(loc=0.043,
	scale=0.01).rvs
config_dict['main_deflector']['parameters']['e2'] = norm(loc=0.008,
	scale=0.01).rvs
config_dict['main_deflector']['parameters']['center_x'] = norm(loc=0.058,
	scale=0.016).rvs
config_dict['main_deflector']['parameters']['center_y'] = norm(loc=-0.016,
	scale=0.016).rvs
config_dict['main_deflector']['parameters']['gamma1'] = norm(loc=0.016,
	scale=0.005).rvs
config_dict['main_deflector']['parameters']['gamma2'] = norm(loc=0.008,
	scale=0.005).rvs
