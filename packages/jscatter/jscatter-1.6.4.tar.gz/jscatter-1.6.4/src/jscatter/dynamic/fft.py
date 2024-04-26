# -*- coding: utf-8 -*-
# written by Ralf Biehl at the Forschungszentrum Jülich ,
# Jülich Center for Neutron Science 1 and Institute of Complex Systems 1
#    Jscatter is a program to read, analyse and plot data
#    Copyright (C) 2015-2024  Ralf Biehl
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import inspect
import math
import os
import sys
import numbers

import numpy as np
from numpy import linalg as la
import scipy
import scipy.integrate
import scipy.interpolate
import scipy.constants
import scipy.special as special

from jscatter import dataArray as dA
from jscatter import dataList as dL
from jscatter import formel
from jscatter.formel import convolve

try:
    from jscatter.libs import fscatter

    useFortran = True
except ImportError:
    useFortran = False

__all__ = ['getHWHM', 'time2frequencyFF', 'shiftAndBinning', 'dynamicSusceptibility', 't2fFF','h', 'hbar', 'convolve']

pi = np.pi
_path_ = os.path.realpath(os.path.dirname(__file__))

#: Planck constant in µeV*ns
h = scipy.constants.Planck / scipy.constants.e * 1E15  # µeV*ns

#: h/2π  reduced Planck constant in µeV*ns
hbar = h/2/pi  # µeV*ns

try:
    # change in scipy 18
    spjn = special.spherical_jn
except AttributeError:
    spjn = lambda n, z: special.jv(n + 1 / 2, z) * np.sqrt(pi / 2) / (np.sqrt(z))


##################################################################
# frequency domain                                               #
##################################################################

# noinspection PyBroadException
def getHWHM(data, center=0, gap=0):
    """
    Find half width at half maximum (left/right) of a distribution around center.

    The hwhm is determined from linear spline between Y values to find (Y.max-Y.min)/2
    left and right of the max value. Requirement increasing X values and a flat background.
    If nothing is found an empty list is returned.

    For sparse data a fit with a peak function like a Gaussian/Lorezian is prefered.

    Parameters
    ----------
    data : dataArray
        Distribution
    center: float, default=0
        Center (symmetry point) of data.
        If None the position of the maximum is used.
    gap : float, default 0
        Exclude values around center as it may contain a singularity.
        Excludes values within X<= abs(center-gap).
        The gap should be large enough to reach the baseline on left/right peak side.

    Returns
    -------
        list of float with hwhm X>0 , X<0 if existing

    Examples
    --------
    ::

     import jscatter as js
     import numpy as np

     x = np.r_[0:10:200j]
     data = js.formel.gauss(x,3,0.3)
     data.Y += 2
     HWHM = js.dynamic.getHWHM(data,3,1.1)
     # => (2*np.log(2))**0.5*0.3 = 1.177 * sigma = 0.353

    """
    gap = abs(gap)
    if center is None:
        # determine center
        center = data.X[data.Y.argmax()]

    # right side
    data1 = data[:, (data.X >= center + gap)]
    # left side
    data2 = data[:, (data.X <= center - gap)]
    data1.X = data1.X - center
    data2.X = data2.X - center
    res = []

    # right of center
    max = data1.Y.max()
    min = data1.Y.min()
    if np.all(np.diff(data1.X) > 0):
        hwhm1 = np.interp((max - min) / 2. + min, data1.Y.astype(float)[::-1], data1.X.astype(float)[::-1])
        res.append(np.abs(hwhm1))
    else:
        res.append(None)

    # left of center
    max = data2.Y.max()
    min = data2.Y.min()
    if np.all(np.diff(data2.X) > 0):
        hwhm2 = np.interp((max - min) / 2. + min, data2.Y.astype(float), data2.X.astype(float))
        res.append(np.abs(hwhm2))
    else:
        res.append(None)

    return res


