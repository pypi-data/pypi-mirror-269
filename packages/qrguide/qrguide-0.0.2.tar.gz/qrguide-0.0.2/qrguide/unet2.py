import theano.tensor as T
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import *
Input, DepthwiseConv2D,Conv2D,SeparableConv2D,concatenate,Lambda,Reshape,add,Dropout,Conv2DTranspose,MaxPooling2D,Concatenate,UpSampling2D
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping,ReduceLROnPlateau
from tensorflow.keras.models import Sequential
import os
from tqdm import tqdm
import scanpy as sc
import numpy as np
from keras.layers.merge import concatenate
from functools import partial
import os, sys, re
from Bio import SeqIO
import pandas as pd
from scipy import special
import torch
import torchmetrics
from tqdm import tqdm
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import transformation
from transformation import *
import analysis_fn
from tensorflow.python.keras.utils.multi_gpu_utils import multi_gpu_model
kld_matcher = re.compile(r"Lindel_pred_test_([\.,\d]{,20})_(\w*).npy")
find_kld = lambda fn : float(kld_matcher.match(fn).group(1))
global ref_lookup
ref_lookup = None
pj = os.path.join
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2" 
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth=True
sess = tf.compat.v1.Session(config=config)

#load dataset
train_label=[]
train_image=[]
test_label=[]
test_image=[]
batch_size=64
num_epochs=100
ann=sc.read_h5ad("/mnt/louisayu/nfs_share/qrcode/K562_LV7A_912class.h5ad")
thre=np.where(np.sum(ann.X.A,axis=1)>0)  #exclude total count=0
anne=ann[thre[0]]
indexx=anne.obs.index.to_numpy()
seq=anne.obs['Refseq'].values
cuts=anne.obs['Cutsite'].values
Y=anne.X.A
yclass=anne.var['label']
train_index=anne.obs.index[anne.obs['TestSet']==False].to_numpy()
test_index=anne.obs.index[anne.obs['TestSet']==True].to_numpy()
#print(train_index)
#a=np.zeros((2,39,4))
#b=np.zeros((41,2,4))

for i in tqdm(train_index):
    train_label.append(np.load('/mnt/louisayu/nfs_share/qrcode/exp2/train912/yyyy_/'+i+'.npy',allow_pickle=False)) 
    img=np.load('/mnt/louisayu/nfs_share/qrcode/exp2/train912/x4/'+i+'.npy',allow_pickle=False).transpose(1,2,0)
    #im1=np.vstack((img,a))
    #im2=np.hstack((b,im1))
    train_image.append(img)


for j in tqdm(test_index):
    test_label.append(np.load('/mnt/louisayu/nfs_share/qrcode/exp2/test912/yyyy_/'+j+'.npy',allow_pickle=False))
    imgt=np.load('/mnt/louisayu/nfs_share/qrcode/exp2/test912/x4/'+j+'.npy',allow_pickle=False).transpose(1,2,0)
    #imt1=np.vstack((imgt,a))
    #imt2=np.hstack((b,imt1))
    test_image.append(imgt)


x_train2 = np.array(train_image,dtype='float32')  
nb_train_samples= len(x_train2)   
y_train2 = np.array(train_label)
index = [i for i in range(len(x_train2))]
np.random.seed(42)
np.random.shuffle(index)
x_train = x_train2[index]
y_train = y_train2[index]

x_test2 = np.array(test_image,dtype='float32')  
nb_test_samples= len(x_test2)   
y_test2 = np.array(test_label)
index = [i for i in range(len(x_test2))]
np.random.seed(42)
np.random.shuffle(index)
x_test = x_test2[index]
y_test = y_test2[index]

input_shape=(41,41,4)



transform_matrix=np.load('/home/louisayu/qrcode/newtrans.npy')#class 894 transformation matrix
from scipy.stats import pearsonr

