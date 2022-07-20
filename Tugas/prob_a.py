def main():
    N = int(input())
    if N > 0 and N <= 1000:
        pass
    else:
        quit()  # jika error
    Mark = 0
    Data = []
    for i in range(N):
        Ai = int(input())
        if (Ai > -1000) and (Ai < 1000) and Ai != 0:
            if (Ai < 0):
                # Scan Data
                # flag
                flag = False

            for z in range(len(Data)):  # Scan Data
                if abs(Data[z]) == abs(Ai):
                    flag = True
                    break
                else:
                    flag == False
                # Jika Sampai Selesai tidak ketemu
            if flag is False:
                Mark += 1
            Data.append(Ai)
        else:
            break

    # print(Data)
    print(Mark)


if __name__ == "__main__":
    main()
