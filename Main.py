
import requests
import socket
import speedtest
import platform
import subprocess
import time
from scapy.all import sr1, IP, TCP
from colorama import init, Fore, Style
from datetime import datetime

init()

logo = """
NetProb

Crate by @hfsads
Site: https://hfs1.ct.ws
"""

def get_ip_info():
    try:
        ip_response = requests.get('https://api.ipify.org?format=json').json()
        ip = ip_response['ip']
        info_response = requests.get(f'http://ip-api.com/json/{ip}').json()
        
        if info_response['status'] == 'success':
            return {
                'ip': ip,
                'country': info_response['country'],
                'city': info_response['city'],
                'isp': info_response['isp'],
                'region': info_response['regionName'],
                'timezone': info_response['timezone']
            }
        return None
    except:
        return None

def save_results(speed_test_results, ip_info, site_results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"internet_test_results_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=== Результаты проверки интернет-соединения ===\n\n")
        
        if ip_info:
            f.write("Информация о подключении:\n")
            f.write(f"IP адрес: {ip_info['ip']}\n")
            f.write(f"Страна: {ip_info['country']}\n")
            f.write(f"Город: {ip_info['city']}\n")
            f.write(f"Провайдер: {ip_info['isp']}\n")
            f.write(f"Регион: {ip_info['region']}\n")
            f.write(f"Часовой пояс: {ip_info['timezone']}\n\n")
        
        f.write("Результаты теста скорости:\n")
        for line in speed_test_results:
            f.write(f"{line}\n")
            
        f.write("\nРезультаты проверки сайтов:\n")
        for category, sites in site_results.items():
            f.write(f"\n=== {category} ===\n")
            for site in sites:
                f.write(f"{site}\n")
            
    return filename