#frameshift r2 for tensor
def transform_r2(x,y): 
    totalcount = tf.reduce_sum(tf.reshape(x,[-1,41*41]), 1)
    totalcount= tf.reshape(totalcount,(-1,1))
    t2 = tf.expand_dims(totalcount,axis=-1)
    x=x / t2
    X = x.numpy()[:,LIST[:,0],LIST[:,1]] @ transform_matrix
    Y = y.numpy()[:,LIST[:,0],LIST[:,1]] @ transform_matrix
    return pearsonr(X,Y)[0]**2



strategy = tf.distribute.MirroredStrategy()
LIST=np.load("/home/louisayu/qrcode/ymap.npy")#locate 894 in 41*41 matrix
print(LIST.shape)

mas=np.full((41,41),-10000000,dtype='float32')  #add -10^7 to elements not in 894, after softmax they will be 0.
for i in range(LIST.shape[0]):
    mas[LIST[i,0],LIST[i,1]]=0
print(mas)
mask=tf.convert_to_tensor(mas)


def kld_fn(Y1, Y2, reduction='mean'):
    """
    compute symmetric KL divergence ? p*log(p/q)
        Y1: true label, can include zero value
        Y2: predicted values , can not include zero
        reduction : str in ['mean', 'sum', 'none']
    Return:
        KLD: scaler value 
    refer: `https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.kl_div.html`
    """
    assert Y1.shape == Y2.shape, "please make sure the two input vector have aligned dimension"

    totalcount = tf.reduce_sum(tf.reshape(Y1,[-1,41*41]), 1)
    totalcount= tf.reshape(totalcount,(-1,1))
    t2 = tf.expand_dims(totalcount,axis=-1)
    Y1=Y1 / t2
    Y1=Y1.numpy()
    Y2=Y2.numpy()

    Y11=Y1[:,LIST[:,0],LIST[:,1]]
    Y22=Y2[:,LIST[:,0],LIST[:,1]]
    #Y22=softmax(Y222)
    y = Y11 + 1e-6
    y_hat = Y22 + 1e-6

    kl_sum =  lambda i, i_hat: special.kl_div(i,i_hat).sum() /2 + special.kl_div(i_hat,i).sum() / 2
    
    
    # multiple sample
    if len(y.shape) >1:
        klds = [kl_sum(i,i_hat) for i,i_hat in zip(y,y_hat)]
    else:
        klds = kl_sum(y,y_hat)

    if reduction == 'mean':
        KLD = np.mean(klds)
    elif reduction == 'sum':
        KLD = np.sum(klds)
    elif reduction == 'none':
        KLD = np.array(klds)
    else:
        raise ValueError("Invalid argument for reduction")

    return KLD

def softmax(x):
    ps = np.empty(x.shape)
    for i in range(x.shape[0]):
        ps[i,:]  = np.exp(x[i,:])
        ps[i,:] /= np.sum(ps[i,:])
    return ps
    
def top_k_overlap(x, y, k, reduction='none'):

    # the location of top10 events
    a=x.shape[0]
    b=y.shape[0]
    x_top_idxx = x.numpy()[:,LIST[:,0],LIST[:,1]]
    x_top_idx=x_top_idxx.argpartition(-1*k, axis=1)[:,-1*k:]
    #x_top_idx=softmax(x_top_idxy)
    
    y_top_idxx = y.numpy()[:,LIST[:,0],LIST[:,1]]
    y_top_idx=y_top_idxx.argpartition(-1*k, axis=1)[:,-1*k:]


    overlap_ls = [len(np.intersect1d(idxs1, idxs2)) for (idxs1, idxs2) in zip(x_top_idx,y_top_idx)]

    if reduction == 'mean':
        TopK = np.mean(overlap_ls)
    elif reduction == 'sum':
        TopK = np.sum(overlap_ls)
    elif reduction == 'none':
        TopK = np.array(overlap_ls)
    else:
        raise ValueError("Invalid argument for reduction")

    return TopK


