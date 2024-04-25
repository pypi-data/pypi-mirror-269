# -*- coding: utf-8 -*-
"""
Implement a few models for parameter inference.

This module implements models to be used for analysis of strong
lensing parameters.
"""

from tensorflow.keras import layers
from tensorflow.keras.models import Model
import tensorflow as tf


def _xresnet_block(x,filters,kernel_size,strides,conv_shortcut,name,
	trainable=True):
	""" Build a block of residual convolutions for the xresnet model family

	Args:
		x (KerasTensor): The input Keras tensorflow tensor that will be
			passed through the stack.
		filters (int): The number of output filters
		kernel_size (int): The kernel size of each filter
		strides (int): The strides to use for each convolutional filter
		conv_shortcut (bool): When true, will use a convolutional shortcut and
			when false will use an identity shortcut.
		name (str): The name for this block
		trainable (bool): If false, the weights in this block will not be
			trainable.

	Returns:
		(KerasTensor): A Keras tensorflow tensor representing the input after
		the block has been applied
	"""
	# First axis is assumed to be the batch
	bn_axis = -1

	# Use the ResnetD variant for the shortcut
	shortcut = x
	if strides > 1:
		shortcut = layers.AveragePooling2D(pool_size=(2,2),name=name+'_id_pool',
			trainable=trainable)(shortcut)
	if conv_shortcut is True:
		shortcut = layers.Conv2D(filters,1,strides=1,use_bias=False,
			name=name+'_id_conv',trainable=trainable)(shortcut)
		shortcut = layers.BatchNormalization(axis=bn_axis,epsilon=1e-5,
			momentum=0.1,name=name+'_id_bn',trainable=trainable)(shortcut)

	# Set up the rest of the block
	x = layers.ZeroPadding2D(padding=((1,1),(1,1)),name=name+'_pad1',
		trainable=trainable)(x)
	x = layers.Conv2D(filters,kernel_size,strides=strides,use_bias=False,
		name=name+'_conv1',trainable=trainable)(x)
	x = layers.BatchNormalization(axis=bn_axis,epsilon=1e-5,momentum=0.1,
		name=name+'_bn1',trainable=trainable)(x)
	x = layers.Activation('relu',name=name+'_relu1',trainable=trainable)(x)
	x = layers.ZeroPadding2D(padding=((1,1),(1,1)),name=name+'_pad2',
		trainable=trainable)(x)
	x = layers.Conv2D(filters,kernel_size,strides=1,use_bias=False,
		name=name+'_conv2',trainable=trainable)(x)
	x = layers.BatchNormalization(axis=bn_axis,epsilon=1e-5,momentum=0.1,
		name=name+'_bn2',gamma_initializer='zeros',trainable=trainable)(x)

	x = layers.Add(name=name+'_add',trainable=trainable)([shortcut,x])
	x = layers.Activation('relu',name=name+'_out',trainable=trainable)(x)

	return x


def _xresnet_stack(x,filters,kernel_size,strides,conv_shortcut,name,blocks,
	trainable=True):
	""" Build a stack of residual blocks for the xresnet model family

	Args:
		x (KerasTensor): The input Keras tensorflow tensor that will be
			passed through the stack.
		filters (int): The number of output filters
		kernel_size (int): The kernel size of each filter
		strides (int): The strides to use for each convolutional filter
		conv_shortcut (bool): When true, will use a convolutional shortcut and
			when false will use an identity shortcut.
		name (str): The name for this stack
		blocks (int): The number of blocks in this stack
		trainable (bool): If false, weights in this stack will not be trainable.

	Returns:
		(KerasTensor): A Keras tensorflow tensor representing the input after
		the stack has been applied
	"""
	# If the input dimension is not divisible by the stride then we must add
	# padding.
	divide_pad = strides - x.shape[1]%strides
	x = tf.cond(x.shape[1] % strides > 0,lambda:layers.ZeroPadding2D(
		padding=((divide_pad,0),(0,0)),name=name+'_stride_pad_r')(x),
		lambda:x)
	divide_pad = strides - x.shape[2]%strides
	x = tf.cond(x.shape[2] % strides > 0,lambda:layers.ZeroPadding2D(
		padding=((0,0),(divide_pad,0)),name=name+'_stride_pad_c')(x),
		lambda:x)
	# Apply each residual block
	x = _xresnet_block(x,filters,kernel_size,strides,
		conv_shortcut=conv_shortcut,name=name+'_block1',trainable=trainable)
	for i in range(2,blocks+1):
		x = _xresnet_block(x,filters,kernel_size,1,conv_shortcut=False,
			name=name+'_block%d'%(i),trainable=trainable)

	return x


