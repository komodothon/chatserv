"""/test1.py"""

import asyncio

async def main():
    print("Start")
    await asyncio.sleep(5)  # doesn't block, allows other tasks to run
    print("End")

asyncio.run(main())