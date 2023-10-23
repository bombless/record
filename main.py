# This is a sample Python script.
import librosa

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def main():

    # 加载WAV文件
    data, sample_rate = librosa.load('../record.wav')

    max_value = 0
    max_count = None

    for idx, x in enumerate(data):
        if max_value < abs(x):
            max_value = abs(x)
            max_count = idx
    print('max_value:', '{:.3f}'.format(max_value))
    print('max_value time:', '{:.1f}'.format(max_count / sample_rate))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
