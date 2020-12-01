def connect(ssid, password):
    import network
    station = network.WLAN(network.STA_IF)

    if station.isconnected():
        print("Ja esta conectado")
        return

    station.active(True)
    station.connect(ssid, password)

    while not station.isconnected():
        pass

    print("Conexao bem sucedida!")
    print(station.ifconfig())