def time2frequencyFF(timemodel, resolution, w=None, tfactor=7, **kwargs):
    r"""
    Fast Fourier transform from time domain to frequency domain for inelastic neutron scattering.

    Shortcut t2fFF calls this function.

    Parameters
    ----------
    timemodel : function, None
        Model for I(t,q) in time domain. t in units of ns.
        The values for t are determined from w as :math:`t=[0..n_{max}]\Delta t` with :math:`\Delta t=1/max(|w|)`
        and :math:`n_{max}=w_{max}/\sigma_{min} tfactor`.
        :math:`\sigma_{min}` is the minimal width of the Gaussians given in resolution.
        If None a constant function (elastic scattering) is used.
    resolution : dataArray, float, string
        dataArray that describes the resolution function as multiple Gaussians (use resolution_w).
        A nonzero bgr in resolution is ignored and needs to be added afterwards.
         - float : value is used as width of a single Gaussian in units 1/ns (w is needed below).
                   Resolution width is in the range of 6 1/ns (IN5 TOF) to 1 1/ns (Spheres BS).
         - string : no resolution ('elastic')
    w : array
        Frequencies for the result, e.g. from experimental data.
        If w is None the frequencies resolution.X are used.
        This allows to use the fit of a resolution to be used with same w values.
    kwargs : keyword args
        Additional keyword arguments that are passed to timemodel.
    tfactor : float, default 7
        Factor to determine max time for timemodel to minimize spectral leakage.
        tmax=1/(min(resolution_width)*tfactor) determines the resolution to decay as :math:`e^{-tfactor^2/2}`.
        The time step is dt=1/max(|w|). A minimum of len(w) steps is used (which might increase tmax).
        Increase tfactor if artifacts (wobbling) from the limited time window are visible as the limited time interval
        acts like a window function (box) for the Fourier transform.

    Returns
    -------
    dataArray :     A symmetric spectrum of the Fourier transform is returned.

      .Sq     :math:`\rightarrow S(q)=\int_{-\omega_{min}}^{\omega_{max}} S(Q,\omega)d\omega
      \approx \int_{-\infty}^{\infty} S(Q,\omega)d\omega = I(q,t=0)`

              Integration is done by a cubic spline in w domain on the 'raw' fourier transform of timemodel.

      .Iqt    *timemodel(t,kwargs)* dataArray as returned from timemodel.
              Implicitly this is the Fourier transform to time domain after a successful fit in w domain.
              Using a heuristic model in time domain as multiple Gaussians or stretched exponential allows a convenient
              transform to time domain of experimental data.


    Notes
    -----
    We use Fourier transform with real signals. The transform is defined as

    .. math:: F(f(t)) =  \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{\infty} f(t) e^{-i\omega t} dt

    .. math:: F(f(w)) =  \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{\infty} f(\omega) e^{i\omega t} d\omega

    The resolution function is defined as (see resolution_w)

    .. math:: R_w(w,m_i,s_i,a_i)&= \sum_i a_i e^{-\frac{1}{2}(\frac{w-m_i}{s_i})^2} = F(R_t(t)) \\

                &=\frac{1}{\sqrt{2\pi}} \int_{-\infty}^{\infty}
                  \sum_i{a_i s_i e^{-\frac{1}{2}s_i^2t^2}} e^{-i\omega t} dt

    using the resolution in time domain with same coefficients
    :math:`R_t(t,m_i,s_i,a_i)=\sum_i a_i s_i e^{-\frac{1}{2}s_i^2 t^2}`

    The Fourier transform of a timemodel I(q,t) is

    .. math:: I(q,w) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{\infty} I(q,t) e^{-i\omega t} dt

    The integral is calculated by Fast Fourier transform as

    .. math:: I(q,m\Delta w) = \frac{1}{\sqrt{2\pi}} \Delta t \sum_{n=-N}^{N} I(q,n\Delta t) e^{-i mn/N}

    :math:`t_{max}=tfactor/min(s_i)`.
    Due to the cutoff at :math:`t_{max}` a wobbling might appear indicating spectral leakage.
    Spectral leakage results from the cutoff, which can be described as multiplication with a box function.
    The corresponding Fourier Transform of the box is a *sinc* function visible in the frequency spectrum as wobbling.
    If the resolution is included in time domain, it acts like a window function to reduce
    spectral leakage with vanishing values at :math:`t_{max}=N\Delta t`.
    The second possibility (default) is to increase :math:`t_{max}` (increase tfactor)
    to make the *sinc* sharp and with low wobbling amplitude.

    **Mixed domain models**

    Associativity and Convolution theorem allow to mix models from frequency domain and time domain.
    After transformation to frequency domain the w domain models have to be convoluted with the FFT transformed model.

    Examples
    --------
    Other usage example with a comparison of w domain and transformed from time domain can be found in
    :ref:`A comparison of different dynamic models in frequency domain` or in the example of
    :py:func:`~.dynamic.frequencydomain.diffusionHarmonicPotential_w`.

    Compare transDiffusion transform from time domain with direct convolution in w domain.
    ::

     import jscatter as js
     import numpy as np
     w=np.r_[-100:100:0.5]
     start={'s0':6,'m0':0,'a0':1,'s1':None,'m1':0,'a1':1,'bgr':0.00}
     resolution=js.dynamic.resolution_w(w,**start)
     p=js.grace(1,1)
     D=0.035;qq=3  # diffusion coefficient of protein alcohol dehydrogenase (140 kDa) is 0.035 nm**2/ns
     p.title('Inelastic spectrum IN5 like')
     p.subtitle(r'resolution width about 6 ns\S-1\N, Q=%.2g nm\S-1\N' %(qq))
     # compare diffusion with convolution and transform from time domain
     diff_ffw=js.dynamic.time2frequencyFF(js.dynamic.simpleDiffusion,resolution,q=qq,D=D)
     diff_w=js.dynamic.transDiff_w(w, q=qq, D=D)
     p.plot(diff_w,sy=0,li=[1,3,3],le=r'diffusion D=%.3g nm\S2\N/ns' %(D))
     p.plot(diff_ffw,sy=[2,0.3,2],le='fft from time domain')
     p.plot(diff_ffw.X,diff_ffw.Y+diff_ffw.Y.max()*1e-3,sy=[2,0.3,7],le=r'fft from time domain with bgr')
     # resolution has to be normalized in convolve
     diff_cw=js.dynamic.convolve(diff_w,resolution,normB=1)
     p.plot(diff_cw,sy=0,li=[1,3,4],le='after convolution in w domain')
     p.plot(resolution.X,resolution.Y/resolution.integral,sy=0,li=[1,1,1],le='resolution')
     p.yaxis(min=1e-6,max=5,scale='l',label='S(Q,w)')
     p.xaxis(min=-100,max=100,label='w / ns\S-1')
     p.legend(x=10,y=4)
     p.text(string=r'convolution edge ==>\nmake broader and cut',x=10,y=8e-6)
     # p.save(js.examples.imagepath+'/dynamic_t2f_examples.jpg', size=(2,2))

    .. image:: ../../examples/images/dynamic_t2f_examples.jpg
     :align: center
     :width: 50 %
     :alt: dynamic_t2f_examples.

    Compare the resolutions direct and from transform from time domain.
    ::

     p=js.grace()
     fwres=js.dynamic.time2frequencyFF(None,resolution)
     p.plot(fwres,le='fft only resolution')
     p.plot(resolution,sy=0,li=2,le='original resolution')

    Compare diffusionHarmonicPotential to show simple usage
    ::

     import jscatter as js
     import numpy as np
     t2f=js.dynamic.time2frequencyFF
     dHP=js.dynamic.diffusionHarmonicPotential
     w=np.r_[-100:100]
     ql=np.r_[1:14.1:6j]
     iqw=js.dL([js.dynamic.diffusionHarmonicPotential_w(w=w,q=q,tau=0.14,rmsd=0.34,ndim=3) for q in ql])
     # To move spectral leakage out of our window we increase w and interpolate.
     # The needed factor (here 23) depends on the quality of your data and background contribution.
     iqt=js.dL([t2f(dHP,'elastic',w=w*13,q=q, rmsd=0.34, tau=0.14 ,ndim=3,tfactor=14).interpolate(w) for q in ql])

     p=js.grace()
     p.multi(2,3)
     p[1].title('Comparison direct and FFT  for ndim= 3')
     for i,(iw,it) in enumerate(zip(iqw,iqt)):
         p[i].plot(iw,li=1,sy=0,le='q=$wavevector nm\S-1')
         p[i].plot(it,li=2,sy=0)
         p[i].yaxis(min=1e-5,max=2,scale='log')
         if i in [1,2,4,5]:p[i].yaxis(ticklabel=0)
         p[i].legend(x=5,y=1, charsize=0.7)

    """

    if w is None:  w = resolution.X
    if timemodel is None:
        timemodel = lambda t, **kwargs: dA(np.c_[t, np.ones_like(t)].T)
    gauss = lambda t, si: si * np.exp(-0.5 * (si * t) ** 2)

    if isinstance(resolution, numbers.Number):
        si = np.r_[resolution]
        ai = np.r_[1]
        # mi = np.r_[0]
    elif isinstance(resolution, str):
        si = np.r_[0.5]  # just a dummy
        ai = np.r_[1]
        # mi = np.r_[0]
    else:
        # filter for given values (remove None) and drop bgr in resolution
        sma = np.r_[[[si, mi, ai] for si, mi, ai in zip(resolution.sigmas, resolution.means, resolution.amps)
                     if (si is not None) & (mi is not None)]]
        si = sma[:, 0, None]
        # mi = sma[:, 1, None]  # ignored
        ai = sma[:, 2, None]

    # determine the times and differences dt
    dt = 1. / np.max(np.abs(w))
    nn = int(np.max(w) / si.min() * tfactor)
    nn = max(nn, len(w))
    tt = np.r_[0:nn] * dt

    # calc values
    if isinstance(resolution, str):
        timeresol = np.ones_like(tt)
    else:
        timeresol = ai * gauss(tt, si)  # resolution normalized to timeresol(w=0)=1
        if timeresol.ndim > 1:
            timeresol = np.sum(timeresol, axis=0)
        timeresol = timeresol / (timeresol[0])  # That  S(Q)= integral[-w_min,w_max] S(Q,w)= = I(Q, t=0)
    kwargs.update(t=tt)
    tm = timemodel(**kwargs)
    RY = timeresol * tm.Y  # resolution * timemodel
    # make it symmetric zero only once
    RY = np.r_[RY[:0:-1], RY]
    # do rfft from -N to N
    # using spectrum from -N,N the shift theorem says we get a
    # exp[-j*2*pi*f*N/2] phase leading to alternating sign => use the absolute value
    wn = 2 * pi * np.fft.rfftfreq(2 * nn - 1, dt)  # frequencies
    wY = dt * np.abs(np.fft.rfft(RY).real) / (2 * pi)  # fft

    # now try to average or interpolate for needed w values
    wn = np.r_[-wn[:0:-1], wn]
    wY = np.r_[wY[:0:-1], wY]
    integral = scipy.integrate.simps(wY, wn)

    result = dA(np.c_[wn, wY].T)
    result.setattr(tm)
    try:
        result.modelname += '_t2w'
    except AttributeError:
        result.modelname = '_t2w'
    result.Sq = integral
    result.Iqt = tm
    result.timeresol = timeresol
    result.setColumnIndex(iey=None)
    result.columnname = 'w;Iqw'
    return result


