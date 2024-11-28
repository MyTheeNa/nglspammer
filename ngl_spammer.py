import asyncio
import aiohttp
import json
import uuid
import random
import time
import sys
from colorama import init, Fore, Style
from tqdm import tqdm

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

init(autoreset=True)

import string
from typing import List
import platform
import socket
from datetime import datetime
import threading
from queue import Queue

class ConsoleUI:
    def __init__(self):
        self.message_queue = Queue()
        self.stop_thread = False
        self.last_status = ""
        
    def start(self):
        self.stop_thread = False
        self.ui_thread = threading.Thread(target=self._update_ui)
        self.ui_thread.start()
    
    def stop(self):
        self.stop_thread = True
        self.ui_thread.join()
        
    def _update_ui(self):
        while not self.stop_thread:
            while not self.message_queue.empty():
                msg = self.message_queue.get()
                if self.last_status:
                    sys.stdout.write('\033[F\033[K')
                print(msg)
                self.last_status = msg
            time.sleep(0.1)
    
    def update_status(self, success, failed, total, current_batch):
        success_rate = (success / total * 100) if total > 0 else 0
        failed_rate = (failed / total * 100) if total > 0 else 0
        
        progress = int((success + failed) / total * 30)
        if progress < 30:
            pulse_pos = progress % 30
            bar = '░' * 30
            bar = bar[:pulse_pos] + '█' + bar[pulse_pos+1:]
            bar = bar[:progress] + ('█' * (progress - (0 if progress == 0 else 1)))
        else:
            bar = '█' * 30
        
        status = f"""
{Style.BRIGHT}{Fore.WHITE}NGLSpammer{Style.RESET_ALL} {Fore.CYAN}v2.0

{Fore.GREEN}✓ {success}/{total} ({success_rate:.1f}%)
{Fore.RED}✗ {failed}/{total} ({failed_rate:.1f}%)
{Fore.BLUE}➤ {bar}
{Fore.YELLOW}⚡ Batch #{current_batch}{Style.RESET_ALL}
"""
        self.message_queue.put(status)