def _xresnet34(conv_inputs,num_outputs,custom_head=False,trainable=True,
	output_trainable=True):
	"""Run a convolutional input through the xresnet34 model described in
	https://arxiv.org/pdf/1812.01187.pdf

	Args:
		conv_inputs (KerasTensor): A KerasTensor with dimension (batch_size,
			image_size,image_size,n_channels) that will be used as the input to
			the xresent_34 model.
		num_outputs (int): The number of outputs to predict
		custom_head (bool): If true, then add a custom head at the end of
			xresnet34 in line with what' used in the fastai code.
		trainable (bool): If False, do not train the convolutional weights.
		output_trainable (bool): If False do not train the last dense layer.

	Returns:
		(KerasTensor): The outputs of the xresnet34 with dimension (batch_size,
		num_outputs).
	"""

	# Assume the first dimension is the batch size
	bn_axis = -1

	# Build the stem of the resnet
	# Conv 1 of stem
	x = layers.ZeroPadding2D(padding=((1,1),(1,1)),name='stem_pad1',
		trainable=trainable)(conv_inputs)
	x = layers.Conv2D(32,3,strides=2,use_bias=False,name='stem_conv1',
		trainable=trainable)(x)
	x = layers.BatchNormalization(axis=bn_axis,epsilon=1e-5,momentum=0.1,
		name='stem_bn1',trainable=trainable)(x)
	x = layers.Activation('relu',name='stem_relu1',trainable=trainable)(x)

	# Conv 2 of stem
	x = layers.ZeroPadding2D(padding=((1,1),(1,1)),name='stem_pad2',
		trainable=trainable)(x)
	x = layers.Conv2D(32,3,strides=1,use_bias=False,name='stem_conv2',
		trainable=trainable)(x)
	x = layers.BatchNormalization(axis=bn_axis,epsilon=1e-5,momentum=0.1,
		name='stem_bn2',trainable=trainable)(x)
	x = layers.Activation('relu',name='stem_relu2',trainable=trainable)(x)

	# Conv 3 of stem
	x = layers.ZeroPadding2D(padding=((1,1),(1,1)),name='stem_pad3',
		trainable=trainable)(x)
	x = layers.Conv2D(64,3,strides=1,use_bias=False,name='stem_conv3',
		trainable=trainable)(x)
	x = layers.BatchNormalization(axis=bn_axis,epsilon=1e-5,momentum=0.1,
		name='stem_bn3',trainable=trainable)(x)
	x = layers.Activation('relu',name='stem_relu3',trainable=trainable)(x)

	# Next step is max pooling of the stem
	x = layers.ZeroPadding2D(padding=((1,1),(1,1)),name='stem_pad4',
		trainable=trainable)(x)
	x = layers.MaxPooling2D(3,strides=2,name='stem_maxpooling',
		trainable=trainable)(x)

	# # Now we apply the residual stacks
	x = _xresnet_stack(x,filters=64,kernel_size=3,strides=1,
		conv_shortcut=False,name='stack1',blocks=3,trainable=trainable)
	x = _xresnet_stack(x,filters=128,kernel_size=3,strides=2,
		conv_shortcut=True,name='stack2',blocks=4,trainable=trainable)
	x = _xresnet_stack(x,filters=256,kernel_size=3,strides=2,
		conv_shortcut=True,name='stack3',blocks=6,trainable=trainable)
	x = _xresnet_stack(x,filters=512,kernel_size=3,strides=2,
		conv_shortcut=True,name='stack4',blocks=3,trainable=trainable)

	# Conduct the pooling and a dense transform to the final prediction
	x = layers.GlobalAveragePooling2D(name='avg_pool')(x)
	if custom_head:
		x = layers.BatchNormalization(axis=bn_axis,epsilon=1e-5,momentum=0.1,
			name='head_bn1',trainable=output_trainable)(x)
		x = layers.Dense(512,use_bias=False,name='head_dense1',
			trainable=output_trainable)(x)
		x = layers.Activation('relu',name='head_relu1')(x)
		x = layers.BatchNormalization(axis=bn_axis,epsilon=1e-5,momentum=0.1,
			name='head_bn2',trainable=output_trainable)(x)
		x = layers.Dense(num_outputs,use_bias=False,name='head_dense2',
			trainable=output_trainable)(x)
		outputs = layers.BatchNormalization(axis=bn_axis,epsilon=1e-5,
			momentum=0.1,name='head_bn3',trainable=output_trainable)(x)
	else:
		outputs = layers.Dense(num_outputs,name='output_dense',
			trainable=output_trainable)(x)

	return outputs