def top5_recall_fn(x,y,reduction='mean'):
    fn = partial(top_k_overlap, k=5, reduction=reduction)
    return fn(x,y)

def top10_recall_fn(x,y,reduction='mean'):
    fn = partial(top_k_overlap, k=10, reduction=reduction)
    return fn(x,y)


def Fix_class_W1_distance(Y1, Y2, reduction='mean'):
    """
    Compute the W1 wasserstain distance with the following form
            W1(P1, P2) = \sum_i p_{1,i} * | p_{1,i} - p_{2,i} |
    Input
    --------
        Y1 : ndarray (n_sample, n_events), frequency matrix. Y1 is the base of wassertain.
        Y2 : ndarray (n_sample, n_events), frequency matrix
        reduction : str in ['mean', 'sum', 'none']
    Return
    --------
        W1 : ndarray or scaler, distance for each sample if reduction is 'none'. Otherwise return a reduced W1 over all samples.
    """
    totalcount = tf.reduce_sum(tf.reshape(Y1,[-1,41*41]), 1)
    totalcount= tf.reshape(totalcount,(-1,1))
    t2 = tf.expand_dims(totalcount,axis=-1)
    Y1=Y1 / t2
    Y1=Y1.numpy()
    Y2=Y2.numpy()
    a=Y1.shape[0]
    b=Y2.shape[0]
    Y11=Y1[:,LIST[:,0],LIST[:,1]]
    ps=Y2[:,LIST[:,0],LIST[:,1]]
    #ps=softmax(Y22)

    assert ps.shape == Y11.shape,  "discordant shape between Array 1 and Array 2"
    assert np.isclose(ps.sum(axis=1)[0].item(), 1), "Input is not normalized"

    res = np.abs(ps - Y11)
    W1_elements = np.multiply(Y11,res).sum(axis=1)

    if reduction == 'mean':
        W1 = W1_elements.mean()
    elif reduction == 'sum':
        W1 = W1_elements.sum()
    elif reduction == 'none':
        W1 = W1_elements
    else:
        raise ValueError("Invalid argument for reduction")

    return W1
    

#multinomial loss function
def bloss(y_true,y_pred):
    totalcount = tf.reduce_sum(tf.reshape(y_true,[-1,41*41]), 1)
    totalcount= tf.reshape(totalcount,(-1,1))
    t2 = tf.expand_dims(totalcount,axis=-1)
    y_true=y_true / t2     #transform count to probability
    total_count= tf.clip_by_value(totalcount, 0, 200) #clip total count by 0-200
    return total_count*keras.losses.categorical_crossentropy(y_true,y_pred)
   
def double_conv_block(x, n_filters):
   x = layers.Conv2D(n_filters, 5, padding = "same")(x)
   x = layers.Conv2D(n_filters, 6, padding = "same",activation='tanh')(x)
   #x = LayerNormalization()(x)
   #x = layers.Conv2D(n_filters, 5, padding = "same")(x)
   return x


def downsample_block(x, n_filters):
   f = double_conv_block(x, n_filters)
   p = layers.MaxPool2D(3)(f)
   p = layers.Dropout(0.3)(p)
   return f, p

def upsample_block1(x, conv_features, n_filters):
   # upsample
   x = layers.Conv2DTranspose(n_filters, 4, 3, padding="same")(x)
   # concatenate
   x = layers.concatenate([ZeroPadding2D(((0, 1), (0, 1)))(x), conv_features])
   # dropout
   x = layers.Dropout(0.2)(x)
   # Conv2D twice with ReLU activation
   x = double_conv_block(x, n_filters)
   return x
   
