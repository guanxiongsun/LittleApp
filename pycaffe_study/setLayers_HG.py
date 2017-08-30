#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 17:43:33 2017

@author: sunguanxiong
"""
from __future__ import print_function
from caffe import layers as L, params as P, to_proto
from caffe.proto import caffe_pb2
#import caffe

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
    batch_norm = L.BatchNorm(bottom, in_place=True, param=[dict(lr_mult=0, 
                                decay_mult=0), dict(lr_mult=0, decay_mult=0), 
                                dict(lr_mult=0, decay_mult=0)])
    scale = L.Scale(batch_norm, bias_term=True, in_place=True)
    return scale

def conv_f(bottom,ks,nout,stride=1,pad=0):
    conv = L.Convolution(bottom, kernel_size=ks, stride=stride,
                         num_output=nout, pad=pad, bias_term=False, 
                         weight_filler=dict(type='msra'))
    return conv

#upsampling with deconv using filter 'Bilinear'
def deconv_f(bottom,ks,nout,stride=2,pad=0):
    deconv = L.Deconvolution(bottom, convolution_param=dict(num_output=nout, 
                            kernel_size=ks, stride=stride, pad=[0],group=nout,
                             weight_filler=dict(type='bilinear'), bias_term=False),
                             param=dict(lr_mult=0, decay_mult=0))
    return deconv

def residual(bottom, numIn, numOut):
    batch_norm = L.BatchNorm(bottom, in_place=False, param=[dict(lr_mult=0, 
                                decay_mult=0), dict(lr_mult=0, decay_mult=0), 
                                dict(lr_mult=0, decay_mult=0)])
    scale = L.Scale(batch_norm, bias_term=True, in_place=True)
    relu = L.Relu(scale, in_place=True);
    
    tmp = int(numOut)/2
    conv1 = conv_bn_sc_rl(relu,1,tmp); # 1x1
    
    conv3 = conv_bn_sc_rl(conv1,3,tmp,1,1); # 3x3
    
    conv1_2 = conv_f(conv3,1,numOut); # 1x1
    
    if numIn == numOut:
        skip = bottom;
    else:
        skip = conv_f(bottom,1,numOut); # 1x1
    
    addition = L.Eltwise(skip,conv1_2,operation=P.Eltwise.SUM);
    
    return addition

def hourglass(inputs, nRepeats, nFeatures):
    up1 = residual(inputs,nFeatures,nFeatures);
    low1 = L.Pooling(inputs, pool = P.Pooling.MAX, kernel_size=2,stride=2);
    low1 = residual(low1,nFeatures,nFeatures);
    
    if nRepeats > 1:
        low2 = hourglass(low1, nRepeats-1, nFeatures);
    else:
        low2 = residual(low1,nFeatures,nFeatures);
    
    low3 = residual(low2,nFeatures,nFeatures);
    
    #upsampling
    #up2 = upsample(low3);
    
    #deconv
    up2 = deconv_f(low3,2,nFeatures);
    
    addition = L.Eltwise(up1,up2,operation=P.Eltwise.SUM);
        
    return addition
 
def lin(inputs, numOut):
    return conv_bn_sc_rl(inputs, 1, numOut);

def createModel(nFeatures, nStacks, nRepeats):
    # now, this code can't recognize include phase, so there will only be a TEST phase data layer
    data, label = L.Data(source='train_lmdb', backend=P.Data.LMDB, batch_size=2, ntop=2,
        transform_param=dict(crop_size=227, mean_value=[104, 117, 123], mirror=True),
        include=dict(phase=getattr(caffe_pb2, 'TRAIN')))
    
    conv1 = conv_bn_sc_rl(data,7,64,2,3);
    r1 = residual(conv1,64,128);
    pool = L.Pooling(r1, pool = P.Pooling.MAX, kernel_size=2,stride=2);
    r2 = residual(pool,128,128);
    r3 = residual(r2,128,nFeatures);
    
    inputs = r3;
    for i in range(nStacks):
        hg = hourglass(inputs, nRepeats, nFeatures);
        
        l1 = residual(hg,nFeatures,nFeatures);
        l2 = residual(hg,nFeatures,nFeatures);
        ll1 = lin(l1, nFeatures);
        ll2 = lin(l2, nFeatures);
        
        tmpOut1 = conv_f(ll1, 1, 38);
        tmpOut2 = conv_f(ll2, 1, 19);
        
        if i < nStacks-1 :
            back1 = conv_f(ll1,1,nFeatures);
            back2 = conv_f(tmpOut1,1,nFeatures);
            back3 = conv_f(tmpOut2,1,nFeatures);
            back4 = conv_f(ll2,1,nFeatures);
            
            addition = L.Eltwise(back1,back2,back3,back4,operation=P.Eltwise.SUM);
            
            inputs = addition;
    return to_proto(tmpOut1,tmpOut2)
    
def make_net():
    with open('HG.prototxt', 'w') as f:
        print(createModel(256,3,4), file = f)
    
if __name__ == '__main__':
    make_net()    
