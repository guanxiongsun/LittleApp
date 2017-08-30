#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 17:43:33 2017

@author: sunguanxiong
"""
from __future__ import print_function
from caffe import layers as L, params as P, to_proto
from caffe.proto import caffe_pb2
import caffe

def conv_bn_sc_rl(bottom, ks, nout, stride=1, pad=0):
    conv = L.Convolution(bottom, kernel_size=ks, stride=stride,
                                num_output=nout, pad=pad, bias_term=False, 
                                weight_filler=dict(type='msra'))
    batch_norm = L.BatchNorm(conv, in_place=True, param=[dict(lr_mult=0, 
                                decay_mult=0), dict(lr_mult=0, decay_mult=0), 
                                dict(lr_mult=0, decay_mult=0)])
    scale = L.Scale(batch_norm, bias_term=True, in_place=True)
    relu = L.ReLU(scale, in_place=True)
    return relu

def bn_scale(bottom):
    batch_norm = L.BatchNorm(conv, in_place=True, param=[dict(lr_mult=0, 
                                decay_mult=0), dict(lr_mult=0, decay_mult=0), 
                                dict(lr_mult=0, decay_mult=0)])
    scale = L.Scale(batch_norm, bias_term=True, in_place=True)
    return scale

def conv_f(bottom,ks,nout,stride=1,pad=0):
    conv = L.Convolution(bottom, kernel_size=ks, stride=stride,
                         num_output=nout, pad=pad, bias_term=False, 
                         weight_filler=dict(type='msra'))
    return conv

def deconv_f(bottom,ks,nout,stride=1,pad=0):
    deconv = L.Deconvolution(bottom, convolution_param=dict(num_output=nout, kernel_size=ks, stride=stride, pad=[0],
                             weight_filler=dict(type='constant', value=1), bias_term=False),
                             param=dict(lr_mult=0, decay_mult=0))


def residual(bottom, numIn, numOut):
    bn = bn_scale(bottom);
    
    conv1 = conv_bn_sc_rl(bn,1,numOut/2); # 1x1
    
    conv3 = conv_bn_sc_rl(conv1,3,numOut/2,1,1); # 3x3
    
    conv1_2 = conv_f(conv3,1,numOut); # 1x1
    
    if numIn == numOut:
        skip = bottom;
    else:
        skip = conv_f(bottom,1,numOut); # 1x1
    
    addition = L.Eltwise(skip,conv1_2,operation=P.Eltwise.SUM);
    
    return addition

def hourglass(nRepeats, nFeatures, inputs):
    up1 = residual(inputs,nFeatures,nFeatures);
    low1 = L.Pooling(bottom, pool = P.Pooling.MAX, 2,2);
    low1 = residual(low1,nFeatures,nFeatures);
    
    if nRepeats > 1:
        low2 = hourglass(nRepeats-1, nFeatures, low1);
    else:
        low2 = residual(low1,nFeatures,nFeatures);
    
    low3 = residual(low2,nFeatures,nFeatures);
    
    #upsampling
    #up2 = upsample(low3);
    
    #deconv
    up2 = deconv_f(low3,2,nFeatures);
    
    addition = L.Eltwise(up1,up2,operation=P.Eltwise.SUM);
        
    return addition

def lin(numIn, numOut, inputs):
    return conv_bn_sc_rl(inputs, [1,1], numOut);

der createModel(nFeatures, nStacks):
    # now, this code can't recognize include phase, so there will only be a TEST phase data layer
    data, label = L.Data(source=train_lmdb, backend=P.Data.LMDB, batch_size=batch_size, ntop=2,
        transform_param=dict(crop_size=227, mean_value=[104, 117, 123], mirror=True),
        include=dict(phase=getattr(caffe_pb2, 'TRAIN')))
    
    conv1 = conv_bn_sc_rl(data,7,64,2,3);
    r1 = residual(conv1,64,128);
    pool = L.Pooling(bottom, pool = P.Pooling.MAX, 2,2);
    r2 = residual(pool,128,128);
    r3 = residual(128,nFeatures);
    
    for i in range(nStacks):
        hg = hourglass()
        
        
    return
    
    
    
    
    
    
    
    
    
    
    
    