def upsample_block2(x, conv_features, n_filters):
   # upsample
   x = layers.Conv2DTranspose(n_filters, 4, 3, padding="same")(x)
   # concatenate
   x = layers.concatenate([ZeroPadding2D(((0, 2), (0, 2)))(x), conv_features])
   # dropout
   x = layers.Dropout(0.2)(x)
   # Conv2D twice with ReLU activation
   x = double_conv_block(x, n_filters)
   return x
      
# Wrap the model with `multi_gpu_model()` to support multi-GPU training   
with strategy.scope():
    xx=Input(shape=input_shape)
    #down sample#
    
    f1, p1 = downsample_block(xx, 64)
    # 1 - downsample
    f2, p2 = downsample_block(p1, 128)
    # 2 - downsample
    f3, p3 = downsample_block(p2, 256)
    # 3 - downsample
    bottleneck = double_conv_block(p3, 512)
    # 4 - bottleneck
    
    #upsample

    # 6 - upsample
    u6 = upsample_block1(bottleneck,f3, 256)
    # 7 - upsample
    u7 = upsample_block1(u6, f2, 128)
    # 8 - upsample
    u8 = upsample_block2(u7, f1, 64)
    # conv2d
    u9 = double_conv_block(u8, 48)
    #48 to 1 channel
    out1= Conv2D(1, 1, padding="same")(u9)
    #add -10^7 to elements not in 894
    out= Reshape((41,41))(out1)
    out2=tf.math.add(mask, out)
    #flatten for softmax
    X = keras.layers.Reshape((-1,))(out2)
    Y = keras.layers.Activation('softmax')(X)
    #reshape to 41*41 
    outt= Reshape((41,41))(Y)
    model= keras.Model(inputs=xx, outputs=outt)
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.0003),
        loss=bloss,
        run_eagerly=True,   
        metrics=[        
            top5_recall_fn,
            top10_recall_fn,
            kld_fn,
            transform_r2,
            Fix_class_W1_distance],
    )
    
model.summary()

checkpoint_filepath = '/mnt/louisayu/nfs_share2/unet2'
checkpoint_callback = ModelCheckpoint(
    checkpoint_filepath,
    monitor="val_loss",
    save_best_only=True,
    save_weights_only=True,
)
early_stopping = EarlyStopping(monitor="val_top10_recall_fn",
               mode="max",
               patience = 4,
               verbose=1
)
rl= ReduceLROnPlateau(monitor="val_transform_r2", mode="max",
                       factor=0.1, min_lr=1e-6, patience=2, verbose=1)
     
history = model.fit(
    x=x_train,
    y=y_train,
    batch_size=batch_size,
    epochs=num_epochs,
    validation_split=0.1,
    callbacks=[checkpoint_callback, early_stopping, rl],
    shuffle=True
    
)                     
model.save('/mnt/louisayu/nfs_share2/unet2_22.h5')
#model=keras.models.load_model("/mnt/louisayu/nfs_share2/unet2_073.h5",compile=False)

y_prediction = model.predict(x_test)
y_pred=y_prediction[:,LIST[:,0],LIST[:,1]] #select 894
y_testt=y_test[:,LIST[:,0],LIST[:,1]]


def transform_r(x,y): 
    
    totalcount = np.sum(y,1)
    t2 = np.expand_dims(totalcount,axis=-1)
    y=y / t2
    
    X = x @ transform_matrix
    Y = y @ transform_matrix
    return pearsonr(X,Y)[0]**2

