import ark
import sys


def read_scp(scpFile):
    arkReader = ark.ArkReader(scpFile)
    for key in arkReader.scp_data:
        in_matr = arkReader.read_utt_data(key)
        print ("utt = " + key + ", Input mat size = " + str(in_matr.shape[0]) + " rows and " + str(
            in_matr.shape[1]) + " columns")

        """
        for i in range(in_matr.shape[0]):
            sys.stdout.write("\n")
            for j in range(in_matr.shape[1]):
                sys.stdout.write(str(in_matr[i][j]) + " ")
        """

        return in_matr


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("USAGE: python " + sys.argv[0] + " scpFile")
        exit(1)
    scp = sys.argv[1]
    read_scp(scp)