t2fFF = time2frequencyFF


def shiftAndBinning(data, w=None, dw=None, w0=0):
    r"""
    Shift spectrum and average (binning) in intervals.

    The intention is to shift spectra and average over intervals.
    It should be used after convolution with the instrument resolution, when singular values
    at zero are smeared by resolution.

    Parameters
    ----------
    data : dataArray
        Data (from model) to be shifted and averaged in intervals to meet experimental data.
    w : array
        New X values (e.g. from experiment). If w is None data.X values are used.
    w0 : float
        Shift by w0 that w_new = w_old + w0
    dw : float, default None

        Average over intervals between [w[i]-dw,w[i]+dw] to average over a detector pixel width.
        If None dw is half the interval to neighbouring points.
        If 0 the value is only linear interpolated to w values and not averaged (about 10 times faster).

    Notes
    -----
    For averaging over intervals scipy.interpolate.CubicSpline is used with integration in the intervals.

    Returns
    -------
    dataArray

    Examples
    --------
    ::

     import jscatter as js
     import numpy as np
     w = np.r_[-100:100:0.5]
     start = {'s0':6,'m0':0,'a0':1,'s1':None,'m1':0,'a1':1,'bgr':0.00}
     resolution = js.dynamic.resolution_w(w,**start)
     p = js.grace(1,0.6)
     p.plot(resolution, le='original')
     wnew = np.r_[-100:100:1.5]
     p.plot(js.dynamic.shiftAndBinning(resolution,w=wnew,w0=20,dw=0),le='dw=0')
     p.plot(js.dynamic.shiftAndBinning(resolution,w=wnew,w0=20,dw=None),le='dw=None')
     p.plot(js.dynamic.shiftAndBinning(resolution,w=wnew,w0=20,dw=3),le='dw=3')
     p.legend()
     p.yaxis(label='S(w) / a.u.')
     p.xaxis(label=r'w / ns\S-1')
     # p.save(js.examples.imagepath+'/shiftAndBinning.jpg', size=(2,2))

    .. image:: ../../examples/images/shiftAndBinning.jpg
     :align: center
     :width: 50 %
     :alt: dynamic_t2f_examples.

    """
    dataw0 = data.copy()
    if w is None:
        w = data.X.copy()
    dataw0.X += w0
    if dw == 0:
        iwY = dataw0.interp(w)
    else:
        if dw is None:
            dw = np.diff(w)
        else:
            dw = np.ones(len(w) - 1) * dw
        csp = scipy.interpolate.CubicSpline(dataw0.X, dataw0.Y)
        iwY = [csp.integrate(wi - dwl, wi + dwr) / (dwl + dwr) for wi, dwl, dwr in zip(w, np.r_[0, dw], np.r_[dw, 0])]
    result = dA(np.c_[w, iwY].T)
    result.setattr(data)
    result.setColumnIndex(data)

    return result


