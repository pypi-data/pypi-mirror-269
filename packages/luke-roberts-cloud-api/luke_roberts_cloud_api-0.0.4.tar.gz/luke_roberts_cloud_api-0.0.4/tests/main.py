from src.luke_roberts_cloud_api.lrcloud import LukeRobertsCloud
import asyncio


async def main():
    lrcloud = LukeRobertsCloud()
    lrcloud.set_api_key(api_key="076f35c0-25b9-434b-8671-612fc3165b41")
    await lrcloud.fetch()
    lamp = lrcloud.get_lamps()[0]
    print(lamp)
    await lamp.set_scene(12)


asyncio.run(main())
