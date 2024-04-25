from paltas.Configs.paper_2203_00690.config_val import *
config_dict = copy.deepcopy(config_dict)

config_dict['subhalo']['parameters']['sigma_sub'] = norm(loc=3.8e-3,
	scale=1.5e-4).rvs
config_dict['main_deflector']['parameters']['gamma'] = truncnorm(-195.8,
	np.inf,loc=1.958,scale=0.01).rvs
config_dict['main_deflector']['parameters']['theta_E'] = truncnorm(-73.8,
	np.inf,loc=1.108,scale=0.015).rvs
config_dict['main_deflector']['parameters']['e1'] = norm(loc=-0.034,
	scale=0.01).rvs
config_dict['main_deflector']['parameters']['e2'] = norm(loc=-0.032,
	scale=0.01).rvs
config_dict['main_deflector']['parameters']['center_x'] = norm(loc=0.027,
	scale=0.016).rvs
config_dict['main_deflector']['parameters']['center_y'] = norm(loc=-0.070,
	scale=0.016).rvs
config_dict['main_deflector']['parameters']['gamma1'] = norm(loc=-0.009,
	scale=0.005).rvs
config_dict['main_deflector']['parameters']['gamma2'] = norm(loc=0.003,
	scale=0.005).rvs
