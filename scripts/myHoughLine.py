import numpy as np


def frange( initial , final , step ) :
    while initial < final :
        yield initial
        initial += step


def __extractLines__( accumulator , angles , threshold ) :
    lines = []
    for angle_index in range(accumulator.shape[0]) :
        for rho in range(accumulator.shape[1]) :
            if accumulator[angle_index , rho] > threshold :
                angle = angles[angle_index]
                # print (angle , rho , accumulator[angle_index , rho])
                lines.append((angle , rho))

    return lines


def myHoughLines( binaryImage , angleAccuracy , threshold ) :
    angles = frange(0 , np.pi , angleAccuracy)
    angles = np.fromiter(angles , dtype = np.float16)

    cartesianWidth = binaryImage.shape[1]
    cartesianHeight = binaryImage.shape[0]

    maxRadius = np.sqrt(cartesianWidth * cartesianWidth +
                        cartesianHeight * cartesianHeight)

    polarWidth = 180  # 180 degree
    polarHeight = int(maxRadius + 0.5)

    # Construct the empty accumulator
    accumulator = np.zeros((polarWidth , polarHeight) , dtype = np.uint16)
    print "Accumulator size:"
    print accumulator.shape
    # Caculate all sines and cosines once to reduce the overhead of redundant
    # float operations.
    sine_table = np.sin(angles , dtype = np.float16)
    cosine_table = np.cos(angles , dtype = np.float16)

    print "Extracting edge points"
    edge_points = [(row , col) for row in range(binaryImage.shape[0]) for col in
                   range(binaryImage.shape[1]) if binaryImage[row , col] != 0]

    edge_points = np.asanyarray(edge_points , dtype = np.uint16)

    for angle_index in range(polarWidth) :
        rho = np.array(np.round(sine_table[angle_index] * edge_points[: , 0] + \
                                cosine_table[angle_index] * edge_points[: ,
                                                            1]) , dtype = int)

        for r in np.nditer(rho , op_flags = ['readonly']) :
            accumulator[angle_index , r] += 1

    lines = __extractLines__(accumulator , angles , threshold)
    print("lines count:")
    print len(lines)
    # print lines
    return lines