def build_xresnet34(img_size,num_outputs,custom_head=False,
	train_only_head=False):
	""" Build the xresnet34 model described in
	https://arxiv.org/pdf/1812.01187.pdf

	Args:
		img_size ((int,int,int)): A tuple with shape (pix,pix,freq) that
			describes the size of the input images.
		num_outputs (int): The number of outputs to predict
		custom_head (bool): If true, then add a custom head at the end of
			xresnet34 in line with what' used in the fastai code.
		train_only_head (bool): If true, only train the head of the network.

	Returns:
		(keras.Model): An instance of the xresnet34 model implemented in
		Keras.
	"""

	# If we train only the head, then none of the previous weights should be
	# trainable
	trainable = not train_only_head

	# Initialize the inputs
	inputs = layers.Input(shape=img_size)

	# Pass the inputs through out xresnet 34 model.
	outputs = _xresnet34(inputs,num_outputs,custom_head=custom_head,
		trainable=trainable,output_trainable=True)

	model = Model(inputs=inputs,outputs=outputs)

	return model


def build_xresnet34_fc_inputs(img_size,num_outputs,num_fc_inputs,
	train_only_head=False):
	""" Build the xresnet34 model described in
	https://arxiv.org/pdf/1812.01187.pdf but include a few more
	fully connected layers and introduce additional inputs (i.e.
	float values associated with the images) into the fully
	connected layers.

	Args:
		img_size ((int,int,int)): A tuple with shape (pix,pix,freq) that
			describes the size of the input images.
		num_outputs (int): The number of outputs to predict
		num_fc_inputs (int): The number of input floats associated to each
			image.
		train_only_head (bool): If true, only train the head of the network.

	Returns:
		(keras.Model): An instance of the xresnet34 model implemented in
		Keras.
	"""

	# If we train only the head, then none of the previous weights should be
	# trainable
	trainable = not train_only_head

	# Initialize the image inputs
	inputs_image = layers.Input(shape=img_size)

	# Initialize the inputs to the fully connected layer.
	inputs_fc = layers.Input(shape=(num_fc_inputs,))

	# The output of our xresnet is not the input to our fc stack
	xresnet_output = 512

	# Pass the inputs through out xresnet 34 model.
	xr_outputs = _xresnet34(inputs_image,xresnet_output,custom_head=False,
		trainable=trainable,output_trainable=trainable)
	xr_outputs = layers.Activation('relu',name='fc_relu1')(xr_outputs)

	# Assume the first dimension is the batch size
	bn_axis = -1

	# Concatenate the redshifts to the xresnet output.
	x = layers.Concatenate(axis=1,name='fc_concat')([xr_outputs,inputs_fc])
	x = layers.Activation('relu',name='fc_relu2')(x)
	x = layers.BatchNormalization(axis=bn_axis,epsilon=1e-5,momentum=0.1,
		name='fc_bn1',trainable=True)(x)
	x = layers.Dense(256,use_bias=True,name='fc_dense1',trainable=True)(x)
	x = layers.Activation('relu',name='fc_relu3')(x)
	x = layers.BatchNormalization(axis=bn_axis,epsilon=1e-5,momentum=0.1,
		name='fc_bn2',trainable=True)(x)
	x = layers.Dense(128,use_bias=True,name='fc_dense2',trainable=True)(x)
	x = layers.Activation('relu',name='fc_relu4')(x)
	x = layers.BatchNormalization(axis=bn_axis,epsilon=1e-5,momentum=0.1,
		name='fc_bn3',trainable=True)(x)
	outputs = layers.Dense(num_outputs,use_bias=True,name='fc_dense3')(x)

	model = Model(inputs=[inputs_image,inputs_fc],outputs=outputs)

	return model