def kld_fn1(Y1, Y2, reduction='mean'):
    """
    compute symmetric KL divergence ? p*log(p/q)
        Y1: true label, can include zero value
        Y2: predicted values , can not include zero
        reduction : str in ['mean', 'sum', 'none']
    Return:
        KLD: scaler value 
    refer: `https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.kl_div.html`
    """
    assert Y1.shape == Y2.shape, "please make sure the two input vector have aligned dimension"
    totalcount = np.sum(Y2,1)
    print(totalcount)    
    t2 = np.expand_dims(totalcount,axis=-1)
    Y2=Y2 / t2
    Y11=Y1
    Y22=Y2
    y = Y11 + 1e-6
    y_hat = Y22 + 1e-6

    kl_sum =  lambda i, i_hat: special.kl_div(i,i_hat).sum() /2 + special.kl_div(i_hat,i).sum() / 2

    if len(y.shape) >1:
        klds = [kl_sum(i,i_hat) for i,i_hat in zip(y,y_hat)]
    else:
        klds = kl_sum(y,y_hat)

    if reduction == 'mean':
        KLD = np.mean(klds)
    elif reduction == 'sum':
        KLD = np.sum(klds)
    elif reduction == 'none':
        KLD = np.array(klds)
    else:
        raise ValueError("Invalid argument for reduction")

    return KLD

def softmax(x):
    ps = np.empty(x.shape)
    for i in range(x.shape[0]):
        ps[i,:]  = np.exp(x[i,:])
        ps[i,:] /= np.sum(ps[i,:])
    return ps
    
def top_k_overlap1(x, y, k, reduction='none'):

    a=x.shape[0]
    b=y.shape[0]
    x_top_idxx = x
    x_top_idx=x_top_idxx.argpartition(-1*k, axis=1)[:,-1*k:]
    y_top_idxx = y
    y_top_idx=y_top_idxx.argpartition(-1*k, axis=1)[:,-1*k:]


    overlap_ls = [len(np.intersect1d(idxs1, idxs2)) for (idxs1, idxs2) in zip(x_top_idx,y_top_idx)]

    if reduction == 'mean':
        TopK = np.mean(overlap_ls)
    elif reduction == 'sum':
        TopK = np.sum(overlap_ls)
    elif reduction == 'none':
        TopK = np.array(overlap_ls)
    else:
        raise ValueError("Invalid argument for reduction")

    return TopK


def top5_recall(x,y,reduction='mean'):
    fn = partial(top_k_overlap1, k=5, reduction=reduction)
    return fn(x,y)

def top10_recall(x,y,reduction='mean'):
    fn = partial(top_k_overlap1, k=10, reduction=reduction)
    return fn(x,y)


def Fix_class_W1_distance1(Y1, Y2, reduction='mean'):
    """
    Compute the W1 wasserstain distance with the following form
            W1(P1, P2) = \sum_i p_{1,i} * | p_{1,i} - p_{2,i} |
    Input
    --------
        Y1 : ndarray (n_sample, n_events), frequency matrix. Y1 is the base of wassertain.
        Y2 : ndarray (n_sample, n_events), frequency matrix
        reduction : str in ['mean', 'sum', 'none']
    Return
    --------
        W1 : ndarray or scaler, distance for each sample if reduction is 'none'. Otherwise return a reduced W1 over all samples.
    """
    totalcount = np.sum(Y1,1)

    t2 = np.expand_dims(totalcount,axis=-1)
    Y1=Y1 / t2
    a=Y1.shape[0]
    b=Y2.shape[0]
    Y11=Y1
    ps=Y2
    assert ps.shape == Y11.shape,  "discordant shape between Array 1 and Array 2"
    assert np.isclose(ps.sum(axis=1)[0].item(), 1), "Input is not normalized"

    res = np.abs(ps - Y11)
    W1_elements = np.multiply(Y11,res).sum(axis=1)

    if reduction == 'mean':
        W1 = W1_elements.mean()
    elif reduction == 'sum':
        W1 = W1_elements.sum()
    elif reduction == 'none':
        W1 = W1_elements
    else:
        raise ValueError("Invalid argument for reduction")

    return W1

print("top5_recall:",top5_recall(y_pred,y_testt))
print("top10_recall:",top10_recall(y_pred,y_testt))
print("kld:",kld_fn1(y_pred,y_testt))
print("frameshift_r2:",transform_r(y_pred,y_testt))
print("w1distance:",Fix_class_W1_distance1(y_testt,y_pred))