def dynamicSusceptibility(data, Temp):
    r"""
    Transform from S(w,q) to the  imaginary  part  of  the  dynamic susceptibility.

    .. math::

        \chi (w,q) &= \frac{S(w,q)}{n(w)} (gain side)

                   &= \frac{S(w,q)}{n(w)+1} (loss side)

    with Bose distribution for integer spin particles

    .. math:: with \ n(w)=\frac{1}{e^{hw/kT}-1}

    Parameters
    ----------
    data : dataArray
        Data to transform with w units in 1/ns
    Temp : float
        Measurement temperature in K.

    Returns
    -------
        dataArray

    Notes
    -----
    "Whereas relaxation processes on different time scales are usually hard to identify
    in S(w,q), they appear as distinct peaks in dynamic susceptibility with associated
    relaxation times :math:`\tau ~(2\pi\omega)^{-1}` [1]_.


    References
    ----------
    .. [1] H. Roh et al. ,Biophys. J. 91, 2573 (2006), doi: 10.1529/biophysj.106.082214

    Examples
    --------
    ::

     import jscatter as js
     import numpy as np
     start={'s0':5,'m0':0,'a0':1,'bgr':0.00}
     w=np.r_[-100:100:0.2]
     resolution=js.dynamic.resolution_w(w,**start)
     # model
     def diffindiffSphere(w,q,R,Dp,Ds,w0,bgr):
         diff_w=js.dynamic.transDiff_w(w,q,Ds)
         rot_w=js.dynamic.diffusionInSphere_w(w=w,q=q,D=Dp,R=R)
         Sx=js.formel.convolve(rot_w,diff_w)
         Sxsb=js.dynamic.shiftAndBinning(Sx,w=w,w0=w0)
         Sxsb.Y+=bgr       # add background
         return Sxsb
     #
     q=5.5;R=0.5;Dp=1;Ds=0.035;w0=1;bgr=1e-4
     Iqw=diffindiffSphere(w,q,R,Dp,Ds,w0,bgr)
     IqwR=js.dynamic.diffusionInSphere_w(w,q,Dp,R)
     IqwT=js.dynamic.transDiff_w(w,q,Ds)
     Xqw=js.dynamic.dynamicSusceptibility(Iqw,293)
     XqwR=js.dynamic.dynamicSusceptibility(IqwR,293)
     XqwT=js.dynamic.dynamicSusceptibility(IqwT,293)
     p=js.grace()
     p.plot(Xqw)
     p.plot(XqwR)
     p.plot(XqwT)
     p.yaxis(scale='l',label='X(w,q) / a.u.',min=1e-7,max=1e-4)
     p.xaxis(scale='l',label='w / ns\S-1',min=0.1,max=100)
     # p.save(js.examples.imagepath+'/susceptibility.jpg', size=(2,2))

    .. image:: ../../examples/images/susceptibility.jpg
     :align: center
     :width: 50 %
     :alt: dynamic_t2f_examples.


    """
    ds = data.copy()

    ds.Y[ds.X > 0] = ds.Y[ds.X > 0] / formel.boseDistribution(ds.X[ds.X > 0], Temp).Y
    ds.Y[ds.X < 0] = ds.Y[ds.X < 0] / (formel.boseDistribution(-ds.X[ds.X < 0], Temp).Y + 1)
    ds.Y[ds.X == 0] = 0
    ds.modelname = data.modelname + '_Susceptibility'
    return ds