class NGLSpammer:
    def __init__(self, username: str, num_messages: int = 100, concurrency: int = 100):
        self.username = username
        self.num_messages = num_messages
        self.concurrency = concurrency
        self.base_url = "https://ngl.link/api/submit"
        self.success_count = 0
        self.failed_count = 0
        self.device_ids = self.generate_device_ids(num_messages)
        self.user_agents = self.generate_user_agents()
        self.cookies = {}
        self.retry_delay = 1
        self.max_retries = 5
        self.ui = ConsoleUI()
        self.current_batch = 1
        
    def print_banner(self):
        banner = f"""
{Style.BRIGHT}{Fore.YELLOW}Welcome to NGLSpammer{Style.RESET_ALL}

{Fore.WHITE}Target    : {Fore.GREEN}{self.username}
{Fore.WHITE}Messages  : {Fore.GREEN}{self.num_messages}
{Fore.WHITE}Concurrent: {Fore.GREEN}{self.concurrency}
"""
        print(banner)

    def generate_device_ids(self, count):
        return [str(uuid.uuid4()) for _ in range(count)]
    
    def generate_user_agents(self):
        chrome_versions = [str(v) for v in range(90, 120)]
        platforms = ['Windows NT 10.0', 'Windows NT 11.0', 'Macintosh; Intel Mac OS X 10_15_7']
        agents = []
        for platform in platforms:
            for version in chrome_versions:
                agent = f"Mozilla/5.0 ({platform}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.{random.randint(1000,9999)}.{random.randint(100,999)} Safari/537.36"
                agents.append(agent)
        return agents

    def generate_tracking_id(self):
        timestamp = int(time.time() * 1000)
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        return f"{timestamp}-{random_str}"

    async def send_message_with_retry(self, session: aiohttp.ClientSession, message: str, index: int) -> bool:
        retries = 0
        while retries < self.max_retries:
            success = await self._try_send_message(session, message, index)
            if success:
                return True
            
            retries += 1
            if retries < self.max_retries:
                delay = self.retry_delay * (2 ** retries) + random.uniform(0, 1)
                await asyncio.sleep(delay)
        return False

    async def _try_send_message(self, session: aiohttp.ClientSession, message: str, index: int) -> bool:
        device_id = self.device_ids[index % len(self.device_ids)]
        timestamp = int(time.time() * 1000)
        
        tracking_props = {
            "trackingId": self.generate_tracking_id(),
            "userId": device_id,
            "deviceId": device_id,
            "sessionId": str(uuid.uuid4()),
            "timestamp": timestamp,
            "platform": "web",
            "client": "chrome",
            "version": "1.0.0"
        }
        
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "dnt": "1",
            "origin": "https://ngl.link",
            "priority": "u=1, i",
            "referer": f"https://ngl.link/{self.username}",
            "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": random.choice(self.user_agents),
            "x-requested-with": "XMLHttpRequest"
        }
        
        data = {
            "username": self.username,
            "question": message,
            "deviceId": device_id,
            "gameSlug": "",
            "referrer": "",
            "trackingInfo": json.dumps(tracking_props),
            "_time": str(timestamp)
        }
        
        try:
            async with session.post(
                self.base_url,
                headers=headers,
                data=data,
                timeout=aiohttp.ClientTimeout(total=10),
                ssl=False
            ) as response:
                if response.status == 200:
                    self.success_count += 1
                    self.ui.update_status(self.success_count, self.failed_count, self.num_messages, self.current_batch)
                    self.cookies.update(session.cookie_jar.filter_cookies(self.base_url))
                    return True
                else:
                    self.failed_count += 1
                    self.ui.update_status(self.success_count, self.failed_count, self.num_messages, self.current_batch)
                    return False
        except Exception as e:
            self.failed_count += 1
            self.ui.update_status(self.success_count, self.failed_count, self.num_messages, self.current_batch)
            return False

    def generate_messages(self) -> List[str]:
        emojis = ["❤️", "😊", "🎉", "👋", "✨", "🌟", "💫", "💕", "🔥", "👍", "💖", "💝", "💓", "💗", "💞"]
        base_messages = [
            "Hey!", "Hi!", "Hello!", "What's up?", "How are you?", "Hey there!", 
            "Nice to meet you!", "Having a good day?", "You're awesome!", 
            "Keep smiling!", "Stay positive!", "You're doing great!",
            "Miss you!", "Take care!", "Be happy!", "Stay strong!",
            "You're amazing!", "Keep going!", "You got this!",
            "Sending good vibes!", "Have a great day!"
        ]
        
        result = []
        for _ in range(self.num_messages):
            msg = random.choice(base_messages)
            timestamp = datetime.now().strftime("%H:%M:%S")
            msg = f"{msg} [{timestamp}]"
            if random.random() < 0.5:
                msg += " " + random.choice(emojis)
            if random.random() < 0.3:
                msg += random.choice(emojis)
            result.append(msg)
        return result

    async def spam(self):
        self.print_banner()
        print(f"{Fore.YELLOW}Initializing spam attack...{Style.RESET_ALL}")
        time.sleep(1)
        
        self.ui.start()
        start_time = time.time()
        
        connector = aiohttp.TCPConnector(
            limit=None,
            force_close=True,
            ssl=False
        )
        
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            messages = self.generate_messages()
            total_batches = (len(messages) + self.concurrency - 1) // self.concurrency
            
            for i in range(0, len(messages), self.concurrency):
                batch = messages[i:i + self.concurrency]
                tasks = [self.send_message_with_retry(session, message, i+j) for j, message in enumerate(batch)]
                await asyncio.gather(*tasks, return_exceptions=True)
                self.current_batch += 1
                await asyncio.sleep(random.uniform(0.5, 1.5))
        
        self.ui.stop()
        end_time = time.time()
        duration = end_time - start_time
        
        stats = f"""
{Style.BRIGHT}{Fore.WHITE}Mission Complete{Style.RESET_ALL}

{Fore.GREEN}✓ Success: {self.success_count}/{self.num_messages}
{Fore.RED}✗ Failed : {self.failed_count}/{self.num_messages}
{Fore.BLUE}⏱ Time   : {duration:.2f}s
{Fore.YELLOW}⚡ Rate   : {self.success_count/duration:.2f} msg/s{Style.RESET_ALL}
"""
        print(stats)

async def main():
    try:
        print(f"{Style.BRIGHT}{Fore.YELLOW}Welcome to NGL Spammer{Style.RESET_ALL}\n")
        
        username = input(f"{Fore.GREEN}Enter NGL username: {Style.RESET_ALL}")
        num_messages = int(input(f"{Fore.GREEN}Enter number of messages to send: {Style.RESET_ALL}"))
        concurrency = int(input(f"{Fore.GREEN}Enter concurrency level (recommended 50-100): {Style.RESET_ALL}"))
        
        spammer = NGLSpammer(username, num_messages, concurrency)
        await spammer.spam()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Stopping spam...{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    asyncio.run(main())
