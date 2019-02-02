import asyncio
import aiohttp
import logging

logging.basicConfig(filename='asynCrawl.log', level=logging.ERROR)


class AsnycGrab(object):

    def __init__(self, url_list, max_threads):
        self.urls = url_list
        self.results = {"num": 0, "data": {}}
        self.max_threads = max_threads

    def __parse_results(self, serial, resJson):
        if resJson:
            self.results["data"][serial] = resJson
            self.results["num"] += 1
        else:
            print('None...')

    async def get_body(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.post(url["batch_url"], json=url["payload"], timeout=2) as response:
                assert response.status == 200
                resJson = await response.json(encoding='utf8')
                return url["serial"], resJson

    async def get_results(self, url):
        serial, resJson = await self.get_body(url)
        self.__parse_results(serial, resJson)
        return 'Completed'

    async def handle_tasks(self, task_id, work_queue):
        while not work_queue.empty():
            current_url = await work_queue.get()
            try:
                task_status = await self.get_results(current_url)
            except Exception as e:
                logging.exception('Error for {}'.format(current_url["serial"]), exc_info=True)
                work_queue.put_nowait(current_url)

    def eventloop(self):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        q = asyncio.Queue()
        [q.put_nowait(url) for url in self.urls]
        tasks = [self.handle_tasks(task_id, q, ) for task_id in range(self.max_threads)]
        new_loop.run_until_complete(asyncio.wait(tasks))
        new_loop.close()


if __name__ == '__main__':
    urls = [{"batch_url": "", "payload": {"opts": [{"url": ""}, {}]}}, {}]
    print("main...")
    async_example = AsnycGrab(urls, 5)
    async_example.eventloop()
    logging.info(async_example.results)
