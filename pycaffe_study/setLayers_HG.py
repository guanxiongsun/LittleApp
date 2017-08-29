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

def conv_bn_sc_rl(bottom, kSize, outCh, stride=1, pad=0):
    conv;
    
    bn_scale(conv);
    
    relu;
    
    return relu

def bn_scale() :
    bn;
    scale;
    return scale

def residual(bottom, numIn, numOut):
    bn_scale();
    
    conv_bn_sc_rl(); # 1x1
    
    conv_bn_sc_rl(); # 3x3
    
    conv1 = conv;
    
    if numIn == numOut:
        skip = bottom;
    else:
        skip = conv(bottom); # 1x1
    
    concat(skip,conv1);
    
    return concat

def hourglass(nRepeats, nFeatures, inputs):
    up1 = residual(inputs)
    low1 = pooling(bottom);
    low1 = residual(low1);
    
    if nRepeats > 1:
        low2 = hourglass(nRepeats-1, nFeatures, low1);
    else:
        low2 = residual(low1);
    
    low3 = residual(low2);
    
    up2 = upsample(low3);
    
    concat(up1,up2);
        
    return concat

def lin(numIn, numOut, inputs):
    return conv_bn_sc_rl(inputs, [1,1], numOut);

der createModel():
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    