def check_site_availability(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return f"{Fore.GREEN}Сайт {url} доступен.{Style.RESET_ALL}"
        else:
            return f"{Fore.RED}Сайт {url} недоступен.{Style.RESET_ALL}"
    except:
        return f"{Fore.RED}Сайт {url} недоступен.{Style.RESET_ALL}"

def check_internet_speed():
    results = []
    print(f"{Fore.CYAN}Проверка скорости интернета...{Style.RESET_ALL}")
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        
        download_speed = st.download() / 1_000_000
        download_result = f"Скорость загрузки: {download_speed:.2f} Мбит/с"
        print(f"{Fore.GREEN}{download_result}{Style.RESET_ALL}")
        results.append(download_result)
        
        upload_speed = st.upload() / 1_000_000
        upload_result = f"Скорость отдачи: {upload_speed:.2f} Мбит/с"
        print(f"{Fore.GREEN}{upload_result}{Style.RESET_ALL}")
        results.append(upload_result)
        
        ping = st.results.ping
        ping_result = f"Пинг: {ping:.0f} мс"
        print(f"{Fore.GREEN}{ping_result}{Style.RESET_ALL}")
        results.append(ping_result)
        
        if download_speed >= 55:
            video_quality = "Доступно видео в качестве 4K/UHD (2160p)"
        elif download_speed >= 24:
            video_quality = "Доступно видео в качестве 2K (1440p)"
        elif download_speed >= 12:
            video_quality = "Доступно видео в качестве 1080p"
        elif download_speed >= 7:
            video_quality = "Доступно видео в качестве 720p"
        elif download_speed >= 4:
            video_quality = "Доступно видео в качестве 480p"
        elif download_speed >= 2:
            video_quality = "Доступно видео в качестве 360p"

        else:
            video_quality = "Меньше 360p, проблемы при просмотре"
        print(f"{Fore.GREEN}{video_quality}{Style.RESET_ALL}")
        results.append(video_quality)
            
        if ping < 50 and download_speed > 15 and upload_speed > 5:
            gaming_quality = "Отличное соединение для онлайн игр"
        elif ping < 100 and download_speed > 10 and upload_speed > 3:
            gaming_quality = "Хорошее соединение для онлайн игр"
        else:
            gaming_quality = "Возможны проблемы в онлайн играх"
        print(f"{Fore.GREEN}{gaming_quality}{Style.RESET_ALL}")
        results.append(gaming_quality)
            
        return results
    except Exception as e:
        error_msg = f"Ошибка при проверке скорости: {str(e)}"
        print(f"{Fore.RED}{error_msg}{Style.RESET_ALL}")
        results.append(error_msg)
        return results

def check_ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    try:
        output = subprocess.check_output(command).decode().strip()
        if 'TTL=' in output or 'ttl=' in output:
            time = output.split('time=')[1].split('ms')[0].strip()
            return f"{Fore.GREEN}Пинг до {host}: {time}ms{Style.RESET_ALL}"
        return f"{Fore.RED}Хост {host} недоступен{Style.RESET_ALL}"
    except:
        return f"{Fore.RED}Ошибка проверки пинга до {host}{Style.RESET_ALL}"

def main():
    while True:
        # Списки сайтов для проверки
        vpn_proxy = [
            "https://psiphon.ca", "https://www.torproject.org", 
            "https://www.protonvpn.com", "https://www.expressvpn.com",
            "https://www.nordvpn.com", "https://www.cyberghostvpn.com",
            "https://www.surfshark.com", "https://www.privateinternetaccess.com",
            "https://www.hotspotshield.com", "https://www.tunnelbear.com",
            "https://www.windscribe.com", "https://www.mullvad.net",
            "https://www.ipvanish.com", "https://www.vyprvpn.com",
            "https://www.zenmate.com"
        ]

        bypass_services = [
            "https://www.shadowsocks.org", "https://www.v2ray.com",
            "https://www.lantern.io", "https://www.ultrasurf.us",
            "https://www.freegate.pro", "https://www.openvpn.net",
            "https://www.wireguard.com", "https://www.softether.org",
            "https://www.getoutline.org", "https://www.i2p-projekt.de",
            "https://www.freenet.org"
        ]

        social_networks = [
            "https://www.facebook.com", "https://www.instagram.com",
            "https://www.twitter.com", "https://www.linkedin.com",
            "https://www.pinterest.com", "https://www.tumblr.com",
            "https://www.reddit.com", "https://www.vk.com",
            "https://www.ok.ru", "https://www.weibo.com",
            "https://www.tiktok.com", "https://www.snapchat.com",
            "https://www.flickr.com", "https://www.meetup.com",
            "https://www.myspace.com"
        ]

        messengers = [
            "https://web.whatsapp.com", "https://web.telegram.org",
            "https://www.viber.com", "https://www.skype.com",
            "https://www.discord.com", "https://www.signal.org",
            "https://www.line.me", "https://www.wechat.com",
            "https://www.messenger.com", "https://www.kakao.com",
            "https://www.threema.ch", "https://www.wire.com"
        ]
        
        gaming = [
            "https://www.steam.com", "https://www.epicgames.com",
            "https://www.origin.com", "https://www.xbox.com",
            "https://www.playstation.com", "https://www.nintendo.com",
            "https://www.blizzard.com", "https://www.ea.com",
            "https://www.ubisoft.com", "https://www.gog.com",
            "https://www.riotgames.com", "https://www.rockstargames.com",
            "https://www.minecraft.net", "https://www.roblox.com",
            "https://www.twitch.tv", "https://www.leagueoflegends.com",
            "https://www.dota2.com", "https://www.fortnite.com",
            "https://www.warframe.com", "https://www.pathofexile.com"
        ]

        streaming = [
            "https://www.netflix.com", "https://www.youtube.com",
            "https://www.twitch.tv", "https://www.spotify.com",
            "https://www.soundcloud.com", "https://www.deezer.com",
            "https://www.tidal.com", "https://www.hulu.com",
            "https://www.disneyplus.com", "https://www.primevideo.com",
            "https://www.hbomax.com", "https://www.pandora.com",
            "https://www.appletv.com", "https://www.peacocktv.com",
            "https://www.crunchyroll.com"
        ]

        cloud_storage = [
            "https://www.dropbox.com", "https://drive.google.com",
            "https://www.onedrive.live.com", "https://www.box.com",
            "https://www.mega.nz", "https://www.icloud.com",
            "https://www.mediafire.com", "https://www.pcloud.com",
            "https://www.sync.com"
        ]

        popular_sites = [
            "https://www.google.com", "https://www.yahoo.com",
            "https://www.bing.com", "https://www.amazon.com",
            "https://www.ebay.com", "https://www.alibaba.com",
            "https://www.walmart.com", "https://www.target.com",
            "https://www.bestbuy.com", "https://www.wikipedia.org",
            "https://www.github.com", "https://www.stackoverflow.com",
            "https://www.microsoft.com", "https://www.apple.com",
            "https://www.adobe.com", "https://www.wordpress.com",
            "https://www.blogger.com", "https://www.medium.com",
            "https://www.cnn.com", "https://www.bbc.com",
            "https://www.nytimes.com", "https://www.weather.com",
            "https://www.booking.com", "https://www.airbnb.com",
            "https://www.paypal.com", "https://www.visa.com",
            "https://www.mastercard.com"
        ]

        # Словарь для хранения результатов проверки сайтов
        site_results = {}
        print(logo)
        # Получаем информацию об IP
        print(f"\n{Fore.CYAN}=== Получение информации о подключении ==={Style.RESET_ALL}")
        ip_info = get_ip_info()
        if ip_info:
            print(f"IP адрес: {ip_info['ip']}")
            print(f"Страна: {ip_info['country']}")
            print(f"Город: {ip_info['city']}")
            print(f"Провайдер: {ip_info['isp']}")
            print(f"Регион: {ip_info['region']}")
            print(f"Часовой пояс: {ip_info['timezone']}")
        else:
            print(f"{Fore.RED}Не удалось получить информацию о подключении{Style.RESET_ALL}")

        # Проверка скорости интернета
        print(f"\n{Fore.CYAN}=== Проверка интернет-соединения ==={Style.RESET_ALL}")
        speed_test_results = check_internet_speed()

        # Проверка пинга до основных серверов
        print(f"\n{Fore.CYAN}=== Проверка пинга до популярных серверов ==={Style.RESET_ALL}")
        servers = [
            "google.com", "youtube.com", "amazon.com",
            "facebook.com", "netflix.com"
        ]
        ping_results = []
        for server in servers:
            result = check_ping(server)
            print(result)
            ping_results.append(result.replace(Fore.GREEN, '').replace(Fore.RED, '').replace(Style.RESET_ALL, ''))

        # Проверка всех сайтов
        print(f"\n{Fore.CYAN}=== Социальные сети ==={Style.RESET_ALL}")
        social_results = []
        for url in social_networks:
            result = check_site_availability(url)
            print(result)
            social_results.append(result.replace(Fore.GREEN, '').replace(Fore.RED, '').replace(Style.RESET_ALL, ''))
        site_results['Социальные сети'] = social_results

        print(f"\n{Fore.CYAN}=== Мессенджеры ==={Style.RESET_ALL}")
        messenger_results = []
        for url in messengers:
            result = check_site_availability(url)
            print(result)
            messenger_results.append(result.replace(Fore.GREEN, '').replace(Fore.RED, '').replace(Style.RESET_ALL, ''))
        site_results['Мессенджеры'] = messenger_results

        print(f"\n{Fore.CYAN}=== Игровые сервисы ==={Style.RESET_ALL}")
        gaming_results = []
        for url in gaming:
            result = check_site_availability(url)
            print(result)
            gaming_results.append(result.replace(Fore.GREEN, '').replace(Fore.RED, '').replace(Style.RESET_ALL, ''))
        site_results['Игровые сервисы'] = gaming_results

        print(f"\n{Fore.CYAN}=== Стриминговые сервисы ==={Style.RESET_ALL}")
        streaming_results = []
        for url in streaming:
            result = check_site_availability(url)
            print(result)
            streaming_results.append(result.replace(Fore.GREEN, '').replace(Fore.RED, '').replace(Style.RESET_ALL, ''))
        site_results['Стриминговые сервисы'] = streaming_results

        print(f"\n{Fore.CYAN}=== Облачные хранилища ==={Style.RESET_ALL}")
        cloud_results = []
        for url in cloud_storage:
            result = check_site_availability(url)
            print(result)
            cloud_results.append(result.replace(Fore.GREEN, '').replace(Fore.RED, '').replace(Style.RESET_ALL, ''))
        site_results['Облачные хранилища'] = cloud_results

        print(f"\n{Fore.CYAN}=== Популярные сайты ==={Style.RESET_ALL}")
        popular_results = []
        for url in popular_sites:
            result = check_site_availability(url)
            print(result)
            popular_results.append(result.replace(Fore.GREEN, '').replace(Fore.RED, '').replace(Style.RESET_ALL, ''))
        site_results['Популярные сайты'] = popular_results

        print(f"\n{Fore.CYAN}=== VPN/Proxy сервисы ==={Style.RESET_ALL}")
        vpn_results = []
        for url in vpn_proxy:
            result = check_site_availability(url)
            print(result)
            vpn_results.append(result.replace(Fore.GREEN, '').replace(Fore.RED, '').replace(Style.RESET_ALL, ''))
        site_results['VPN/Proxy сервисы'] = vpn_results

        print(f"\n{Fore.CYAN}=== Сервисы обхода блокировок ==={Style.RESET_ALL}")
        bypass_results = []
        for url in bypass_services:
            result = check_site_availability(url)
            print(result)
            bypass_results.append(result.replace(Fore.GREEN, '').replace(Fore.RED, '').replace(Style.RESET_ALL, ''))
        site_results['Сервисы обхода блокировок'] = bypass_results

        # После завершения всех проверок
        print(f"\n{Fore.CYAN}=== Проверка завершена ==={Style.RESET_ALL}")
        
        # Спрашиваем о сохранении результатов
        save_choice = input("\nСохранить результаты? (y/n): ").lower()
        if save_choice == 'y':
            filename = save_results(speed_test_results, ip_info, site_results)
            print(f"\n{Fore.GREEN}Результаты сохранены в файл: {filename}{Style.RESET_ALL}")

        # Спрашиваем о повторном запуске
        restart_choice = input("\nЗапустить проверку снова? (y/n): ").lower()
        if restart_choice != 'y':
            print(f"\n{Fore.CYAN}Программа завершена.{Style.RESET_ALL}")
            break
        else:
            print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Программа прервана пользователем.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Произошла ошибка: {str(e)}{Style.RESET_ALL}")
          
