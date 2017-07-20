#!/usr/bin/python
"""
Created on Jul 10, 2017

@author: flg-ma
@attention: Jerk Metric
@contact: marcel.albus@ipa.fraunhofer.de (Marcel Albus)
@version: 1.4.1
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


# plot data in one figure
def plot1figure(xAxis, yAxis, legendLabel='legend label', xLabel='x-axis label', yLabel='y-axis label',
                title='plot', axSize='auto', show=0):
    """
    :param xAxis: time axis data
    :param yAxis: data for y axis
    :param legendLabel: label name for first y-axis data (e.g. '$v_x$' for velocity in x-direction)
    :param xLabel: label for time axis (mostly 'Time [s]')
    :param yLabel: label for first y-axis (e.g. '$v [m/s]$', for given example above)
    :param title: title of the plot (obviously)
    :param axSize: 'auto' means min and max is chosen automatically, otherwise: [x_min, x_max, y_min, y_max]
    :param show: shall plot be shown? 1: yes / 2: no
    """
    if show == 1:
        global n
        plt.figure(n, figsize=(16.0, 10.0))
        plt.plot(xAxis, yAxis, 'r', label=legendLabel)
        plt.title(title, fontsize=20)
        plt.xlabel(xLabel, fontsize=20)
        plt.ylabel(yLabel, fontsize=20)
        plt.grid(True)

        if axSize != 'auto':
            plt.axis(axSize)

        plt.legend()
        plt.savefig(title + '.pdf', bbox_inches='tight')

        # increment figure number counter
        n += 1
    else:
        pass


# plot 2 subplots in one figure
def plot2Subplots(xAxis, yAxis1, yAxis2, legendLabel1='first legend label', legendLabel2='second legend label',
                  xLabel='x-axis label', yLabel1='y-axis label 1', yLabel2='y-axis label 2',
                  title='plot', axSize='auto', show=0):
    """
    @param xAxis: time axis array
    @param yAxis1: data for first y-axis as array
    @param yAxis2: data for second y-axis as array
    @param legendLabel1: label name for first y-axis data (e.g. '$v_x$' for velocity in x-direction)
    @param legendLabel2: label name for second y-axis data (e.g. '$v_y$' for velocity in y-direction)
    @param xLabel: label for time axis (mostly 'Time [s]')
    @param yLabel1: label for first y-axis (e.g. '$v [m/s]$', for given example above)
    @param yLabel2: label for second y-axis (e.g. '$v [m/s]$', for given example above)
    @param title: title of the plot (obviously)
    @param n: number of figure
    @param axSize: 'auto' means min and max is chosen automatically, otherwise: [x_min, x_max, y_min, y_max]
    @param show: shall plot be shown? 1: yes / 2: no
    @return: nothing
    """

    if show == 1:
        global n
        plt.figure(n, figsize=(16.0, 10.0))
        plt.subplot(211)
        plt.plot(xAxis, yAxis1, 'r', label=legendLabel1)
        plt.title(title, fontsize=20)
        plt.ylabel(yLabel1, fontsize=20)
        plt.grid(True)
        if axSize != 'auto':
            plt.axis(axSize)
        # legend: loc='best' sets legend to best location
        plt.legend()
        plt.subplot(212)
        plt.plot(xAxis, yAxis2, 'g', label=legendLabel2)
        plt.xlabel(xLabel, fontsize=20)
        plt.ylabel(yLabel2, fontsize=20)
        plt.grid(True)
        if axSize != 'auto':
            plt.axis(axSize)
        # legend: loc='best' sets legend to best location
        plt.legend()
        plt.savefig(title + '.pdf', bbox_inches='tight')

        # increment figure number counter
        n += 1
    else:
        pass


# plot the specified figures
def show_figures():
    # plot position
    plot2Subplots(A[:, AD.TIME], A[:, AD.POS_X], A[:, AD.POS_Y],
                  '$Pos_x$', '$Pos_y$', 'Time [s]', 'x [m]',
                  'x [m]', 'Position', axSize='auto', show=0)

    # plot velocity
    plot2Subplots(A[:, AD.TIME], A[:, AD.VEL_X], A[:, AD.VEL_Y],
                  '$v_x$', '$v_y$', 'Time [s]', 'v [m/s]', 'v [m/s]',
                  title='Velocity', show=0)

    # plot velocity (x^2+y^2)^0.5 diff
    plot2Subplots(A[:-1, AD.TIME], np.sqrt(A_diff[:, AD.POS_X] ** 2 + A_diff[:, AD.POS_Y] ** 2),
                  np.sqrt(A[:-1, AD.VEL_X] ** 2 + A[:-1, AD.VEL_Y] ** 2),
                  '$v_{x,diff,root}$', '$v_{x,odo,root}$', 'Time [s]', 'v [m/s]', 'v [m/s]',
                  title='Velocity calculated using \'diff\'', show=0)

    # plot velocity (x^2+y^2)^0.5 gradient
    plot2Subplots(A[:, AD.TIME], A_grad_vel[:, ],
                  np.sqrt(A[:, AD.VEL_X] ** 2 + A[:, AD.VEL_Y] ** 2),
                  '$v_{x,grad,root}$', '$v_x{x,odo,root}$', 'Time [s]',
                  'v [m/s]', 'v [m/s]', title='Velocity calculated using \'gradient\'',
                  axSize=[0, 73, -.05, .3], show=0)

    # plot acceleration diff: x,y
    plot2Subplots(A[:-1, AD.TIME], A_diff[:, AD.VEL_X], A_diff[:, AD.VEL_Y],
                  '$a_x$', '$a_y$', 'Time [s]', '$\mathrm{a\quad[m/s^2]}$', '$\mathrm{a\quad[m/s^2]}$',
                  'Acceleration', axSize='auto', show=0)

    # plot diff and gradient method comparison for acceleration
    plot2Subplots(A[:-1, AD.TIME], A_grad_acc[:-1, ], np.sqrt(A_diff[:, AD.VEL_X] ** 2 + A_diff[:, AD.VEL_Y] ** 2),
                  '$a_{grad}$', '$a_{diff}$', 'Time [s]', '$\mathrm{a\;[m/s^2]}$',
                  '$\mathrm{a\;[m/s^2]}$', 'Diff_Grad', axSize='auto', show=0)

    # plot acceleration smoothed and noisy signal
    plot2Subplots(A[:, AD.TIME], smooth(A_grad_acc[:, ], 30, window='hanning'),
                  A_grad_acc[:, ], '$a_{grad,smoothed}$', '$a_{grad,noisy}$',
                  'Time [s]', '$\mathrm{a\;[m/s^2]}$', '$\mathrm{a\;[m/s^2]}$',
                  'Acceleration', axSize=[0, 80, -.1, 1.0], show=0)

    # plot acceleration x,y separately
    plot2Subplots(A[:, AD.TIME], A_grad_acc_x, A_grad_acc_y, '$a_{grad,x}$', '$a_{grad,y}$',
                  'Time [s]', '$\mathrm{a\;[m/s^2]}$', '$\mathrm{a\;[m/s^2]}$',
                  title='Acceleration: x,y direction', show=0)

    # plot jerk smoothed and noisy: 30 is good value for smoothing
    plot2Subplots(A[:, AD.TIME], smooth(A_grad_jerk[:, ], 30, window='hanning'),
                  A_grad_jerk[:, ], '$j_{grad,smoothed}$', '$j_{grad,noisy}$',
                  'Time [s]', '$\mathrm{j\;[m/s^3]}$', '$\mathrm{j\;[m/s^3]}$',
                  'Jerk', axSize=[0, 80, -.5, 15], show=0)
    plt.show()


# plot smoothing comparison with different parameter for smoothing
def smoothing_plot():
    global n
    plt.figure(n, figsize=(16.0, 10.0))
    plt.plot(A[:, AD.TIME], A[:, AD.VEL_X], 'r',
             label='$v_{normal}$')
    plt.plot(A[:, AD.TIME], smooth(A[:, AD.VEL_X], 30, window='hanning'),
             label='$v_{smooth,1\,times}$')
    plt.plot(A[:, AD.TIME], smooth(
        smooth(A[:, AD.VEL_X], 10, window='hanning'),
        50, window='hamming'), label='$v_{smooth,2\,times}$')
    plt.grid(True)
    plt.xlabel('Time [s]')
    plt.ylabel('v [m/s]')
    plt.legend()
    plt.savefig('smoothing_plot.pdf', bbox_inches='tight')

    # increment figure counter
    n += 1


# plot jerk comparison between smothed and noisy signal
def jerk_comparison():
    global n
    plt.figure(n, figsize=(16.0, 10.0))
    for i in [10, 20, 30, 40, 50]:
        plt.plot(A[:, AD.TIME], smooth(A_grad_jerk[:, ], i, window='hanning'),
                 label='$j_{grad,smooth,' + str(i) + '}$')
        plt.xlabel('Time [s]', fontsize=20)
        plt.ylabel('j $[m/s^3]$', fontsize=20)
        plt.legend(fontsize=15)
        plt.grid(True)
    plt.title('Jerk comparison different smoothing', fontsize=20)
    plt.axis([18, 23, -.5, 7])
    plt.draw()
    plt.savefig('jerk_comparison.pdf', bbox_inches='tight')

    # increment figure counter
    n += 1


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='low')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    """
    @param data: data to filter
    @param lowcut: lowpass cutoff frequency
    @param highcut: highpass cutoff frequency
    @param fs: sample rate
    @param order: order of butterworth filter
    """
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y


# AD stands for ArrayData
class AD(enumerate):
    TIME = 0
    HS = 1
    FHS = 2
    VEL_X = 3
    VEL_Y = 4
    OME_Z = 5
    POS_X = 6
    POS_Y = 7


def smooth(x, window_len=11, window='hanning'):
    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."

    if window_len < 3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"

    s = np.r_[x[window_len - 1:0:-1], x, x[-2:-window_len - 1:-1]]
    # print(len(s))
    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.' + window + '(window_len)')

    y = np.convolve(w / w.sum(), s, mode='valid')

    return y[(window_len / 2 - 1):-(window_len / 2)]
    # return y


# read data from .csv-file
def read_data():
    global A
    global m_A
    global n_A
    with open('Ingolstadt_Test3.csv', 'rb') as csvfile:
        odometry_reader = csv.DictReader(csvfile, delimiter=',')
        # column_names_csv is of type 'list'
        column_names_csv = odometry_reader.fieldnames
        # get number of rows in csv-file
        row_number = sum(1 for line in odometry_reader)
        A = np.zeros([row_number, data.__len__()], dtype=np.double)
        # set pointer to first row
        csvfile.seek(0)
        # jump over first now with names
        odometry_reader.next()

        i = 0
        for row in odometry_reader:
            # jump over header row with names
            if row[data[0]] == time:
                continue
            j = 0
            for name in data:
                if name == time or name == fhs:
                    # scale time and field.header.stamp with factor 1e-9
                    scale = 10 ** -9
                else:
                    # otherwise no scaling is needed
                    scale = 1
                a = row[name]
                A[i, j] = float(a) * scale
                j += 1
            i += 1

    # set time to start at 0s
    A[:, AD.TIME] = A[:, AD.TIME] - A[0, AD.TIME]
    # save dimensions of A
    m_A, n_A = A.shape

    print 'Time of Interval: {:.2f} [s]'.format(A[-1, AD.TIME] - A[0, AD.TIME])


# get differentiation from given data
def differentiation():
    global A_grad
    global A_grad_vel
    global A_grad_vel_x
    global A_grad_vel_y
    global A_grad_acc
    global A_grad_acc_x
    global A_grad_acc_y
    global A_grad_jerk
    global A_grad_jerk_x
    global A_grad_jerk_y

    global A_diff


    # differentiation
    A_grad_vel_x = np.gradient(A[:, AD.POS_X], A[1, AD.FHS] - A[0, AD.FHS])
    A_grad_vel_y = np.gradient(A[:, AD.POS_Y], A[1, AD.FHS] - A[0, AD.FHS])
    # (x^2+y^2)^0.5 to get absolut velocity
    A_grad_vel = np.sqrt(A_grad_vel_x[:, ] ** 2 + A_grad_vel_y[:, ] ** 2)

    # differentiation
    # compute acceleration from velocity by differentiation
    A_grad_acc_x = np.gradient(A[:, AD.VEL_X], A[1, AD.FHS] - A[0, AD.FHS])
    A_grad_acc_y = np.gradient(A[:, AD.VEL_Y], A[1, AD.FHS] - A[0, AD.FHS])
    # (x^2+y^2)^0.5 to get absolut acceleration
    A_grad_acc = np.sqrt(A_grad_acc_x[:, ] ** 2 + A_grad_acc_y[:, ] ** 2)

    # differentiation
    # compute jerk from acceleration by differentiation
    A_grad_jerk_x = np.gradient(A_grad_acc_x[:, ], A[1, AD.FHS] - A[0, AD.FHS])
    A_grad_jerk_y = np.gradient(A_grad_acc_y[:, ], A[1, AD.FHS] - A[0, AD.FHS])
    # (x^2+y^2)^0.5 to get absolut jerk
    A_grad_jerk = np.sqrt(A_grad_jerk_x[:, ] ** 2 + A_grad_jerk_y[:, ] ** 2)

    # differentiation using diff
    A_diff = np.diff(np.transpose(A))
    print 'm * n of A_grad:\t', A_grad_acc.shape
    print 'm * n of A:\t\t', A.shape
    print 'n * m of A_diff:\t', A_diff.shape
    A_diff = np.transpose(A_diff)


def main():
    smoothing_plot()
    jerk_comparison()
    show_figures()


# close all existing figures
plt.close("all")

# number counter for figures
n = 1

# save header names for further use
time = '%time'
hs = 'field.header.seq'
fhs = 'field.header.stamp'  # stamp for calculating differentiation
vel_x = 'field.twist.twist.linear.x'  # velocity x-direction
vel_y = 'field.twist.twist.linear.y'  # velocity y-direction
ome_z = 'field.twist.twist.angular.z'  # omega around z-axis
pos_x = 'field.pose.pose.position.x'  # position x-axis
pos_y = 'field.pose.pose.position.y'  # position y-axis

data = [time, hs, fhs, vel_x, vel_y, ome_z, pos_x, pos_y]

if __name__ == '__main__':
    read_data()
    differentiation()

    # ===========================================================================
    # b1, a1 = signal.butter(5, .01)
    # y1 = signal.filtfilt(b1, a1, A[:, AD.VEL_X])
    # plt.figure(3)
    # plt.plot(A[:, AD.TIME], A[:, AD.VEL_X], 'b', alpha=0.75)
    # plt.plot(A[:, AD.TIME], y1, 'k')
    # plt.legend(('noisy signal', 'filtfilt'), loc='best')
    # plt.savefig('butterworth_lowpass.png', bbox_inches='tight')
    # plt.show()
    # ===========================================================================

    fs = 50
    lowcut = 1
    highcut = 10

    # ===========================================================================
    # y = butter_bandpass_filter(A[:, AD.VEL_X], lowcut, highcut, fs, order=6)
    # plt.plot(A[:, AD.TIME], y, 'r', label='Filtered signal (%g Hz)' % 50)
    # plt.xlabel('time (seconds)')
    # plt.grid(True)
    # plt.axis('tight')
    # plt.legend(loc='upper left')
    # plt.draw()
    # plt.savefig('butterworth_bandpass.png', bbox_inches='tight')
    # plt.show()
    # ===========================================================================

    main()

pass

# TODO: 2. bandwith for jerk
# TODO: 3. bool if jerk lower bandwith
# TODO: 4. output if data smaller jerk bandwith max
# REVIEW: butterworth bandpass plots as pdf