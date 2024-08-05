import pywifi
from pywifi import const
import time
import string

def list_wifi_networks():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    
    iface.scan()
    time.sleep(2)  # Wait for the scan to complete
    results = iface.scan_results()
    
    if not results:
        print("No Wi-Fi networks found. Please ensure your Wi-Fi adapter is enabled.")
        return
    
    for network in results:
        print(f"SSID: {network.ssid}, Signal: {network.signal}, Frequency: {network.freq}, IsProtected: {network.akm}, BSSID: {network.bssid}")

    return results

def findBestWifi(listOfNetworks):
    protectedNetworks = []
    protectedNetworks2G = []
    protectedNetworks5G = []
    bestNetwork = None

    if not listOfNetworks:
        print("No Wi-Fi networks found. Please ensure your Wi-Fi adapter is enabled.")
        return

    for network in listOfNetworks:
        if network.akm == [4]:
            networkName = network.ssid
            if networkName.startswith("vptower"):
                protectedNetworks.append(network)
                if network.freq < 3000000:
                    protectedNetworks2G.append(network)
                else:
                    protectedNetworks5G.append(network)
    
    if  not protectedNetworks:
        print("No protected networks found.")
        return
    if protectedNetworks2G:
        print("2.4GHz Networks:")
        protectedNetworks2G.sort(key=lambda net: net.signal, reverse=True)
        for network in protectedNetworks2G:
            print(f"SSID: {network.ssid}, Signal: {network.signal}")
        
        bestNetwork = protectedNetworks2G[0]
    else:
        print("No 2.4GHz networks found.")

    if protectedNetworks5G:
        print("5GHz Networks:")
        protectedNetworks5G.sort(key=lambda net: net.signal, reverse=True)
        for network in protectedNetworks5G:
            print(f"SSID: {network.ssid}, Signal: {network.signal}")

        bestNetwork = protectedNetworks5G[0]
    else:
        print("No 5GHz networks found.")

    if bestNetwork:
        print(f"Best network: {bestNetwork.ssid}, Signal: {bestNetwork.signal}, Frequency: {bestNetwork.freq}, IsProtected: {bestNetwork.akm}, BSSID: {bestNetwork.bssid}")
        return bestNetwork
    else:
        print("No best network found.")

def connectToWifi(network):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.disconnect()
    time.sleep(1)
    profile = pywifi.Profile()
    profile.ssid = network.ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP


    # Création du mot de passe
    # Trouver une série de 4 chiffres
    serieChiffres = []
    for i in range(len(network.ssid)):
        if network.ssid[i].isdigit() and (network.ssid[i+1].isdigit() or network.ssid[i-1].isdigit()):
            serieChiffres.append(network.ssid[i])
    
    password = 'vptower' + ''.join(serieChiffres)
    print(f"Password : {password}")

    # password = network.ssid[:11]

    profile.key = password
    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)
    iface.connect(tmp_profile)
    time.sleep(3)
    if iface.status() == const.IFACE_CONNECTED:
        print(f"Connected to {network.ssid}")
    else:
        print(f"Failed to connect to {network.ssid}")






if __name__ == "__main__":
    try:
        scanResults = list_wifi_networks()
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        networkCandidate = findBestWifi(scanResults)
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        connectToWifi(networkCandidate)
    except Exception as e:
        print(f"An error occurred: {e}")
