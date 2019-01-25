import asyncio
import aiohttp
import json
import logging

logging.basicConfig(filename='asynCrawl.log', level=logging.INFO)


class AsnycGrab(object):

    def __init__(self, url_list, max_threads):
        self.urls = url_list
        self.results = {}
        self.max_threads = max_threads

    def __parse_results(self, url, resJson):
        if resJson:
            self.results[url] = resJson
        else:
            print('None...')

    async def get_body(self, url):
        async with aiohttp.ClientSession() as session:
            print(url["payload"])
            async with session.post(url["batch_url"], json=url["payload"], timeout=1) as response:
                assert response.status == 200
                resJson = await response.json(encoding='utf8')
                return response.url, resJson

    async def get_results(self, url):
        url, resJson = await self.get_body(url)
        self.__parse_results(url, resJson)
        return 'Completed'

    async def handle_tasks(self, task_id, work_queue):
        while not work_queue.empty():
            current_url = await work_queue.get()
            try:
                task_status = await self.get_results(current_url)
            except Exception as e:
                logging.exception('Error for {}'.format(current_url), exc_info=True)

    def eventloop(self):
        q = asyncio.Queue()
        [q.put_nowait(url) for url in self.urls]
        loop = asyncio.get_event_loop()
        tasks = [self.handle_tasks(task_id, q, ) for task_id in range(self.max_threads)]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()


if __name__ == '__main__':
    urls = [{"batch_url": "", "payload": {"opts": [{"url": ""}, {}]}}, {}]
    print("main...")
    async_example = AsnycGrab(urls, 5)
    async_example.eventloop()
    logging.info(async_example.results)
