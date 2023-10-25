import time
import librosa
import glob

import read_with_numpy


def read(file):

    start_time = time.time()
    data, sample_rate = librosa.load(file)
    end_load_time = time.time()
    load_time = end_load_time - start_time
    print('load_time: {:.2f} seconds'.format(load_time))

    start_read_time = time.time()
    max_index = read_with_numpy.arg_max(data)
    end_read_time = time.time()
    read_time = end_read_time - start_read_time
    print('read_time: {:.2f} seconds'.format(read_time))

    max_value = data[max_index]

    print('max_value:', '{:.3f}'.format(max_value))
    print('max_value time:', format_time(max_index / sample_rate))

    end_round_time = time.time()
    round_time = end_round_time - start_time
    print('round_time: {:.2f} seconds'.format(round_time))


def format_time(seconds):
    return '{:.0f}:{:02.0f}:{:02.1f}'.format(seconds // 3600, seconds % 3600 // 60, seconds % 60)


def main():
    start_time = time.time()
    file_list = glob.glob('e:/20231025/record-*.wav')
    for file in file_list:
        print(file, ':')
        read(file)
    end_time = time.time()
    total_time = end_time - start_time
    print('total_time: {:.2f} seconds'.format(total_time))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
