def tryE():
    try:
        print(3)
        input()
    except KeyboardInterrupt:
        pass
    finally:
        tryE()


tryE()
